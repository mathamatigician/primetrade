import unittest

from bot.validators import validate_order_input


class ValidatorTests(unittest.TestCase):
    def test_market_order_validation(self):
        order = validate_order_input("btcusdt", "buy", "market", "0.001")

        self.assertEqual(
            order,
            {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
                "quantity": "0.001",
            },
        )

    def test_limit_order_requires_price(self):
        with self.assertRaisesRegex(ValueError, "Price is required"):
            validate_order_input("BTCUSDT", "BUY", "LIMIT", "0.001")

    def test_limit_order_validation(self):
        order = validate_order_input("BTCUSDT", "SELL", "LIMIT", "0.0010", "120000.00")

        self.assertEqual(
            order,
            {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "type": "LIMIT",
                "quantity": "0.001",
                "price": "120000",
            },
        )

    def test_rejects_price_for_market_order(self):
        with self.assertRaisesRegex(ValueError, "only be supplied"):
            validate_order_input("BTCUSDT", "BUY", "MARKET", "0.001", "100")


if __name__ == "__main__":
    unittest.main()
