"""Tests for presence detection state machine."""
import pytest
from tests.conftest import advance_time, reset_time


@pytest.fixture(autouse=True)
def setup():
    """Reset time before each test."""
    reset_time()


def test_idle_to_detecting():
    """Presence should start detection timer."""
    from core.presence import PresenceDetector, PresenceState

    detector = PresenceDetector(activation_ms=1000, timeout_ms=5000)

    assert detector.state == PresenceState.IDLE

    detector.update(presence_detected=True)

    assert detector.state == PresenceState.DETECTING


def test_detecting_to_active():
    """Sustained presence should activate."""
    from core.presence import PresenceDetector, PresenceState

    activated = []

    def on_activate():
        activated.append(True)

    detector = PresenceDetector(
        activation_ms=1000,
        timeout_ms=5000,
        on_activate=on_activate,
    )

    detector.update(presence_detected=True)
    assert detector.state == PresenceState.DETECTING
    assert not activated

    advance_time(500)
    detector.update(presence_detected=True)
    assert detector.state == PresenceState.DETECTING

    advance_time(600)
    detector.update(presence_detected=True)
    assert detector.state == PresenceState.ACTIVE
    assert len(activated) == 1


def test_active_to_timeout():
    """No presence should start timeout."""
    from core.presence import PresenceDetector, PresenceState

    detector = PresenceDetector(activation_ms=100, timeout_ms=5000)

    detector.update(presence_detected=True)
    advance_time(150)
    detector.update(presence_detected=True)

    assert detector.state == PresenceState.ACTIVE

    detector.update(presence_detected=False)
    assert detector.state == PresenceState.TIMEOUT


def test_timeout_to_idle():
    """Expired timeout should deactivate."""
    from core.presence import PresenceDetector, PresenceState

    deactivated = []

    def on_deactivate():
        deactivated.append(True)

    detector = PresenceDetector(
        activation_ms=100,
        timeout_ms=1000,
        on_deactivate=on_deactivate,
    )

    detector.update(presence_detected=True)
    advance_time(150)
    detector.update(presence_detected=True)
    assert detector.state == PresenceState.ACTIVE

    detector.update(presence_detected=False)
    assert detector.state == PresenceState.TIMEOUT
    assert not deactivated

    advance_time(1100)
    detector.update(presence_detected=False)
    assert detector.state == PresenceState.IDLE
    assert len(deactivated) == 1


def test_interrupted_detection():
    """Interrupted presence should reset."""
    from core.presence import PresenceDetector, PresenceState

    detector = PresenceDetector(activation_ms=1000, timeout_ms=5000)

    detector.update(presence_detected=True)
    assert detector.state == PresenceState.DETECTING

    detector.update(presence_detected=False)
    assert detector.state == PresenceState.IDLE


def test_return_during_timeout():
    """Return during timeout should reactivate."""
    from core.presence import PresenceDetector, PresenceState

    detector = PresenceDetector(activation_ms=100, timeout_ms=5000)

    detector.update(presence_detected=True)
    advance_time(150)
    detector.update(presence_detected=True)
    assert detector.state == PresenceState.ACTIVE

    detector.update(presence_detected=False)
    assert detector.state == PresenceState.TIMEOUT

    detector.update(presence_detected=True)
    assert detector.state == PresenceState.ACTIVE
