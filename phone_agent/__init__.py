"""
Phone Agent - An AI-powered phone automation framework.

This package provides tools for automating Android and iOS phone interactions
using AI models for visual understanding and decision making.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

__version__ = "0.1.0"
__all__ = ["PhoneAgent", "IOSPhoneAgent"]

if TYPE_CHECKING:
    from phone_agent.agent import PhoneAgent
    from phone_agent.ios.agent import IOSPhoneAgent


def __getattr__(name: str):
    if name == "PhoneAgent":
        from phone_agent.agent import PhoneAgent  # noqa: WPS433

        return PhoneAgent
    if name == "IOSPhoneAgent":
        from phone_agent.ios.agent import IOSPhoneAgent  # noqa: WPS433

        return IOSPhoneAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
