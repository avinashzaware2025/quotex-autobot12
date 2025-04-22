from quotexapi.stable import Quotex

class QuotexBot(Quotex):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.connect()
        self.check_connect()

    def check_connect(self):
        if self.check_connect():
            print("✅ Login Successful")
        else:
            print("❌ Login Failed")

    def get_all_profit(self):
        data = self.get_profile()
        assets = data["balances"][0]["balances"]
        result = {}
        for a in assets:
            if "profit_percentage" in a and a["profit_percentage"] >= 80:
                result[a["symbol"]] = a["profit_percentage"]
        return result

    def place_real_trade(self, pair, direction, amount, duration=5):
        """
        Quotex वर DEMO balance वापरून real trade टाकतो.
        direction: 'buy' किंवा 'sell'
        amount: INR मध्ये
        duration: trade duration (minutes)
        """
        self.change_asset(pair)
        is_successful, trade_id = self.buy(amount, direction, duration)
        if is_successful:
            print(f"✅ Trade placed: {direction.upper()} ₹{amount} on {pair}")
            return True
        else:
            print(f"❌ Trade failed on {pair}")
            return False
