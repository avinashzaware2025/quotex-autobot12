import os
import time
from stable_api import QuotexBot
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("QX_EMAIL")
password = os.getenv("QX_PASSWORD")

q = QuotexBot(email, password)
if not q.login():
    print("❌ Login failed.")
    exit()

print("✅ Login Successful")

# Filter live pairs with 80%+ profit
live_pairs = q.get_high_profit_pairs()
if not live_pairs:
    print("⚠️ No high-profit live pairs found.")
    exit()

print("🟢 80%+ Live Trading Pairs:")
for pair in live_pairs:
    print(f"🔹 {pair} ({live_pairs[pair]}%)")

# Analyze each pair
for pair in live_pairs:
    print(f"📈 {pair}")
    ema = q.ema_signal(pair)
    macd_rsi = q.macd_rsi_signal(pair)
    candle = q.candlestick_signal(pair)

    print(f"📊 EMA Signal: {ema}")
    print(f"📊 MACD + RSI Signal: {macd_rsi}")
    print(f"📊 Candlestick Pattern: {candle}")

    if ema == macd_rsi == candle and ema in ["BUY", "SELL"]:
        print(f"✅ FINAL SIGNAL: {ema}")
        print(f"🔄 Placing {ema} trade of ₹70 on {pair}")
        result = q.place_demo_trade(pair, ema, amount=70)
        print(f"🎯 Trade Result: {result}")
        break
    else:
        print(f"⚠️ Signals not aligned – EMA: {ema}, MACD+RSI: {macd_rsi}, Candle: {candle}")
