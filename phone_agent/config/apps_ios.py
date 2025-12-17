"""Backward-compatible import path for iOS app bundle id mapping.

Prefer importing from `phone_agent.ios.apps`.
"""

from phone_agent.ios.apps import (  # noqa: F401
    APP_PACKAGES_IOS,
    check_app_installed,
    get_bundle_id,
    get_app_info_by_id,
    get_app_info_from_itunes,
    get_app_name,
    list_supported_apps,
)

__all__ = [
    "APP_PACKAGES_IOS",
    "check_app_installed",
    "get_bundle_id",
    "get_app_name",
    "get_app_info_from_itunes",
    "get_app_info_by_id",
    "list_supported_apps",
]
