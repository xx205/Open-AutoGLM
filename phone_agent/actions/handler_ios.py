"""Backward-compatible import path for iOS action handler.

Prefer importing from `phone_agent.ios.action_handler`.
"""

from phone_agent.ios.action_handler import IOSActionHandler

__all__ = ["IOSActionHandler"]

