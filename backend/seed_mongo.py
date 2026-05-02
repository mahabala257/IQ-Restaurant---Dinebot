from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "iqrestaurant"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

MENU = [
    # ── Breakfast ──
    {"name": "Masala Dosa",      "category": "Breakfast", "price": 80,  "veg": True,  "tags": ["spicy","crispy"],       "emoji": "🫓", "stock": 50, "orders": 320, "badge": "bestseller"},
    {"name": "Plain Dosa",       "category": "Breakfast", "price": 60,  "veg": True,  "tags": ["light","crispy"],       "emoji": "🫓", "stock": 50, "orders": 210, "badge": ""},
    {"name": "Rava Dosa",        "category": "Breakfast", "price": 90,  "veg": True,  "tags": ["crispy","onion"],       "emoji": "🫓", "stock": 40, "orders": 180, "badge": ""},
    {"name": "Onion Dosa",       "category": "Breakfast", "price": 75,  "veg": True,  "tags": ["crispy","onion"],       "emoji": "🫓", "stock": 40, "orders": 130, "badge": ""},
    {"name": "Set Dosa",         "category": "Breakfast", "price": 70,  "veg": True,  "tags": ["soft","light"],         "emoji": "🫓", "stock": 40, "orders": 100, "badge": ""},
    {"name": "Idli Sambar",      "category": "Breakfast", "price": 60,  "veg": True,  "tags": ["steamed","healthy"],    "emoji": "🍚", "stock": 60, "orders": 290, "badge": "bestseller"},
    {"name": "Medu Vada",        "category": "Breakfast", "price": 50,  "veg": True,  "tags": ["crispy","fried"],       "emoji": "🍩", "stock": 50, "orders": 200, "badge": ""},
    {"name": "Pongal",           "category": "Breakfast", "price": 70,  "veg": True,  "tags": ["soft","comfort"],       "emoji": "🍚", "stock": 30, "orders": 150, "badge": ""},
    {"name": "Upma",             "category": "Breakfast", "price": 55,  "veg": True,  "tags": ["light","semolina"],     "emoji": "🍚", "stock": 30, "orders": 90,  "badge": ""},
    {"name": "Poha",             "category": "Breakfast", "price": 50,  "veg": True,  "tags": ["light","flattened"],    "emoji": "🍚", "stock": 40, "orders": 110, "badge": ""},
    {"name": "Aloo Paratha",     "category": "Breakfast", "price": 90,  "veg": True,  "tags": ["stuffed","filling"],    "emoji": "🫓", "stock": 35, "orders": 175, "badge": ""},
    {"name": "Chole Bhature",    "category": "Breakfast", "price": 120, "veg": True,  "tags": ["spicy","filling"],      "emoji": "🍛", "stock": 30, "orders": 220, "badge": "popular"},
    {"name": "Bread Omelette",   "category": "Breakfast", "price": 70,  "veg": False, "tags": ["egg","quick"],          "emoji": "🍳", "stock": 40, "orders": 130, "badge": ""},
    {"name": "Egg Bhurji",       "category": "Breakfast", "price": 80,  "veg": False, "tags": ["egg","spicy"],          "emoji": "🍳", "stock": 40, "orders": 145, "badge": ""},
    # ── Lunch ──
    {"name": "Veg Thali",        "category": "Lunch",     "price": 180, "veg": True,  "tags": ["complete","value"],     "emoji": "🍱", "stock": 25, "orders": 380, "badge": "bestseller"},
    {"name": "Non-Veg Thali",    "category": "Lunch",     "price": 250, "veg": False, "tags": ["complete","value"],     "emoji": "🍱", "stock": 20, "orders": 310, "badge": "bestseller"},
    {"name": "Dal Makhani Rice", "category": "Lunch",     "price": 160, "veg": True,  "tags": ["creamy","comfort"],     "emoji": "🍛", "stock": 30, "orders": 195, "badge": "popular"},
    {"name": "Paneer Butter Masala","category":"Lunch",   "price": 200, "veg": True,  "tags": ["creamy","rich"],        "emoji": "🧀", "stock": 30, "orders": 260, "badge": "popular"},
    {"name": "Palak Paneer",     "category": "Lunch",     "price": 190, "veg": True,  "tags": ["healthy","spinach"],    "emoji": "🥬", "stock": 25, "orders": 170, "badge": ""},
    {"name": "Chicken Curry",    "category": "Lunch",     "price": 220, "veg": False, "tags": ["spicy","protein"],      "emoji": "🍗", "stock": 30, "orders": 290, "badge": "popular"},
    {"name": "Mutton Curry",     "category": "Lunch",     "price": 280, "veg": False, "tags": ["rich","slow-cooked"],   "emoji": "🍖", "stock": 20, "orders": 210, "badge": ""},
    {"name": "Fish Curry",       "category": "Lunch",     "price": 240, "veg": False, "tags": ["coastal","tangy"],      "emoji": "🐟", "stock": 25, "orders": 180, "badge": ""},
    {"name": "Vegetable Biryani","category": "Lunch",     "price": 180, "veg": True,  "tags": ["aromatic","rice"],      "emoji": "🍚", "stock": 30, "orders": 240, "badge": "popular"},
    {"name": "Chicken Biryani",  "category": "Lunch",     "price": 250, "veg": False, "tags": ["aromatic","rice"],      "emoji": "🍗", "stock": 30, "orders": 410, "badge": "bestseller"},
    {"name": "Egg Fried Rice",   "category": "Lunch",     "price": 140, "veg": False, "tags": ["quick","rice"],         "emoji": "🍳", "stock": 40, "orders": 200, "badge": ""},
    {"name": "Veg Fried Rice",   "category": "Lunch",     "price": 120, "veg": True,  "tags": ["quick","rice"],         "emoji": "🍚", "stock": 40, "orders": 160, "badge": ""},
    {"name": "Chapati Dal",      "category": "Lunch",     "price": 100, "veg": True,  "tags": ["simple","healthy"],     "emoji": "🫓", "stock": 40, "orders": 120, "badge": ""},
    {"name": "Rajma Rice",       "category": "Lunch",     "price": 150, "veg": True,  "tags": ["protein","comfort"],    "emoji": "🍛", "stock": 30, "orders": 140, "badge": ""},
    # ── Dinner ──
    {"name": "Butter Naan",      "category": "Dinner",    "price": 40,  "veg": True,  "tags": ["bread","soft"],         "emoji": "🫓", "stock": 60, "orders": 350, "badge": "bestseller"},
    {"name": "Garlic Naan",      "category": "Dinner",    "price": 50,  "veg": True,  "tags": ["bread","garlic"],       "emoji": "🫓", "stock": 60, "orders": 300, "badge": "popular"},
    {"name": "Kadai Paneer",     "category": "Dinner",    "price": 210, "veg": True,  "tags": ["spicy","rich"],         "emoji": "🧀", "stock": 25, "orders": 230, "badge": "popular"},
    {"name": "Shahi Paneer",     "category": "Dinner",    "price": 220, "veg": True,  "tags": ["creamy","royal"],       "emoji": "🧀", "stock": 20, "orders": 190, "badge": ""},
    {"name": "Butter Chicken",   "category": "Dinner",    "price": 260, "veg": False, "tags": ["creamy","mild"],        "emoji": "🍗", "stock": 30, "orders": 380, "badge": "bestseller"},
    {"name": "Prawn Masala",     "category": "Dinner",    "price": 320, "veg": False, "tags": ["seafood","spicy"],      "emoji": "🦐", "stock": 15, "orders": 160, "badge": ""},
    {"name": "Dal Tadka",        "category": "Dinner",    "price": 130, "veg": True,  "tags": ["comfort","smoky"],      "emoji": "🍛", "stock": 40, "orders": 175, "badge": ""},
    {"name": "Baingan Bharta",   "category": "Dinner",    "price": 160, "veg": True,  "tags": ["smoky","roasted"],      "emoji": "🍆", "stock": 20, "orders": 100, "badge": ""},
    {"name": "Tandoori Roti",    "category": "Dinner",    "price": 30,  "veg": True,  "tags": ["bread","clay-oven"],    "emoji": "🫓", "stock": 60, "orders": 270, "badge": ""},
    {"name": "Mutton Biryani",   "category": "Dinner",    "price": 320, "veg": False, "tags": ["aromatic","rich"],      "emoji": "🍖", "stock": 20, "orders": 290, "badge": "popular"},
    # ── Snacks ──
    {"name": "Samosa",           "category": "Snacks",    "price": 20,  "veg": True,  "tags": ["crispy","tea-time"],    "emoji": "🔺", "stock": 80, "orders": 450, "badge": "bestseller"},
    {"name": "Pav Bhaji",        "category": "Snacks",    "price": 120, "veg": True,  "tags": ["buttery","street"],     "emoji": "🍞", "stock": 40, "orders": 310, "badge": "popular"},
    {"name": "Vada Pav",         "category": "Snacks",    "price": 30,  "veg": True,  "tags": ["spicy","street"],       "emoji": "🍔", "stock": 60, "orders": 280, "badge": "popular"},
    {"name": "Bhel Puri",        "category": "Snacks",    "price": 60,  "veg": True,  "tags": ["tangy","crunchy"],      "emoji": "🥣", "stock": 50, "orders": 190, "badge": ""},
    {"name": "Pani Puri",        "category": "Snacks",    "price": 60,  "veg": True,  "tags": ["tangy","street"],       "emoji": "🫧", "stock": 50, "orders": 240, "badge": "popular"},
    {"name": "Aloo Tikki",       "category": "Snacks",    "price": 60,  "veg": True,  "tags": ["crispy","potato"],      "emoji": "🥔", "stock": 50, "orders": 160, "badge": ""},
    {"name": "Chicken 65",       "category": "Snacks",    "price": 180, "veg": False, "tags": ["spicy","fried"],        "emoji": "🍗", "stock": 35, "orders": 290, "badge": "popular"},
    {"name": "Gobi Manchurian",  "category": "Snacks",    "price": 140, "veg": True,  "tags": ["indo-chinese","crispy"],"emoji": "🥦", "stock": 35, "orders": 210, "badge": ""},
    {"name": "Paneer Tikka",     "category": "Snacks",    "price": 200, "veg": True,  "tags": ["grilled","smoky"],      "emoji": "🧀", "stock": 25, "orders": 250, "badge": "popular"},
    {"name": "Spring Roll",      "category": "Snacks",    "price": 100, "veg": True,  "tags": ["crispy","indo-chinese"],"emoji": "🌯", "stock": 40, "orders": 130, "badge": ""},
    # ── Juices & Drinks ──
    {"name": "Mango Lassi",      "category": "Drinks",    "price": 80,  "veg": True,  "tags": ["sweet","cooling"],      "emoji": "🥭", "stock": 50, "orders": 300, "badge": "bestseller"},
    {"name": "Sweet Lassi",      "category": "Drinks",    "price": 60,  "veg": True,  "tags": ["sweet","dairy"],        "emoji": "🥛", "stock": 50, "orders": 180, "badge": ""},
    {"name": "Masala Chai",      "category": "Drinks",    "price": 30,  "veg": True,  "tags": ["hot","spiced"],         "emoji": "☕", "stock": 80, "orders": 420, "badge": "bestseller"},
    {"name": "Filter Coffee",    "category": "Drinks",    "price": 40,  "veg": True,  "tags": ["hot","strong"],         "emoji": "☕", "stock": 80, "orders": 380, "badge": "popular"},
    {"name": "Fresh Lime Soda",  "category": "Drinks",    "price": 50,  "veg": True,  "tags": ["tangy","refreshing"],   "emoji": "🍋", "stock": 60, "orders": 210, "badge": ""},
    {"name": "Mango Juice",      "category": "Drinks",    "price": 70,  "veg": True,  "tags": ["sweet","fruity"],       "emoji": "🥭", "stock": 40, "orders": 190, "badge": ""},
    {"name": "Coconut Water",    "category": "Drinks",    "price": 60,  "veg": True,  "tags": ["natural","hydrating"],  "emoji": "🥥", "stock": 30, "orders": 150, "badge": "new"},
    {"name": "Watermelon Juice", "category": "Drinks",    "price": 60,  "veg": True,  "tags": ["refreshing","summer"],  "emoji": "🍉", "stock": 30, "orders": 130, "badge": "new"},
    {"name": "Sugarcane Juice",  "category": "Drinks",    "price": 40,  "veg": True,  "tags": ["natural","sweet"],      "emoji": "🌿", "stock": 30, "orders": 110, "badge": ""},
    # ── Desserts ──
    {"name": "Gulab Jamun",      "category": "Desserts",  "price": 60,  "veg": True,  "tags": ["sweet","syrupy"],       "emoji": "🟤", "stock": 50, "orders": 280, "badge": "popular"},
    {"name": "Rasgulla",         "category": "Desserts",  "price": 60,  "veg": True,  "tags": ["sweet","spongy"],       "emoji": "⚪", "stock": 50, "orders": 200, "badge": ""},
    {"name": "Kheer",            "category": "Desserts",  "price": 80,  "veg": True,  "tags": ["creamy","rice"],        "emoji": "🍮", "stock": 30, "orders": 160, "badge": ""},
    {"name": "Jalebi",           "category": "Desserts",  "price": 50,  "veg": True,  "tags": ["crispy","sweet"],       "emoji": "🌀", "stock": 40, "orders": 190, "badge": "popular"},
    {"name": "Ice Cream",        "category": "Desserts",  "price": 80,  "veg": True,  "tags": ["cold","sweet"],         "emoji": "🍦", "stock": 40, "orders": 220, "badge": ""},
    {"name": "Halwa",            "category": "Desserts",  "price": 70,  "veg": True,  "tags": ["sweet","warm"],         "emoji": "🟡", "stock": 30, "orders": 130, "badge": ""},
]


def seed():
    db["food_items"].drop()
    db["counters"].delete_many({"_id": "order_id"})

    now = datetime.utcnow()
    for item in MENU:
        item["created_at"] = now
        item["ratings"] = []
        item["avg_rating"] = 0.0
    db["food_items"].insert_many(MENU)

    # Indexes
    db["food_items"].create_index("category")
    db["food_items"].create_index("name")
    db["orders"].create_index("session_id")
    db["orders"].create_index("order_id")
    db["order_history"].create_index("session_id")
    db["order_tracking"].create_index("order_id")

    print(f"✅ Seeded {len(MENU)} menu items into '{DB_NAME}' database.")
    cats = {}
    for i in MENU:
        cats[i['category']] = cats.get(i['category'], 0) + 1
    for c, n in cats.items():
        print(f"   {c}: {n} items")


if __name__ == "__main__":
    seed()
