# 🍽️ IQ Restaurant — Full Stack Food Ordering App

A real-world AI-powered food ordering system with 60+ dishes, voice ordering, live tracking, admin dashboard and more.

## Tech Stack
- **Backend:** Python 3.9+ · FastAPI · MongoDB
- **Frontend:** HTML5 · CSS3 · Vanilla JS
- **AI/NLP:** Fuzzy matching · Web Speech API · TTS
- **DB:** MongoDB (database: `iqrestaurant`)

---

## Folder Structure
```
IQRestaurant/
├── backend/
│   ├── main.py            ← FastAPI server (all routes)
│   ├── db_mongo.py        ← MongoDB helpers
│   ├── nlp_utils.py       ← Fuzzy NLP + item parsing
│   ├── seed_mongo.py      ← Seeds 60 menu items
│   └── requirements.txt
└── frontend/
    ├── home.html          ← Main customer site
    ├── styles.css         ← Full stylesheet
    └── admin.html         ← Admin dashboard
```

---

## Setup & Run

### 1. Start MongoDB
```cmd
# Windows (run as Admin):
net start MongoDB

# Verify:
mongosh
```

### 2. Install Python Dependencies
```cmd
cd IQRestaurant/backend
pip install -r requirements.txt
```

### 3. Seed the Database
```cmd
python seed_mongo.py
```
Expected output:
```
✅ Seeded 63 menu items into 'iqrestaurant' database.
   Breakfast: 14 items
   Lunch: 15 items
   Dinner: 11 items
   Snacks: 9 items
   Drinks: 9 items
   Desserts: 6 items
```

### 4. Start Backend
```cmd
python -m uvicorn main:app --reload
```
Visit http://localhost:8000/health to verify.

### 5. Open Frontend
Double-click `frontend/home.html` in File Explorer.

### 6. Open Admin Dashboard
Double-click `frontend/admin.html`
- **Username:** admin
- **Password:** admin123

---

## Features

| Feature | Details |
|---|---|
| 🍽️ 60+ Dishes | Breakfast, Lunch, Dinner, Snacks, Drinks, Desserts |
| 🎤 Voice Ordering | Web Speech API · Indian English (en-IN) |
| 🔊 TTS Bot Replies | Bot speaks every response aloud |
| 🔍 Fuzzy Matching | "Biriyani" → "Chicken Biryani" auto-matched |
| 🗣️ Wake Word | Say "Hey DineBot" to open chat hands-free |
| 🔇 Noise Indicator | Visual mic level + noisy environment warning |
| 🛒 Animated Cart | Live cart sidebar with +/- qty controls |
| ✅❌ Confirm/Cancel | Action buttons after every order update |
| 📦 Live Tracking | Auto-polls every 15s for status updates |
| ⏱️ Delivery ETA | Estimated time shown after order placed |
| 💳 UPI QR | Payment QR shown after order confirmation |
| 📋 Order History | Past orders with reorder + rate buttons |
| ♻️ Repeat Order | "Repeat my last order" restores previous cart |
| 🌿 Allergy Filter | Set allergies — those items auto-skipped |
| ⭐ Customer Ratings | Rate order after delivery (1–5 stars + comment) |
| 🔥 Popularity Badges | Bestseller / Popular / New badges on menu cards |
| 🔎 Menu Search | Search by name, tag, or category |
| 🟢 Veg Filter | One-click veg-only menu filter |
| 📊 Admin Dashboard | Stats, top items, live orders, ratings |
| ⚠️ Low Stock Alerts | Critical stock warnings in admin panel |
| 🔄 Order Advance | Admin can advance order status step by step |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /menu | All 60+ menu items |
| POST | /chat | Main chat + order handler |
| GET | /status/{id} | Order tracking status |
| GET | /admin/stats | Full admin stats |
| POST | /admin/advance/{id} | Advance order status |
| GET | /admin/low-stock | Low stock items |

---

## Chat Intent Reference

| What you say | Intent triggered |
|---|---|
| "Add 2 Chicken Biryani" | add |
| "Remove Samosa" | remove |
| "Confirm" / "Place order" | confirm |
| "Cancel" | cancel |
| "Track order 5" | track |
| "Show my history" | history |
| "Repeat my last order" | repeat |
| "Show my cart" | cart |

---

## 3 Terminals Needed

| Terminal | Command |
|---|---|
| 1 | `mongosh` (keep open) |
| 2 | `cd backend` → `python -m uvicorn main:app --reload` |
| 3 | Open `frontend/home.html` in Chrome/Edge |

