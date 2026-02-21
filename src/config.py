"""
Configuration module for mirror light controller.

All hardware pins and timing parameters in one place.
"""


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
