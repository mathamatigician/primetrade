"""Application configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_BASE_URL = "https://testnet.binancefuture.com"


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_secret: str
    base_url: str = DEFAULT_BASE_URL


def load_settings() -> Settings:
    """Load API credentials from .env and environment variables."""
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    base_url = os.getenv("BINANCE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

    if not api_key or not api_secret:
        raise ValueError(
            "Missing Binance credentials. Add BINANCE_API_KEY and "
            "BINANCE_API_SECRET to your .env file before placing orders."
        )

    return Settings(api_key=api_key, api_secret=api_secret, base_url=base_url)
