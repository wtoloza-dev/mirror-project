"""
Ultrasonic distance sensor driver.

Supports AJ-SR04M and compatible HC-SR04 sensors.
"""
from machine import Pin, time_pulse_us
from time import sleep_us


class UltrasonicSensor:
    """
    Driver for ultrasonic distance sensors.

    Attributes:
        trigger_pin: GPIO pin connected to sensor TRIG.
        echo_pin: GPIO pin connected to sensor ECHO.
        timeout_us: Maximum wait time for echo in microseconds.
        sound_divisor: Speed of sound factor for distance calculation.
    """

    def __init__(
        self,
        trigger_pin: int,
        echo_pin: int,
        timeout_us: int = 30000,
        sound_divisor: float = 29.1,
    ) -> None:
        """
        Initialize the ultrasonic sensor.

        Args:
            trigger_pin: GPIO number for trigger output.
            echo_pin: GPIO number for echo input.
            timeout_us: Echo timeout in microseconds.
            sound_divisor: Divisor for distance calculation.
        """
        self._trigger = Pin(trigger_pin, Pin.OUT)
        self._echo = Pin(echo_pin, Pin.IN)
        self._timeout_us = timeout_us
        self._sound_divisor = sound_divisor
        self._trigger.off()

    def measure(self) -> float:
        """
        Measure distance to nearest object.

        Returns:
            Distance in centimeters, or -1.0 if measurement failed.
        """
        self._send_pulse()
        duration = self._read_echo()

        if duration < 0:
            return -1.0

        return self._calculate_distance(duration)

    def _send_pulse(self) -> None:
        """Send 10us trigger pulse to initiate measurement."""
        self._trigger.off()
        sleep_us(2)
        self._trigger.on()
        sleep_us(10)
        self._trigger.off()

    def _read_echo(self) -> int:
        """
        Read echo pulse duration.

        Returns:
            Pulse duration in microseconds, or negative on error.
        """
        return time_pulse_us(self._echo, 1, self._timeout_us)

    def _calculate_distance(self, duration_us: int) -> float:
        """
        Convert pulse duration to distance.

        Args:
            duration_us: Echo pulse duration in microseconds.

        Returns:
            Distance in centimeters.
        """
        return (duration_us / 2) / self._sound_divisor
