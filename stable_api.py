import random

class Quotex:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        return True  # Mock login success

    def get_all_profit(self):
        # Live trading pairs with profit percent (mocked)
        return {
            "EURUSD": {"profit": 82, "open": 1},
            "USDJPY": {"profit": 85, "open": 1},
            "AUDUSD": {"profit": 90, "open": 1},
            "GBPJPY": {"profit": 80, "open": 1},
            "EURJPY": {"profit": 70, "open": 0},   # Closed, not active
            "GBPUSD": {"profit": 78, "open": 1},   # <80%, should be ignored
        }

    def get_ema_signal(self, pair):
        return random.choice(["BUY", "SELL"])

    def get_macd_rsi_signal(self, pair):
        return random.choice(["BUY", "SELL", "WAIT"])

    def get_candle_pattern(self, pair):
        return random.choice(["BUY", "SELL", "WAIT"])
