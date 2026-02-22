"""
Configuration module for mirror light controller.

All hardware pins and timing parameters in one place.
"""


class PinConfig:
    """GPIO pin assignments."""

    # VL53L0X I2C pins
    SDA: int = 8
    SCL: int = 9

    # Ultrasonic sensor pins (legacy/prototype)
    TRIGGER: int = 13
    ECHO: int = 12

    # Output
    LED: int = 4


class SensorConfig:
    """Sensor parameters."""

    # Sensor type: "vl53l0x" or "ultrasonic"
    SENSOR_TYPE: str = "vl53l0x"

    MAX_DISTANCE_CM: float = 60.0
    MIN_DISTANCE_CM: float = 3.0

    # Ultrasonic specific
    TIMEOUT_US: int = 30000
    SOUND_SPEED_DIVISOR: float = 29.1


class TimingConfig:
    """Timing parameters for activation and timeout."""

    ACTIVATION_MS: int = 1500
    TIMEOUT_MS: int = 5000
    POLL_INTERVAL_MS: int = 150


class PowerConfig:
    """Power management settings."""

    USE_LIGHT_SLEEP: bool = True  # Saves ~60% power, disables REPL
    SLEEP_DURATION_MS: int = 150
