"""WebDriverAgent (WDA) connection management.

To control a device, provide a reachable WDA URL.

- Wi‑Fi (recommended): http://<device-ip>:8100
- USB: forward :8100 to this machine (then http://localhost:8100)
"""

from phone_agent.ios.wda.wda_client import WDAClient, WDAError


def _extract_session_ids(payload: object) -> list[str]:
    session_ids: list[str] = []

    if isinstance(payload, dict):
        top_session_id = payload.get("sessionId")
        if isinstance(top_session_id, str) and top_session_id:
            session_ids.append(top_session_id)

        value = payload.get("value")
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    continue
                candidate = item.get("id") or item.get("sessionId")
                if isinstance(candidate, str) and candidate:
                    session_ids.append(candidate)
        elif isinstance(value, dict):
            candidate = value.get("id") or value.get("sessionId")
            if isinstance(candidate, str) and candidate:
                session_ids.append(candidate)
    elif isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            candidate = item.get("id") or item.get("sessionId")
            if isinstance(candidate, str) and candidate:
                session_ids.append(candidate)

    deduped: list[str] = []
    seen: set[str] = set()
    for session_id in session_ids:
        if session_id in seen:
            continue
        seen.add(session_id)
        deduped.append(session_id)
    return deduped


def _extract_session_id_from_status(status: object) -> str | None:
    if not isinstance(status, dict):
        return None

    top_session_id = status.get("sessionId")
    if isinstance(top_session_id, str) and top_session_id:
        return top_session_id

    value = status.get("value")
    if isinstance(value, dict):
        value_session_id = value.get("sessionId")
        if isinstance(value_session_id, str) and value_session_id:
            return value_session_id
    return None


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
            if not session_id:
                session_ids = self.list_wda_sessions()
                if session_ids:
                    session_id = session_ids[0]
            return True, session_id or "session_started"
        except WDAError as e:
            return False, str(e)

    def list_wda_sessions(self) -> list[str]:
        """List active WDA session IDs, if supported by the server."""
        try:
            data = self._client.get("sessions", use_session=False, timeout=5.0)
            session_ids = _extract_session_ids(data)
            if session_ids:
                return session_ids
        except WDAError:
            pass

        status = self.get_wda_status()
        session_id = _extract_session_id_from_status(status) if status else None
        return [session_id] if session_id else []

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
