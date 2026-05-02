from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import db_mongo as db
import nlp_utils
import logging
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IQ Restaurant API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# In-memory sessions
sessions = {}   # session_id -> {cart, prefs_loaded}


def get_session(sid: str) -> dict:
    if sid not in sessions:
        sessions[sid] = {"cart": {}, "prefs_loaded": False}
    return sessions[sid]


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "message": "IQ Restaurant API v2.0 running"}


# ── Menu API ──────────────────────────────────────────────────────────────────

@app.get("/menu")
def get_menu():
    return db.get_all_menu()


# ── Cart / Order Chatbot endpoint ─────────────────────────────────────────────

@app.post("/chat")
async def chat(request: Request):
    payload    = await request.json()
    text       = payload.get("text", "").strip()
    session_id = payload.get("session_id", "guest")
    intent     = payload.get("intent", "")

    session = get_session(session_id)

    # Load prefs once per session
    if not session["prefs_loaded"]:
        prefs = db.get_prefs(session_id)
        session["prefs"] = prefs
        session["prefs_loaded"] = True

    logger.info(f"[{session_id}] intent={intent} text={text}")

    # Route
    if intent == "add":
        return handle_add(text, session_id, session)
    elif intent == "remove":
        return handle_remove(text, session_id, session)
    elif intent == "confirm":
        return handle_confirm(session_id, session)
    elif intent == "cancel":
        return handle_cancel(session_id, session)
    elif intent == "track":
        return handle_track(text, session_id)
    elif intent == "history":
        return handle_history(session_id)
    elif intent == "repeat":
        return handle_repeat(session_id, session)
    elif intent == "rate":
        return handle_rate(payload, session_id)
    elif intent == "prefs":
        return handle_prefs(payload, session_id, session)
    elif intent == "cart":
        return handle_cart(session_id, session)
    else:
        return JSONResponse(content={"text": "I'm not sure how to help with that. Try saying 'add 2 Samosa' or 'show my cart'."})


def handle_add(text: str, session_id: str, session: dict):
    parsed = nlp_utils.parse_food_items_from_text(text)

    if not parsed:
        return JSONResponse(content={
            "text": "I couldn't find any menu items in that. Could you be more specific? E.g. 'Add 2 Samosa and 1 Mango Lassi'",
            "suggestions": ["Show menu", "What's available?"]
        })

    # Filter out allergens
    prefs    = session.get("prefs", {})
    allergies = [a.lower() for a in prefs.get("allergies", [])]
    blocked  = []
    allowed  = {}
    for item, qty in parsed.items():
        item_data = db.get_item(item)
        tags = [t.lower() for t in (item_data.get("tags", []) if item_data else [])]
        if any(a in tags or a in item.lower() for a in allergies):
            blocked.append(item)
        else:
            allowed[item] = qty

    # Smart quantity correction: if user says "make it 3" etc, update existing
    for item, qty in allowed.items():
        session["cart"][item] = session["cart"].get(item, 0) + qty

    cart_str  = nlp_utils.get_str_from_food_dict(session["cart"])
    total     = sum(db.get_item_price(i) * q for i, q in session["cart"].items())

    resp_text = f"✅ Added to cart!\n\n🛒 Current order:\n{cart_str}\n\n💰 Total: ₹{total:.2f}"
    if blocked:
        resp_text += f"\n\n⚠️ Skipped {', '.join(blocked)} due to your allergy preferences."

    # XAI suggestions
    suggestions = []
    if any("Biryani" in i for i in session["cart"]) and "Mango Lassi" not in session["cart"]:
        suggestions.append("Add Mango Lassi — great with Biryani! 🥭")
    if any(db.get_item(i) and db.get_item(i).get("category") == "Dinner" for i in session["cart"]) \
            and not any("Naan" in i or "Roti" in i for i in session["cart"]):
        suggestions.append("Add Butter Naan or Garlic Naan to go with your curry? 🫓")

    return JSONResponse(content={
        "text": resp_text,
        "cart": session["cart"],
        "total": total,
        "suggestions": suggestions,
        "show_actions": True
    })


def handle_remove(text: str, session_id: str, session: dict):
    parsed = nlp_utils.parse_food_items_from_text(text)
    if not parsed or not session["cart"]:
        return JSONResponse(content={"text": "Nothing to remove or item not found."})

    removed = []
    for item in parsed:
        if item in session["cart"]:
            del session["cart"][item]
            removed.append(item)

    if not removed:
        return JSONResponse(content={"text": f"I couldn't find those items in your cart."})

    cart_str = nlp_utils.get_str_from_food_dict(session["cart"]) if session["cart"] else "Empty"
    total    = sum(db.get_item_price(i) * q for i, q in session["cart"].items())
    return JSONResponse(content={
        "text": f"🗑️ Removed {', '.join(removed)}.\n\n🛒 Cart: {cart_str}\n💰 Total: ₹{total:.2f}",
        "cart": session["cart"],
        "total": total,
        "show_actions": bool(session["cart"])
    })


