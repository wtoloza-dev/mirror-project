"""
Mirror Light Controller - Combined build.

Auto-generated from src/ files. Do not edit directly.
Edit source files in src/ and run: uv run python scripts/build.py
"""


# ============================================================
# config.py
# ============================================================

class PinConfig:
    """GPIO pin assignments."""

    TRIGGER: int = 13
    ECHO: int = 12
    LED: int = 2


class SensorConfig:
    """Ultrasonic sensor parameters."""

    MAX_DISTANCE_CM: float = 30.0
    TIMEOUT_US: int = 30000
    SOUND_SPEED_DIVISOR: float = 29.1


class TimingConfig:
    """Timing parameters for activation and timeout."""

    ACTIVATION_MS: int = 1500
    TIMEOUT_MS: int = 5000
    POLL_INTERVAL_MS: int = 150


class PowerConfig:
    """Power management settings."""

    USE_LIGHT_SLEEP: bool = False  # Set True for production
    SLEEP_DURATION_MS: int = 150



# ============================================================
# lib/sensor.py
# ============================================================

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



# ============================================================
# lib/light.py
# ============================================================

from machine import Pin


class LightController:
    """
    Controls output for LED or light strip.

    Attributes:
        pin: GPIO pin controlling the light.
        is_on: Current state of the light.
    """

    def __init__(self, pin: int, inverted: bool = False) -> None:
        """
        Initialize light controller.

        Args:
            pin: GPIO number for light control.
            inverted: If True, LOW turns light on (for some MOSFETs).
        """
        self._pin = Pin(pin, Pin.OUT)
        self._inverted = inverted
        self._is_on = False
        self.off()

    @property
    def is_on(self) -> bool:
        """Return current light state."""
        return self._is_on

    def on(self) -> None:
        """Turn light on."""
        if self._inverted:
            self._pin.off()
        else:
            self._pin.on()
        self._is_on = True

    def off(self) -> None:
        """Turn light off."""
        if self._inverted:
            self._pin.on()
        else:
            self._pin.off()
        self._is_on = False

    def toggle(self) -> None:
        """Toggle light state."""
        if self._is_on:
            self.off()
        else:
            self.on()



# ============================================================
# lib/presence.py
# ============================================================

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



# ============================================================
# lib/power.py
# ============================================================

import machine
from time import sleep_ms


class PowerManager:
    """
    Manages power states and sleep modes.

    Supports light sleep for ~60% power reduction while
    maintaining quick wake-up for sensor polling.
    """

    def __init__(self, use_light_sleep: bool = True) -> None:
        """
        Initialize power manager.

        Args:
            use_light_sleep: If True, use light sleep instead of busy wait.
        """
        self._use_light_sleep = use_light_sleep

    def sleep(self, duration_ms: int) -> None:
        """
        Sleep for specified duration.

        Uses light sleep if enabled, otherwise regular sleep.
        Light sleep reduces power from ~50mA to ~20mA.

        Args:
            duration_ms: Sleep duration in milliseconds.
        """
        if self._use_light_sleep:
            self._light_sleep(duration_ms)
        else:
            sleep_ms(duration_ms)

    def _light_sleep(self, duration_ms: int) -> None:
        """
        Enter light sleep mode.

        CPU stops, RTC and some peripherals remain active.
        Wake-up time is ~3ms.

        Args:
            duration_ms: Sleep duration in milliseconds.
        """
        try:
            machine.lightsleep(duration_ms)
        except AttributeError:
            sleep_ms(duration_ms)

    @staticmethod
    def deep_sleep(duration_ms: int) -> None:
        """
        Enter deep sleep mode.

        Almost all systems off. Wake causes reset.
        Use only when you don't need quick response.

        Args:
            duration_ms: Sleep duration in milliseconds.
        """
        machine.deepsleep(duration_ms)



# ============================================================
# main.py
# ============================================================

"""
Mirror light controller - Main application.

Contactless bathroom mirror light using proximity sensor.
"""


class MirrorLightApp:
    """
    Main application controller.

    Coordinates sensor, light, presence detection, and power management.
    """

    def __init__(self) -> None:
        """Initialize all components."""
        self._sensor = UltrasonicSensor(
            trigger_pin=PinConfig.TRIGGER,
            echo_pin=PinConfig.ECHO,
            timeout_us=SensorConfig.TIMEOUT_US,
            sound_divisor=SensorConfig.SOUND_SPEED_DIVISOR,
        )

        self._light = LightController(pin=PinConfig.LED)

        self._presence = PresenceDetector(
            activation_ms=TimingConfig.ACTIVATION_MS,
            timeout_ms=TimingConfig.TIMEOUT_MS,
            on_activate=self._on_presence_start,
            on_deactivate=self._on_presence_end,
        )

        self._power = PowerManager(use_light_sleep=PowerConfig.USE_LIGHT_SLEEP)

    def _on_presence_start(self) -> None:
        """Callback when sustained presence detected."""
        self._light.on()
        print(f"Light ON - presence confirmed")

    def _on_presence_end(self) -> None:
        """Callback when presence timeout expired."""
        self._light.off()
        print(f"Light OFF - presence timeout")

    def run(self) -> None:
        """Main application loop."""
        self._print_config()

        while True:
            distance = self._sensor.measure()
            presence = self._is_presence(distance)
            self._presence.update(presence)
            self._power.sleep(PowerConfig.SLEEP_DURATION_MS)

    def _is_presence(self, distance: float) -> bool:
        """
        Determine if distance indicates presence.

        Args:
            distance: Measured distance in cm.

        Returns:
            True if valid presence detected.
        """
        if distance < 0:
            return False
        return distance < SensorConfig.MAX_DISTANCE_CM

    def _print_config(self) -> None:
        """Print current configuration on startup."""
        print("Mirror Light Controller")
        print(f"  Detection:  <{SensorConfig.MAX_DISTANCE_CM}cm")
        print(f"  Activation: {TimingConfig.ACTIVATION_MS}ms")
        print(f"  Timeout:    {TimingConfig.TIMEOUT_MS}ms")
        print(f"  Light sleep: {PowerConfig.USE_LIGHT_SLEEP}")
        print("Ready.")


def main() -> None:
    """Application entry point."""
    app = MirrorLightApp()
    app.run()


if __name__ == "__main__":
    main()

