import unittest

from bot.client import BinanceFuturesClient


class ClientTests(unittest.TestCase):
    def test_signature_matches_known_hmac(self):
        client = BinanceFuturesClient(
            api_key="key",
            api_secret="secret",
            base_url="https://testnet.binancefuture.com",
        )

        signature = client._sign({"symbol": "BTCUSDT", "timestamp": 1})

        self.assertEqual(
            signature,
            "ef9d3d77a34d9a13a21a4c2d7f3e8cb091888a74ca62b5b62f430e78eded95ba",
        )


if __name__ == "__main__":
    unittest.main()
