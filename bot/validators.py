"""Input validation for order requests."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if not value:
        raise ValueError("Symbol is required.")
    if not value.endswith("USDT"):
        raise ValueError("This assignment expects a USDT-M symbol, e.g. BTCUSDT.")
    if not value.replace("USDT", "").isalnum():
        raise ValueError("Symbol must contain only letters and numbers.")
    return value


def normalize_side(side: str) -> str:
    value = side.strip().upper()
    if value not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL.")
    return value


def normalize_order_type(order_type: str) -> str:
    value = order_type.strip().upper()
    if value not in VALID_ORDER_TYPES:
        raise ValueError("Order type must be MARKET or LIMIT.")
    return value


def positive_decimal(value: str, field_name: str) -> str:
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} must be a valid number.") from None

    if decimal_value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return format(decimal_value.normalize(), "f")


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None = None,
) -> dict[str, str]:
    normalized_type = normalize_order_type(order_type)
    normalized_price = None

    if normalized_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        normalized_price = positive_decimal(price, "Price")
    elif price is not None:
        raise ValueError("Price should only be supplied for LIMIT orders.")

    order = {
        "symbol": normalize_symbol(symbol),
        "side": normalize_side(side),
        "type": normalized_type,
        "quantity": positive_decimal(quantity, "Quantity"),
    }

    if normalized_price is not None:
        order["price"] = normalized_price

    return order

