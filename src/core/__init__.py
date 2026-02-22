"""
Core application logic.

Contains the business logic for the mirror light controller.
Independent of hardware implementation details.

Modules:
    light: LED/relay output control.
    presence: State machine for presence detection.
    power: Power management and sleep modes.
"""
from core.light import LightController
from core.presence import PresenceDetector
from core.power import PowerManager

__all__ = [
    "LightController",
    "PresenceDetector",
    "PowerManager",
]
