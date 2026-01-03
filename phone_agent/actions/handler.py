"""Action handler for processing AI model outputs."""

import time
from typing import Callable

from phone_agent.adb import (
    back,
    clear_text,
    detect_and_set_adb_keyboard,
    double_tap,
    home,
    launch_app,
    long_press,
    restore_keyboard,
    swipe,
    tap,
    type_text,
)
from phone_agent.actions.base_handler import BaseActionHandler
from phone_agent.actions.types import ActionResult
from phone_agent.config.timing import TIMING_CONFIG


class ActionHandler(BaseActionHandler):
    """
    Handles execution of actions from AI model output.

    Args:
        device_id: Optional ADB device ID for multi-device setups.
        confirmation_callback: Optional callback for sensitive action confirmation.
            Should return True to proceed, False to cancel.
        takeover_callback: Optional callback for takeover requests (login, captcha).
    """

    def __init__(
        self,
        device_id: str | None = None,
        confirmation_callback: Callable[[str], bool] | None = None,
        takeover_callback: Callable[[str], None] | None = None,
    ):
        super().__init__(
            confirmation_callback=confirmation_callback, takeover_callback=takeover_callback
        )
        self.device_id = device_id

    def _launch_app(self, app_name: str) -> bool:
        return launch_app(app_name, self.device_id)

    def _tap(self, x: int, y: int) -> None:
        tap(x, y, self.device_id)

    def _type_text(self, text: str) -> None:
        # Switch to ADB keyboard
        original_ime = detect_and_set_adb_keyboard(self.device_id)
        time.sleep(TIMING_CONFIG.action.keyboard_switch_delay)

        # Clear existing text and type new text
        clear_text(self.device_id)
        time.sleep(TIMING_CONFIG.action.text_clear_delay)

        type_text(text, self.device_id)
        time.sleep(TIMING_CONFIG.action.text_input_delay)

        # Restore original keyboard
        restore_keyboard(original_ime, self.device_id)
        time.sleep(TIMING_CONFIG.action.keyboard_restore_delay)

    def _swipe(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        swipe(start_x, start_y, end_x, end_y, device_id=self.device_id)

    def _back(self) -> None:
        back(self.device_id)

    def _home(self) -> None:
        home(self.device_id)

    def _double_tap(self, x: int, y: int) -> None:
        double_tap(x, y, self.device_id)

    def _long_press(self, x: int, y: int) -> None:
        long_press(x, y, device_id=self.device_id)
