import time
import pandas as pd
from stable_api import Quotex

def get_ema_signal(closes):
    df = pd.DataFrame(closes, columns=["close"])
    df["EMA_5"] = df["close"].ewm(span=5, adjust=False).mean()
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()
    if df["EMA_5"].iloc[-1] > df["EMA_20"].iloc[-1]:
        return "BUY"
    elif df["EMA_5"].iloc[-1] < df["EMA_20"].iloc[-1]:
        return "SELL"
    else:
        return "WAIT"

def get_macd_rsi_signal(closes):
    df = pd.DataFrame(closes, columns=["close"])
    df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    if df["MACD"].iloc[-1] > df["Signal"].iloc[-1] and df["RSI"].iloc[-1] > 50:
        return "BUY"
    elif df["MACD"].iloc[-1] < df["Signal"].iloc[-1] and df["RSI"].iloc[-1] < 50:
        return "SELL"
    else:
        return "WAIT"

def get_candlestick_signal(candles):
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    if prev['close'] < prev['open'] and latest['close'] > latest['open'] and latest['close'] > prev['open'] and latest['open'] < prev['close']:
        return "BUY"
    if prev['close'] > prev['open'] and latest['close'] < latest['open'] and latest['close'] < prev['open'] and latest['open'] > prev['close']:
        return "SELL"
    body = abs(latest['close'] - latest['open'])
    candle_range = latest['high'] - latest['low']
    lower_wick = min(latest['close'], latest['open']) - latest['low']
    upper_wick = latest['high'] - max(latest['close'], latest['open'])
    if body < candle_range * 0.3 and lower_wick > upper_wick * 2:
        return "BUY"
    if body < candle_range * 0.3 and upper_wick > lower_wick * 2:
        return "SELL"
    if body < (candle_range * 0.1):
        return "WAIT"
    return "WAIT"

qx = Quotex(email="your_email", password="your_password")
qx.login()
if qx.check_connect():
    print("✅ Login Successful")
    assets = qx.get_all_profit()
    active_pairs = [k for k, v in assets.items() if v >= 80]
    print("🟢 80%+ Live Trading Pairs:")
    for p in active_pairs:
        print(f"🔹 {p} ({assets[p]}%)")

    for symbol in active_pairs:
        candles = qx.get_candles(symbol, 5, 100)
        closes = [c[4] for c in candles]
        ema_signal = get_ema_signal(closes)
        macd_rsi_signal = get_macd_rsi_signal(closes)
        candle_signal = get_candlestick_signal(candles)
        print(f"📊 EMA Signal: {ema_signal}")
        print(f"📊 MACD + RSI Signal: {macd_rsi_signal}")
        print(f"🕯️ Candlestick Pattern Signal: {candle_signal}")
        if ema_signal == macd_rsi_signal == candle_signal and ema_signal != "WAIT":
            print(f"🚀 Final Signal: {ema_signal} ✅ FULL CONFIRMATION")
        else:
            print(f"⚠️ Signals not aligned – EMA: {ema_signal}, MACD+RSI: {macd_rsi_signal}, Candle: {candle_signal}")
else:
    print("❌ Login failed")
