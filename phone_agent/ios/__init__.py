"""iOS backend (WebDriverAgent/WDA) support for Phone Agent.

This package is kept import-light to avoid circular imports (e.g. when
`phone_agent.config` needs iOS app metadata).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from phone_agent.ios.agent import IOSAgentConfig, IOSPhoneAgent

__all__ = ["IOSPhoneAgent", "IOSAgentConfig"]


def __getattr__(name: str):
    if name == "IOSPhoneAgent":
        from phone_agent.ios.agent import IOSPhoneAgent  # noqa: WPS433

        return IOSPhoneAgent
    if name == "IOSAgentConfig":
        from phone_agent.ios.agent import IOSAgentConfig  # noqa: WPS433

        return IOSAgentConfig
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

