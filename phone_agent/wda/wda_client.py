"""Backward-compatible import path for the WDA HTTP client."""

from phone_agent.ios.wda.wda_client import WDAClient, WDAError, WDAHTTPError

__all__ = ["WDAClient", "WDAError", "WDAHTTPError"]

