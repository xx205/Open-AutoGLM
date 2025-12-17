"""Backward-compatible import path for WDA screenshot helpers."""

from phone_agent.ios.wda.screenshot import Screenshot, get_screenshot, get_screenshot_png, save_screenshot

__all__ = ["Screenshot", "get_screenshot", "get_screenshot_png", "save_screenshot"]

