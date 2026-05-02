import re
from fuzzywuzzy import process

MENU_ITEMS = [
    # Breakfast
    "Masala Dosa", "Plain Dosa", "Rava Dosa", "Onion Dosa", "Set Dosa",
    "Idli Sambar", "Medu Vada", "Pongal", "Upma", "Poha",
    "Aloo Paratha", "Stuffed Paratha", "Chole Bhature", "Poori Bhaji",
    "Bread Omelette", "Egg Bhurji", "Pesarattu", "Akki Roti",
    # Lunch
    "Veg Thali", "Non-Veg Thali", "Rajma Rice", "Dal Makhani Rice",
    "Paneer Butter Masala", "Palak Paneer", "Chicken Curry",
    "Mutton Curry", "Fish Curry", "Vegetable Biryani",
    "Chicken Biryani", "Mutton Biryani", "Egg Fried Rice",
    "Veg Fried Rice", "Noodles", "Chapati Dal",
    # Dinner
    "Butter Naan", "Garlic Naan", "Tandoori Roti", "Kadai Paneer",
    "Shahi Paneer", "Butter Chicken", "Prawn Masala", "Dal Tadka",
    "Matar Paneer", "Aloo Gobi", "Baingan Bharta",
    # Snacks
    "Samosa", "Pav Bhaji", "Vada Pav", "Bhel Puri", "Pani Puri",
    "Sev Puri", "Dahi Puri", "Aloo Tikki", "Kachori", "Spring Roll",
    "Chicken 65", "Gobi Manchurian", "Paneer Tikka",
    # Juices & Drinks
    "Mango Lassi", "Sweet Lassi", "Masala Chai", "Filter Coffee",
    "Fresh Lime Soda", "Coconut Water", "Mango Juice", "Watermelon Juice",
    "Orange Juice", "Sugarcane Juice",
    # Desserts
    "Gulab Jamun", "Rasgulla", "Kheer", "Ice Cream",
    "Jalebi", "Halwa"
]


def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(v)} × {k}" for k, v in food_dict.items()])


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    return match.group(1) if match else ""


def fuzzy_match_item(query: str, threshold: int = 70):
    """Match a food item name using fuzzy string matching."""
    result = process.extractOne(query, MENU_ITEMS)
    if result and result[1] >= threshold:
        return result[0]
    return None


def parse_food_items_from_text(text: str):
    """Extract food items from free-form text using fuzzy matching."""
    found = {}
    words = text.lower().split()
    # Try word-number pairs and multi-word spans
    number_words = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'a': 1, 'an': 1
    }
    # Build spans of 1-4 words, try to match each
    for span_len in range(4, 0, -1):
        for i in range(len(words)):
            span = " ".join(words[i:i+span_len])
            match = fuzzy_match_item(span.title(), threshold=80)
            if match and match not in found:
                # Look for a number before this span
                qty = 1
                if i > 0:
                    prev = words[i-1]
                    if prev.isdigit():
                        qty = int(prev)
                    elif prev in number_words:
                        qty = number_words[prev]
                found[match] = qty
    return found
