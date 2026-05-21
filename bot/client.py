"""Direct REST client for Binance USDT-M Futures testnet."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)


class BinanceAPIError(RuntimeError):
    """Raised when Binance returns a non-successful response."""


class BinanceFuturesClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str,
        timeout: int = 15,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _sign(self, params: dict[str, Any]) -> str:
        query = urlencode(params, doseq=True)
        return hmac.new(self.api_secret, query.encode("utf-8"), hashlib.sha256).hexdigest()

    def _post_signed(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        request_params = {
            **params,
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }
        request_params["signature"] = self._sign(request_params)

        safe_params = {key: value for key, value in request_params.items() if key != "signature"}
        LOGGER.info("POST %s params=%s", path, safe_params)

        url = f"{self.base_url}{path}?{urlencode(request_params, doseq=True)}"
        request = Request(url=url, data=b"", method="POST", headers={"X-MBX-APIKEY": self.api_key})

        try:
            with urlopen(request, timeout=self.timeout) as response:
                status_code = response.status
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            status_code = exc.code
            body = exc.read().decode("utf-8", errors="replace")
        except URLError as exc:
            LOGGER.exception("Network failure during Binance request")
            raise BinanceAPIError(f"Network failure: {exc.reason}") from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            LOGGER.error("Non-JSON Binance response status=%s text=%s", status_code, body)
            raise BinanceAPIError(f"Binance returned non-JSON response: {body}") from None

        LOGGER.info("Response status=%s body=%s", status_code, data)

        if status_code < 200 or status_code >= 300:
            message = data.get("msg", data)
            raise BinanceAPIError(f"Binance API error {status_code}: {message}")

        return data

    def place_order(self, order: dict[str, str]) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": order["symbol"],
            "side": order["side"],
            "type": order["type"],
            "quantity": order["quantity"],
        }

        if order["type"] == "LIMIT":
            params.update(
                {
                    "timeInForce": "GTC",
                    "price": order["price"],
                }
            )

        return self._post_signed("/fapi/v1/order", params)
