"""
Presence detection state machine.

Handles timing logic for activation delay and timeout.
"""
from time import ticks_ms, ticks_diff


class PresenceState:
    """Enum-like class for presence states."""

    IDLE = "idle"
    DETECTING = "detecting"
    ACTIVE = "active"
    TIMEOUT = "timeout"


class PresenceDetector:
    """
    State machine for presence detection with hysteresis.

    Prevents false triggers by requiring sustained presence
    before activation and delayed timeout before deactivation.

    State diagram:
        IDLE → (presence) → DETECTING → (sustained) → ACTIVE
        ACTIVE → (no presence) → TIMEOUT → (expired) → IDLE
    """

    def __init__(
        self,
        activation_ms: int,
        timeout_ms: int,
        on_activate=None,
        on_deactivate=None,
    ) -> None:
        """
        Initialize presence detector.

        Args:
            activation_ms: Time presence must be sustained to activate.
            timeout_ms: Time without presence before deactivating.
            on_activate: Callback when light should turn on.
            on_deactivate: Callback when light should turn off.
        """
        self._activation_ms = activation_ms
        self._timeout_ms = timeout_ms
        self._on_activate = on_activate
        self._on_deactivate = on_deactivate

        self._state = PresenceState.IDLE
        self._detection_start: int = 0
        self._last_presence: int = 0

    @property
    def state(self) -> str:
        """Return current state."""
        return self._state

    @property
    def is_active(self) -> bool:
        """Return True if light should be on."""
        return self._state == PresenceState.ACTIVE

    def update(self, presence_detected: bool) -> None:
        """
        Update state machine with new sensor reading.

        Args:
            presence_detected: True if sensor detects presence.
        """
        now = ticks_ms()

        if presence_detected:
            self._handle_presence(now)
        else:
            self._handle_no_presence(now)

    def _handle_presence(self, now: int) -> None:
        """Handle state transitions when presence is detected."""
        self._last_presence = now

        if self._state == PresenceState.IDLE:
            self._state = PresenceState.DETECTING
            self._detection_start = now

        elif self._state == PresenceState.DETECTING:
            elapsed = ticks_diff(now, self._detection_start)
            if elapsed >= self._activation_ms:
                self._state = PresenceState.ACTIVE
                if self._on_activate:
                    self._on_activate()

        elif self._state == PresenceState.TIMEOUT:
            self._state = PresenceState.ACTIVE

    def _handle_no_presence(self, now: int) -> None:
        """Handle state transitions when no presence is detected."""
        if self._state == PresenceState.DETECTING:
            self._state = PresenceState.IDLE

        elif self._state == PresenceState.ACTIVE:
            self._state = PresenceState.TIMEOUT

        elif self._state == PresenceState.TIMEOUT:
            elapsed = ticks_diff(now, self._last_presence)
            if elapsed >= self._timeout_ms:
                self._state = PresenceState.IDLE
                if self._on_deactivate:
                    self._on_deactivate()
