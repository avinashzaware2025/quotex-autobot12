from quotexapi.stable_api import Quotex

# ====== STEP 1: LOGIN ======
q = Quotex(email="truptiauti2001@gmail.com", password="Samarth@123")

if q.login():
    print("✅ Login Successful")
else:
    print("❌ Login Failed")

# ====== STEP 2: LIVE PAIRS + 80% PROFIT FILTER ======
def get_live_pairs_with_high_profit():
    # Dummy data - इथे नंतर Quotex API वापरून live data आणू
    all_pairs = [
        {"symbol": "EURUSD", "profit": 82, "status": "live"},
        {"symbol": "GBPUSD", "profit": 78, "status": "closed"},
        {"symbol": "USDJPY", "profit": 85, "status": "live"},
        {"symbol": "AUDUSD", "profit": 90, "status": "live"},
        {"symbol": "EURJPY", "profit": 75, "status": "live"},
        {"symbol": "GBPJPY", "profit": 80, "status": "live"},
    ]

    filtered = [pair for pair in all_pairs if pair["status"] == "live" and pair["profit"] >= 80]
    return filtered

# ====== STEP 3: PRINT FILTERED PAIRS ======
selected_pairs = get_live_pairs_with_high_profit()
print("🟢 80%+ Live Trading Pairs:")
for pair in selected_pairs:
    print(f"🔹 {pair['symbol']} ({pair['profit']}%)")

