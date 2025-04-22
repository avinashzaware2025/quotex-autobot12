from stable_api import QuotexBot
import ta
import pandas as pd
import time

# 📩 Login info
email = "truptiauti2001@gmail.com"
password = "Samarth@123"

q = QuotexBot(email, password)

# 🔎 Get live profitable pairs
pairs = q.get_all_profit()
print("🟢 80%+ Live Trading Pairs:")
for p, profit in pairs.items():
    print(f"🔹 {p} ({profit}%)")

# 📊 Define technical analysis function
def get_indicators(df):
    df['EMA'] = ta.trend.ema_indicator(df['close'], window=14).round(2)
    macd = ta.trend.macd(df['close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)
    return df

def get_candle_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if last['close'] > last['open'] and prev['close'] < prev['open']:
        return "BUY"
    elif last['close'] < last['open'] and prev['close'] > prev['open']:
        return "SELL"
    else:
        return "WAIT"

# 🧠 Strategy logic
def get_signals(df):
    df = get_indicators(df)
    ema_signal = "BUY" if df['close'].iloc[-1] > df['EMA'].iloc[-1] else "SELL"
    macd_rsi_signal = "BUY" if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1] and df['RSI'].iloc[-1] > 50 else "SELL"
    candle_signal = get_candle_signal(df)
    return ema_signal, macd_rsi_signal, candle_signal

# 📈 Analyze and place trade
for pair in pairs.keys():
    df = q.get_candles(pair, 5, 100)
    df = pd.DataFrame(df)
    df.columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
    ema_signal, macd_rsi_signal, candle_signal = get_signals(df)

    print(f"\n📈 {pair}")
    print(f"📊 EMA Signal: {ema_signal}")
    print(f"📊 MACD + RSI Signal: {macd_rsi_signal}")
    print(f"📊 Candlestick Pattern: {candle_signal}")

    if ema_signal == macd_rsi_signal == candle_signal:
        print(f"✅ FINAL SIGNAL: {ema_signal}")
        q.place_real_trade(pair, ema_signal.lower(), 70)
        break
    else:
        print(f"⚠️ Signals not aligned – EMA: {ema_signal}, MACD+RSI: {macd_rsi_signal}, Candle: {candle_signal}")
