import time
import os
from stable_api import Quotex

email = "truptiauti2001@gmail.com"
password = "Samarth@123"

q = Quotex(email, password)

if q.login():
    print("✅ Login Successful")

    pairs_data = q.get_all_profit()
    live_pairs = {k: v for k, v in pairs_data.items() if v['profit'] >= 80 and v['open'] == 1}

    print("🟢 80%+ Live Trading Pairs:")
    for pair in live_pairs:
        print(f"🔹 {pair} ({pairs_data[pair]['profit']}%)")

    initial_amount = 70
    martingale_levels = [70, 160, 350, 800]
    total_profit = 0
    total_loss = 0
    max_profit = 1000
    max_loss = 500

    for pair in live_pairs:
        print(f"\n📈 {pair}")

        ema_signal = q.get_ema_signal(pair)
        macd_rsi_signal = q.get_macd_rsi_signal(pair)
        candle_signal = q.get_candle_pattern(pair)

        print(f"📊 EMA Signal: {ema_signal}")
        print(f"📊 MACD + RSI Signal: {macd_rsi_signal}")
        print(f"📊 Candlestick Pattern: {candle_signal}")

        if ema_signal == macd_rsi_signal == candle_signal and ema_signal in ["BUY", "SELL"]:
            print(f"✅ FINAL SIGNAL: {ema_signal}")

            # Execute Martingale Strategy
            for step, amount in enumerate(martingale_levels):
                print(f"🔄 Step {step+1} – Placing {ema_signal} trade of ₹{amount} on {pair}")

                # simulate result (use real API in production)
                result = q.mock_trade_result(pair, ema_signal)  # WIN / LOSS

                if result == "WIN":
                    profit = int(amount * 0.8)
                    total_profit += profit
                    print(f"✅ Trade WON: +₹{profit} (Total Profit: ₹{total_profit})")
                    break
                else:
                    total_loss += amount
                    print(f"❌ Trade LOST: -₹{amount} (Total Loss: ₹{total_loss})")
                    if total_loss >= max_loss:
                        print("🛑 STOP: Max Loss Limit Reached.")
                        exit()
            if total_profit >= max_profit:
                print("🎉 STOP: Profit Target Achieved.")
                break
        else:
            print(f"⚠️ Signals not aligned – EMA: {ema_signal}, MACD+RSI: {macd_rsi_signal}, Candle: {candle_signal}")
else:
    print("❌ Login Failed")
