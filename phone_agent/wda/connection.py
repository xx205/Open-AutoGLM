"""Backward-compatible import path for WDA connection helpers."""

from phone_agent.ios.wda.connection import WDAConnection, quick_connect

__all__ = ["WDAConnection", "quick_connect"]

