"""
Mirror light controller - Main application.

Contactless bathroom mirror light using proximity sensor.
Uses Factory Pattern for sensor creation - supports multiple sensor types.
"""
from config import PinConfig, SensorConfig, TimingConfig, LightConfig, PowerConfig
from hardware.sensors import DistanceSensor, SensorFactory
from core import LightController, PresenceDetector, PowerManager


def create_sensor() -> DistanceSensor:
    """
    Create sensor instance using Factory Pattern.

    Reads sensor type from configuration and creates
    appropriate sensor with configured pins.

    Returns:
        Configured sensor instance implementing DistanceSensor.
    """
    sensor_type = SensorConfig.SENSOR_TYPE

    if sensor_type == "vl53l0x":
        return SensorFactory.create(
            sensor_type,
            sda_pin=PinConfig.SDA,
            scl_pin=PinConfig.SCL,
        )
    elif sensor_type == "ultrasonic":
        return SensorFactory.create(
            sensor_type,
            trigger_pin=PinConfig.TRIGGER,
            echo_pin=PinConfig.ECHO,
            timeout_us=SensorConfig.TIMEOUT_US,
            sound_divisor=SensorConfig.SOUND_SPEED_DIVISOR,
        )
    else:
        raise ValueError(f"Unknown sensor type: {sensor_type}")


class MirrorLightApp:
    """
    Main application controller.

    Coordinates sensor, light, presence detection, and power management.
    Uses dependency injection for sensor to support multiple types.
    """

    def __init__(self, sensor: DistanceSensor) -> None:
        """
        Initialize application with injected sensor.

        Args:
            sensor: Distance sensor instance implementing DistanceSensor.
        """
        self._sensor = sensor
        self._light = LightController(
            pin=PinConfig.LED,
            use_fade=LightConfig.USE_FADE,
            fade_duration_ms=LightConfig.FADE_DURATION_MS,
            fade_steps=LightConfig.FADE_STEPS,
            pwm_freq=LightConfig.PWM_FREQ,
        )
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
        print("Light ON - presence confirmed")

    def _on_presence_end(self) -> None:
        """Callback when presence timeout expired."""
        self._light.off()
        print("Light OFF - presence timeout")

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
            True if valid presence detected within configured range.
        """
        if distance < 0:
            return False
        if distance < SensorConfig.MIN_DISTANCE_CM:
            return False
        return distance < SensorConfig.MAX_DISTANCE_CM

    def _print_config(self) -> None:
        """Print current configuration on startup."""
        print("Mirror Light Controller")
        print(f"  Sensor:      {self._sensor.sensor_type}")
        print(f"  Range:       {SensorConfig.MIN_DISTANCE_CM}-{SensorConfig.MAX_DISTANCE_CM}cm")
        print(f"  Activation:  {TimingConfig.ACTIVATION_MS}ms")
        print(f"  Timeout:     {TimingConfig.TIMEOUT_MS}ms")
        print(f"  Fade:        {LightConfig.USE_FADE} ({LightConfig.FADE_DURATION_MS}ms)")
        print(f"  Light sleep: {PowerConfig.USE_LIGHT_SLEEP}")
        print("Ready.")


def main() -> None:
    """Application entry point."""
    sensor = create_sensor()
    app = MirrorLightApp(sensor)
    app.run()


if __name__ == "__main__":
    main()
