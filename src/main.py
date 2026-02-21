"""
Mirror light controller - Main application.

Contactless bathroom mirror light using proximity sensor.
"""
from config import PinConfig, SensorConfig, TimingConfig, PowerConfig
from lib import UltrasonicSensor, LightController, PresenceDetector, PowerManager


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
