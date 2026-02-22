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

    MAX_DISTANCE_CM: float = 40.0
    MIN_DISTANCE_CM: float = 3.0

    # Ultrasonic specific
    TIMEOUT_US: int = 30000
    SOUND_SPEED_DIVISOR: float = 29.1


class TimingConfig:
    """Timing parameters for activation and timeout."""

    ACTIVATION_MS: int = 1000  # 1 second of sustained presence
    TIMEOUT_MS: int = 3000     # Reduced: quicker off (fade compensates)
    POLL_INTERVAL_MS: int = 100


class LightConfig:
    """Light/LED control settings."""

    USE_FADE: bool = True           # Enable fade in/out effects
    FADE_DURATION_MS: int = 600     # Duration of fade effect
    FADE_STEPS: int = 50            # Smoothness (more = smoother)
    PWM_FREQ: int = 1000            # PWM frequency in Hz


class PowerConfig:
    """Power management settings."""

    USE_LIGHT_SLEEP: bool = True  # Saves ~60% power, disables REPL
    SLEEP_DURATION_MS: int = 100  # Match poll interval
