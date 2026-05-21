"""Command-line interface for the trading bot."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Any

from bot.client import BinanceAPIError, BinanceFuturesClient
from bot.config import load_settings
from bot.logging_config import setup_logging
from bot.orders import build_order, place_order

LOGGER = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Place MARKET and LIMIT orders on Binance Futures Testnet.",
    )
    parser.add_argument("--symbol", required=True, help="USDT-M symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Limit price, required for LIMIT orders")
    return parser


def print_order_summary(order: dict[str, str]) -> None:
    print("\nOrder request")
    print("-------------")
    print(f"Symbol   : {order['symbol']}")
    print(f"Side     : {order['side']}")
    print(f"Type     : {order['type']}")
    print(f"Quantity : {order['quantity']}")
    if "price" in order:
        print(f"Price    : {order['price']}")


def print_order_response(response: dict[str, Any]) -> None:
    print("\nOrder response")
    print("--------------")
    print(f"Order ID     : {response.get('orderId', 'N/A')}")
    print(f"Status       : {response.get('status', 'N/A')}")
    print(f"Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"Raw Symbol   : {response.get('symbol', 'N/A')}")


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        order = build_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print_order_summary(order)

        settings = load_settings()
        client = BinanceFuturesClient(
            api_key=settings.api_key,
            api_secret=settings.api_secret,
            base_url=settings.base_url,
        )
        response = place_order(client, order)
        print_order_response(response)
        print("\nSuccess: order submitted to Binance Futures Testnet.")
        return 0
    except ValueError as exc:
        LOGGER.error("Invalid input: %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
        return 2
    except BinanceAPIError as exc:
        LOGGER.error("Order failed: %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        LOGGER.exception("Unexpected failure")
        print(f"\nFailure: unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