def handle_confirm(session_id: str, session: dict):
    if not session["cart"]:
        return JSONResponse(content={"text": "Your cart is empty! Add some items first."})

    order_id = db.get_next_order_id()
    for item, qty in session["cart"].items():
        db.insert_order_item(item, qty, order_id, session_id)

    total = db.get_total_order_price(order_id)
    db.insert_order_tracking(order_id)
    db.save_order_to_history(order_id, session_id, dict(session["cart"]), total)

    # Estimate delivery time: 15 min base + 5 min per unique item
    eta_min = 15 + len(session["cart"]) * 5
    eta_max = eta_min + 10

    session["cart"]       = {}
    session["last_order"] = order_id

    return JSONResponse(content={
        "text": (
            f"🎉 Order #{order_id} placed!\n"
            f"💰 Total: ₹{total:.2f}\n"
            f"⏱️ Estimated delivery: {eta_min}–{eta_max} mins\n"
            f"💳 Pay on delivery (UPI QR below)\n\n"
            f"Track with: Order #{order_id}"
        ),
        "order_id": order_id,
        "total": total,
        "eta": f"{eta_min}–{eta_max} mins",
        "show_upi": True,
        "show_track": True,
        "show_rate": False
    })


def handle_cancel(session_id: str, session: dict):
    session["cart"] = {}
    return JSONResponse(content={
        "text": "🗑️ Order cancelled. Your cart is now empty.\n\nFeel free to start a fresh order! 😊",
        "cart": {}
    })


def handle_track(text: str, session_id: str):
    # Extract order id from text
    import re
    nums = re.findall(r'\d+', text)
    if not nums:
        # Try last order
        last = db.get_last_order(session_id)
        if last:
            order_id = last["order_id"]
        else:
            return JSONResponse(content={"text": "Please provide an order ID. E.g. 'Track order 5'"})
    else:
        order_id = int(nums[0])

    status = db.get_order_status(order_id)
    if not status:
        return JSONResponse(content={"text": f"No order found with ID #{order_id}."})

    steps   = ["Order Received", "Preparing", "Ready", "Out for Delivery", "Delivered"]
    current = status["status"]
    try:
        step_idx = steps.index(current)
    except ValueError:
        step_idx = 0

    progress = int(((step_idx + 1) / len(steps)) * 100)

    return JSONResponse(content={
        "text": f"📦 Order #{order_id}\nStatus: **{current}**\nProgress: {progress}%",
        "order_id": order_id,
        "status": current,
        "progress": progress,
        "steps": steps,
        "current_step": step_idx,
        "show_track_ui": True
    })


def handle_history(session_id: str):
    history = db.get_order_history(session_id, limit=5)
    if not history:
        return JSONResponse(content={"text": "No past orders found. Place your first order today! 🍽️"})

    lines = []
    for h in history:
        items_str = ", ".join([f"{q}×{i}" for i, q in h["items"].items()])
        lines.append(f"• Order #{h['order_id']} — ₹{h['total']} — {items_str}")

    return JSONResponse(content={
        "text": "📋 Your recent orders:\n\n" + "\n".join(lines),
        "history": history,
        "show_history_ui": True
    })


def handle_repeat(session_id: str, session: dict):
    last = db.get_last_order(session_id)
    if not last:
        return JSONResponse(content={"text": "No previous order found to repeat."})

    session["cart"] = dict(last["items"])
    total = sum(db.get_item_price(i) * q for i, q in session["cart"].items())
    cart_str = nlp_utils.get_str_from_food_dict(session["cart"])

    return JSONResponse(content={
        "text": f"♻️ Repeated your last order!\n\n🛒 {cart_str}\n💰 Total: ₹{total:.2f}",
        "cart": session["cart"],
        "total": total,
        "show_actions": True
    })


def handle_rate(payload: dict, session_id: str):
    order_id = payload.get("order_id")
    rating   = payload.get("rating", 5)
    comment  = payload.get("comment", "")
    if order_id:
        db.save_rating(order_id, session_id, rating, comment)
    stars = "⭐" * int(rating)
    return JSONResponse(content={"text": f"Thank you for your {stars} rating! Your feedback helps us improve. 🙏"})


def handle_prefs(payload: dict, session_id: str, session: dict):
    allergies = payload.get("allergies", [])
    prefs_text = payload.get("preferences", [])
    name      = payload.get("name", "")
    data      = {}
    if allergies:  data["allergies"]    = allergies
    if prefs_text: data["preferences"]  = prefs_text
    if name:       data["name"]         = name
    db.save_prefs(session_id, data)
    session["prefs"] = db.get_prefs(session_id)
    allergy_str = ", ".join(allergies) if allergies else "none"
    return JSONResponse(content={"text": f"✅ Preferences saved! Allergies noted: {allergy_str}. I'll make sure to flag these items."})


def handle_cart(session_id: str, session: dict):
    if not session["cart"]:
        return JSONResponse(content={"text": "Your cart is empty! Browse the menu and add something. 🍽️"})
    cart_str = nlp_utils.get_str_from_food_dict(session["cart"])
    total    = sum(db.get_item_price(i) * q for i, q in session["cart"].items())
    return JSONResponse(content={
        "text": f"🛒 Your cart:\n{cart_str}\n\n💰 Total: ₹{total:.2f}",
        "cart": session["cart"],
        "total": total,
        "show_actions": True
    })


# ── Admin API ─────────────────────────────────────────────────────────────────

@app.get("/admin/stats")
def admin_stats():
    return db.get_admin_stats()

@app.post("/admin/advance/{order_id}")
def admin_advance(order_id: int):
    new_status = db.advance_order_status(order_id)
    return {"order_id": order_id, "new_status": new_status}

@app.get("/admin/low-stock")
def admin_low_stock():
    return db.get_low_stock_items(10)


# ── Order Status Push (polling) ───────────────────────────────────────────────

@app.get("/status/{order_id}")
def get_status(order_id: int):
    status = db.get_order_status(order_id)
    if not status:
        raise HTTPException(status_code=404, detail="Order not found")
    return status
