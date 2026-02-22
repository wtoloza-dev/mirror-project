"""
Ultrasonic distance sensor driver.

Supports trigger/echo based ultrasonic sensors:
    - HC-SR04 (standard, not waterproof)
    - AJ-SR04M (waterproof, separate transducer)
    - JSN-SR04T (waterproof, integrated)

Pinout:
    VCC  -> 5V
    GND  -> GND
    TRIG -> GPIO (output from MCU)
    ECHO -> GPIO (input to MCU)

Range: 2cm - 400cm (sensor dependent)
"""
from machine import Pin, time_pulse_us
from time import sleep_us

from hardware.sensors.base import DistanceSensor
from hardware.sensors.factory import SensorFactory


@SensorFactory.register("ultrasonic")
class UltrasonicSensor(DistanceSensor):
    """
    Driver for ultrasonic distance sensors.

    Uses trigger pulse and echo timing to calculate distance
    based on speed of sound.

    Attributes:
        _trigger: Output pin for trigger pulse.
        _echo: Input pin for echo signal.
        _timeout_us: Maximum wait time for echo.
        _sound_divisor: Factor for distance calculation.
    """

    SPEED_OF_SOUND_DIVISOR = 29.1  # microseconds per cm (round trip / 2)

    def __init__(
        self,
        trigger_pin: int,
        echo_pin: int,
        timeout_us: int = 30000,
        sound_divisor: float = None,
    ) -> None:
        """
        Initialize ultrasonic sensor.

        Args:
            trigger_pin: GPIO number for trigger output.
            echo_pin: GPIO number for echo input.
            timeout_us: Echo timeout in microseconds (default 30ms = ~5m).
            sound_divisor: Custom divisor for distance calc (default 29.1).
        """
        self._trigger = Pin(trigger_pin, Pin.OUT)
        self._echo = Pin(echo_pin, Pin.IN)
        self._timeout_us = timeout_us
        self._sound_divisor = sound_divisor or self.SPEED_OF_SOUND_DIVISOR
        self._trigger.off()

    def measure(self) -> float:
        """
        Measure distance to nearest object.

        Sends 10us trigger pulse and measures echo duration.

        Returns:
            Distance in centimeters, or -1.0 on timeout/error.
        """
        self._send_trigger_pulse()
        duration = time_pulse_us(self._echo, 1, self._timeout_us)

        if duration < 0:
            return -1.0

        return (duration / 2) / self._sound_divisor

    def _send_trigger_pulse(self) -> None:
        """Send 10 microsecond trigger pulse."""
        self._trigger.off()
        sleep_us(2)
        self._trigger.on()
        sleep_us(10)
        self._trigger.off()
