from quotexapi.stable_api import Quotex
import pandas as pd
from finta import TA

# ========== STEP 1: LOGIN ==========
q = Quotex(email="truptiauti2001@gmail.com", password="Samarth@123")

if q.login():
    print("✅ Login Successful")
else:
    print("❌ Login Failed")
    exit()

# ========== STEP 2: LIVE 80%+ PAIRS ==========
def get_live_pairs_with_high_profit():
    # NOTE: Replace with real API when available
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

selected_pairs = get_live_pairs_with_high_profit()
print("🟢 80%+ Live Trading Pairs:")
for pair in selected_pairs:
    print(f"🔹 {pair['symbol']} ({pair['profit']}%)")

# ========== STEP 3: EMA SIGNAL ==========
def get_ema_signal(candles):
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df["EMA9"] = TA.EMA(df, 9)
    df["EMA21"] = TA.EMA(df, 21)

    if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1]:
        return "BUY"
    elif df["EMA9"].iloc[-1] < df["EMA21"].iloc[-1]:
        return "SELL"
    else:
        return "WAIT"

# ========== STEP 4: MACD + RSI SIGNAL ==========
def get_macd_rsi_signal(candles):
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

    macd_df = TA.MACD(df)
    df["MACD"] = macd_df["MACD"]
    df["SIGNAL"] = macd_df["SIGNAL"]
    df["RSI"] = TA.RSI(df)

    last_macd = df["MACD"].iloc[-1]
    last_signal = df["SIGNAL"].iloc[-1]
    last_rsi = df["RSI"].iloc[-1]

    if last_macd > last_signal and last_rsi < 70:
        return "BUY"
    elif last_macd < last_signal and last_rsi > 30:
        return "SELL"
    else:
        return "WAIT"

# ========== STEP 5: TEST WITH SAMPLE CANDLES ==========
candles = [
    [1, 1.1234, 1.1240, 1.1220, 1.1235, 1000],
    [2, 1.1235, 1.1250, 1.1230, 1.1245, 1200],
    [3, 1.1245, 1.1260, 1.1240, 1.1255, 1100],
    [4, 1.1255, 1.1270, 1.1250, 1.1265, 1300],
    [5, 1.1265, 1.1280, 1.1260, 1.1275, 1150],
    [6, 1.1275, 1.1290, 1.1270, 1.1285, 1400],
    [7, 1.1285, 1.1300, 1.1280, 1.1295, 1450],
    [8, 1.1295, 1.1310, 1.1290, 1.1305, 1500],
    [9, 1.1305, 1.1320, 1.1300, 1.1315, 1600],
    [10, 1.1315, 1.1330, 1.1310, 1.1325, 1550],
]

ema_signal = get_ema_signal(candles)
macd_rsi_signal = get_macd_rsi_signal(candles)

print(f"📊 EMA Signal: {ema_signal}")
print(f"📊 MACD + RSI Signal: {macd_rsi_signal}")

if ema_signal == macd_rsi_signal and ema_signal != "WAIT":
    print(f"🚀 Final Signal: {ema_signal} ✅ CONFIRMED by EMA + MACD + RSI")
else:
    print(f"⚠️ Signals not aligned – EMA: {ema_signal}, MACD+RSI: {macd_rsi_signal}")
