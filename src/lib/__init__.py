"""
Mirror light controller library.

Modules:
    sensor: Ultrasonic distance sensor driver.
    light: LED/light strip controller.
    presence: Presence detection state machine.
    power: Power management and sleep modes.
"""
from lib.sensor import UltrasonicSensor
from lib.light import LightController
from lib.presence import PresenceDetector
from lib.power import PowerManager

__all__ = [
    "UltrasonicSensor",
    "LightController",
    "PresenceDetector",
    "PowerManager",
]
