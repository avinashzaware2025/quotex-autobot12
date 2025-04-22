import random

class QuotexBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.logged_in = False

    def login(self):
        # Dummy login simulation
        self.logged_in = True
        return self.logged_in

    def get_high_profit_pairs(self):
        # Simulated high-profit live pairs
        return {
            "EURUSD": 82,
            "USDJPY": 85,
            "AUDUSD": 90,
            "GBPJPY": 80,
        }

    def ema_signal(self, pair):
        return random.choice(["BUY", "SELL", "WAIT"])

    def macd_rsi_signal(self, pair):
        return random.choice(["BUY", "SELL", "WAIT"])

    def candlestick_signal(self, pair):
        return random.choice(["BUY", "SELL", "WAIT"])

    def place_demo_trade(self, pair, direction, amount=70):
        # Simulate trade result
        result = random.choice(["WIN", "LOSS"])
        return f"{result} – {direction} on {pair} with ₹{amount}"
