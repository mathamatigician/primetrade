"""Order orchestration helpers."""

from __future__ import annotations

from typing import Any

from bot.client import BinanceFuturesClient
from bot.validators import validate_order_input


def build_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None = None,
) -> dict[str, str]:
    return validate_order_input(symbol, side, order_type, quantity, price)


def place_order(client: BinanceFuturesClient, order: dict[str, str]) -> dict[str, Any]:
    return client.place_order(order)

