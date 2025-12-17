"""Backward-compatible import path for WDA device helpers."""

from phone_agent.ios.wda.device import (  # noqa: F401
    DEFAULT_SCREEN_SIZE,
    back,
    double_tap,
    get_current_app,
    get_screen_size,
    home,
    launch_app,
    long_press,
    press_button,
    swipe,
    tap,
)

__all__ = [
    "DEFAULT_SCREEN_SIZE",
    "get_current_app",
    "tap",
    "swipe",
    "back",
    "home",
    "double_tap",
    "long_press",
    "launch_app",
    "get_screen_size",
    "press_button",
]

