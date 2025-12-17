"""Backward-compatible import path for the iOS WebDriverAgent (WDA) backend.

Prefer importing from `phone_agent.ios.wda`.
"""

from phone_agent.ios.wda import (  # noqa: F401
    WDAConnection,
    back,
    clear_text,
    double_tap,
    get_current_app,
    get_screenshot,
    home,
    launch_app,
    long_press,
    quick_connect,
    swipe,
    tap,
    type_text,
)

__all__ = [
    "WDAConnection",
    "quick_connect",
    "get_screenshot",
    "type_text",
    "clear_text",
    "get_current_app",
    "tap",
    "swipe",
    "back",
    "home",
    "double_tap",
    "long_press",
    "launch_app",
]

