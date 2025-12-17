"""WebDriverAgent (WDA) connection management.

To control a device, provide a reachable WDA URL.

- Wi‑Fi (recommended): http://<device-ip>:8100
- USB: forward :8100 to this machine (then http://localhost:8100)
"""

from phone_agent.wda.wda_client import WDAClient, WDAError


class WDAConnection:
    """
    Manages a WebDriverAgent endpoint and sessions.

    The device must have WebDriverAgent running and reachable at `wda_url`.
    """

    def __init__(self, wda_url: str = "http://localhost:8100", *, verify_tls: bool = True):
        """
        Initialize WDA connection manager.

        Args:
            wda_url: WebDriverAgent URL (default: http://localhost:8100).
                     For Wi‑Fi devices, use http://<device-ip>:8100
        """
        self.wda_url = wda_url.rstrip("/")
        self._client = WDAClient(self.wda_url, verify_tls=verify_tls)

    def is_wda_ready(self, timeout: int = 2) -> bool:
        """
        Check if WebDriverAgent is running and accessible.

        Args:
            timeout: Request timeout in seconds.

        Returns:
            True if WDA is ready, False otherwise.
        """
        try:
            self._client.get("status", use_session=False, timeout=float(timeout))
            return True
        except WDAError:
            return False

    def start_wda_session(self) -> tuple[bool, str]:
        """
        Start a new WebDriverAgent session.

        Returns:
            Tuple of (success, session_id or error_message).
        """
        try:
            data = self._client.post(
                "session",
                use_session=False,
                json={"capabilities": {}},
                timeout=30.0,
                allow_status=(200, 201),
            )

            session_id = None
            if isinstance(data, dict):
                session_id = data.get("sessionId") or data.get("value", {}).get("sessionId")
            return True, session_id or "session_started"
        except WDAError as e:
            return False, str(e)

    def get_wda_status(self) -> dict | None:
        """
        Get WebDriverAgent status information.

        Returns:
            Status dictionary or None if not available.
        """
        try:
            data = self._client.get("status", use_session=False, timeout=5.0)
            return data if isinstance(data, dict) else None
        except WDAError:
            return None

    def restart_wda(self) -> tuple[bool, str]:
        """
        Restart WebDriverAgent (requires manual restart on device).

        Returns:
            Tuple of (success, message).

        Note:
            This method only checks if WDA needs restart.
            Actual restart requires re-running WDA on the device via Xcode or other means.
        """
        if self.is_wda_ready():
            return True, "WDA is already running"
        else:
            return (
                False,
                "WDA is not running. Please start it manually on the device.",
            )


def quick_connect(wda_url: str = "http://localhost:8100") -> tuple[bool, str]:
    """
    Quick helper to check iOS device connection and WDA status.

    Args:
        wda_url: WebDriverAgent URL.

    Returns:
        Tuple of (success, message).
    """
    conn = WDAConnection(wda_url=wda_url)

    if not conn.is_wda_ready():
        return False, "WebDriverAgent is not running"

    return True, "WebDriverAgent is reachable"
