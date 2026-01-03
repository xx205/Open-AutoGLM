"""WebDriverAgent (WDA) utilities for iOS device interaction."""

from phone_agent.ios.wda.connection import (
    WDAConnection,
    quick_connect,
)
from phone_agent.ios.wda.device import (
    back,
    double_tap,
    get_current_app,
    home,
    launch_app,
    long_press,
    swipe,
    tap,
)
from phone_agent.ios.wda.input import (
    clear_text,
    type_text,
)
from phone_agent.ios.wda.screenshot import get_screenshot

__all__ = [
    # Screenshot
    "get_screenshot",
    # Input
    "type_text",
    "clear_text",
    # Device control
    "get_current_app",
    "tap",
    "swipe",
    "back",
    "home",
    "double_tap",
    "long_press",
    "launch_app",
    # Connection management
    "WDAConnection",
    "quick_connect",
]
