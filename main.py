from stable_api import Quotex
import time

email = "truptiauti2001@gmail.com"
password = "Samarth@123"

q = Quotex(email, password)
if q.login():
    print("✅ Login Successful")

    pairs = q.get_all_profit()
    active_pairs = [pair for pair, info in pairs.items() if info['profit'] >= 80 and info['open'] == 1]

    print("🟢 80%+ Live Trading Pairs:")
    for pair in active_pairs:
        print(f"🔹 {pair} ({pairs[pair]['profit']}%)")

    for pair in active_pairs:
        ema_signal = q.get_ema_signal(pair)
        macd_rsi_signal = q.get_macd_rsi_signal(pair)
        candle_signal = q.get_candle_pattern(pair)

        print(f"\n📈 {pair}")
        print(f"📊 EMA Signal: {ema_signal}")
        print(f"📊 MACD + RSI Signal: {macd_rsi_signal}")
        print(f"📊 Candlestick Pattern: {candle_signal}")

        if ema_signal == macd_rsi_signal == candle_signal:
            final_signal = ema_signal
            print(f"✅ FINAL SIGNAL: {final_signal}")
            # याठिकाणी तुमचं trade execution logic टाकता येईल (q.buy/q.sell)
        else:
            print(f"⚠️ Signals not aligned – EMA: {ema_signal}, MACD+RSI: {macd_rsi_signal}, Candle: {candle_signal}")
else:
    print("❌ Login failed")
