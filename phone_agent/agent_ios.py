"""Backward-compatible import path for iOS agent classes.

Prefer importing from `phone_agent.ios`.
"""

from phone_agent.ios.agent import IOSAgentConfig, IOSPhoneAgent

__all__ = ["IOSPhoneAgent", "IOSAgentConfig"]

