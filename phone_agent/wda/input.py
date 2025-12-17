"""Backward-compatible import path for WDA input helpers."""

from phone_agent.ios.wda.input import (  # noqa: F401
    clear_text,
    hide_keyboard,
    type_text,
)

__all__ = ["type_text", "clear_text", "hide_keyboard"]

