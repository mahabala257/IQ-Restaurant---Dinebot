from pymongo import MongoClient, DESCENDING
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "iqrestaurant"

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

food_col     = db["food_items"]
orders_col   = db["orders"]
tracking_col = db["order_tracking"]
history_col  = db["order_history"]
prefs_col    = db["user_preferences"]
ratings_col  = db["ratings"]


# ── Menu ─────────────────────────────────────────────────────────────────────

def get_all_menu():
    return list(food_col.find({}, {"_id": 0}))

def get_item(name: str):
    return food_col.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}}, {"_id": 0})

def get_item_price(name: str):
    item = get_item(name)
    return float(item["price"]) if item else 0

def get_all_prices():
    return {i["name"]: float(i["price"]) for i in food_col.find({}, {"_id": 0})}

def decrement_stock(name: str, qty: int):
    food_col.update_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"$inc": {"stock": -qty, "orders": qty}}
    )

def get_low_stock_items(threshold: int = 5):
    return list(food_col.find({"stock": {"$lte": threshold}}, {"_id": 0, "name": 1, "stock": 1}))


# ── Orders ────────────────────────────────────────────────────────────────────

def get_next_order_id():
    counter = db["counters"].find_one_and_update(
        {"_id": "order_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,
    )
    return counter["seq"]

def insert_order_item(food_item, quantity, order_id, session_id):
    item = get_item(food_item)
    if not item:
        return -1
    price = float(item["price"])
    orders_col.insert_one({
        "order_id":    order_id,
        "session_id":  session_id,
        "item_name":   food_item,
        "quantity":    int(quantity),
        "unit_price":  price,
        "total_price": price * int(quantity),
        "timestamp":   datetime.utcnow(),
    })
    decrement_stock(food_item, int(quantity))
    return 1

def get_total_order_price(order_id):
    pipeline = [
        {"$match": {"order_id": order_id}},
        {"$group": {"_id": None, "total": {"$sum": "$total_price"}}},
    ]
    result = list(orders_col.aggregate(pipeline))
    return round(result[0]["total"], 2) if result else 0

def save_order_to_history(order_id, session_id, items, total):
    history_col.insert_one({
        "order_id":   order_id,
        "session_id": session_id,
        "items":      items,
        "total":      total,
        "placed_at":  datetime.utcnow(),
        "status":     "in progress",
        "rated":      False,
    })

def get_order_history(session_id: str, limit: int = 10):
    return list(
        history_col.find({"session_id": session_id}, {"_id": 0})
                   .sort("placed_at", DESCENDING).limit(limit)
    )

def get_last_order(session_id: str):
    return history_col.find_one(
        {"session_id": session_id}, {"_id": 0},
        sort=[("placed_at", DESCENDING)]
    )


# ── Tracking ──────────────────────────────────────────────────────────────────

STATUSES = ["Order Received", "Preparing", "Ready", "Out for Delivery", "Delivered"]

def insert_order_tracking(order_id, status="Order Received"):
    tracking_col.update_one(
        {"order_id": order_id},
        {"$set": {"status": status, "last_updated": datetime.utcnow(),
                  "history": [{"status": status, "time": datetime.utcnow()}]}},
        upsert=True,
    )

def get_order_status(order_id):
    r = tracking_col.find_one({"order_id": order_id}, {"_id": 0})
    return r if r else None

def advance_order_status(order_id):
    """Move order to next status step (for simulation/admin)."""
    r = tracking_col.find_one({"order_id": order_id})
    if not r:
        return None
    try:
        idx = STATUSES.index(r["status"])
        next_status = STATUSES[min(idx + 1, len(STATUSES) - 1)]
    except ValueError:
        next_status = STATUSES[1]
    tracking_col.update_one(
        {"order_id": order_id},
        {"$set": {"status": next_status, "last_updated": datetime.utcnow()},
         "$push": {"history": {"status": next_status, "time": datetime.utcnow()}}}
    )
    history_col.update_one({"order_id": order_id}, {"$set": {"status": next_status}})
    return next_status


# ── User Preferences ──────────────────────────────────────────────────────────

def get_prefs(session_id: str):
    r = prefs_col.find_one({"session_id": session_id}, {"_id": 0})
    return r if r else {"session_id": session_id, "allergies": [], "preferences": [], "name": ""}

def save_prefs(session_id: str, data: dict):
    prefs_col.update_one({"session_id": session_id}, {"$set": data}, upsert=True)


# ── Ratings ───────────────────────────────────────────────────────────────────

def save_rating(order_id, session_id, rating, comment=""):
    ratings_col.update_one(
        {"order_id": order_id},
        {"$set": {"session_id": session_id, "rating": rating,
                  "comment": comment, "rated_at": datetime.utcnow()}},
        upsert=True
    )
    history_col.update_one({"order_id": order_id}, {"$set": {"rated": True, "rating": rating}})


# ── Admin ─────────────────────────────────────────────────────────────────────

def get_admin_stats():
    total_orders   = history_col.count_documents({})
    total_revenue  = list(history_col.aggregate([{"$group": {"_id": None, "t": {"$sum": "$total"}}}]))
    revenue        = round(total_revenue[0]["t"], 2) if total_revenue else 0
    today          = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_orders   = history_col.count_documents({"placed_at": {"$gte": today}})
    today_rev_agg  = list(history_col.aggregate([
        {"$match": {"placed_at": {"$gte": today}}},
        {"$group": {"_id": None, "t": {"$sum": "$total"}}}
    ]))
    today_revenue  = round(today_rev_agg[0]["t"], 2) if today_rev_agg else 0

    top_items = list(food_col.find({}, {"_id": 0, "name": 1, "orders": 1, "category": 1})
                              .sort("orders", DESCENDING).limit(10))
    low_stock = get_low_stock_items(10)
    recent    = list(history_col.find({}, {"_id": 0}).sort("placed_at", DESCENDING).limit(20))

    avg_rating_agg = list(ratings_col.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$rating"}}}]))
    avg_rating     = round(avg_rating_agg[0]["avg"], 1) if avg_rating_agg else 0

    return {
        "total_orders": total_orders,
        "total_revenue": revenue,
        "today_orders": today_orders,
        "today_revenue": today_revenue,
        "top_items": top_items,
        "low_stock": low_stock,
        "recent_orders": recent,
        "avg_rating": avg_rating,
    }
