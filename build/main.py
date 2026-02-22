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



# ============================================================
# hardware/sensors/base.py
# ============================================================

from abc import ABC, abstractmethod


class DistanceSensor(ABC):
    """
    Abstract base class for distance sensors.

    All sensor implementations must inherit from this class
    and implement the measure() method.

    This ensures consistent interface across different sensor types,
    enabling the Factory pattern and dependency injection.

    Methods:
        measure: Returns distance in centimeters or -1 on failure.
        sensor_type: Returns string identifier for the sensor.
    """

    @abstractmethod
    def measure(self) -> float:
        """
        Measure distance to nearest object.

        Returns:
            Distance in centimeters.
            Returns -1.0 if measurement failed or object out of range.

        Note:
            Implementations should handle hardware errors gracefully
            and return -1.0 rather than raising exceptions.
        """
        pass

    @property
    def sensor_type(self) -> str:
        """
        Return sensor type identifier.

        Returns:
            String name of the sensor class.
        """
        return self.__class__.__name__



# ============================================================
# hardware/sensors/factory.py
# ============================================================

class SensorFactory:
    """
    Factory for creating distance sensor instances.

    Uses registry pattern - sensors register themselves via decorator.
    New sensors can be added without modifying this class.

    Class Attributes:
        _registry: Dictionary mapping sensor type names to classes.

    Example:
        # Register a new sensor type
        @SensorFactory.register("my_sensor")
        class MySensor(DistanceSensor):
            def __init__(self, pin: int):
                self._pin = pin

            def measure(self) -> float:
                return 42.0

        # Create sensor instance
        sensor = SensorFactory.create("my_sensor", pin=5)
    """

    _registry: dict = {}

    @classmethod
    def register(cls, sensor_type: str):
        """
        Decorator to register a sensor class in the factory.

        Args:
            sensor_type: Unique string identifier for the sensor.

        Returns:
            Decorator function that registers the class.

        Example:
            @SensorFactory.register("ultrasonic")
            class UltrasonicSensor(DistanceSensor):
                ...
        """
        def decorator(sensor_class):
            cls._registry[sensor_type] = sensor_class
            return sensor_class
        return decorator

    @classmethod
    def create(cls, sensor_type: str, **kwargs) -> DistanceSensor:
        """
        Create a sensor instance of the specified type.

        Args:
            sensor_type: Registered type name of sensor to create.
            **kwargs: Arguments passed to sensor constructor.

        Returns:
            New instance of the requested sensor type.

        Raises:
            ValueError: If sensor_type is not registered.

        Example:
            sensor = SensorFactory.create(
                "vl53l0x",
                sda_pin=8,
                scl_pin=9
            )
        """
        if sensor_type not in cls._registry:
            available = ", ".join(cls._registry.keys()) or "none"
            raise ValueError(
                f"Unknown sensor type: '{sensor_type}'. "
                f"Available: {available}"
            )

        sensor_class = cls._registry[sensor_type]
        return sensor_class(**kwargs)

    @classmethod
    def available_types(cls) -> list:
        """
        Get list of all registered sensor types.

        Returns:
            List of sensor type name strings.
        """
        return list(cls._registry.keys())



# ============================================================
# hardware/sensors/ultrasonic.py
# ============================================================

from machine import Pin, time_pulse_us
from time import sleep_us



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



# ============================================================
# hardware/sensors/vl53l0x.py
# ============================================================

from machine import Pin, I2C
from time import sleep_ms



@SensorFactory.register("vl53l0x")
class VL53L0XSensor(DistanceSensor):
    """
    Driver for VL53L0X Time-of-Flight distance sensor.

    Uses I2C communication with the sensor's onboard
    microcontroller for distance measurement.

    Attributes:
        _i2c: I2C bus instance.
        _address: I2C address of sensor.
    """

    DEFAULT_ADDRESS = 0x29
    MODEL_ID = 0xEE

    # Register addresses
    _REG_SYSRANGE_START = 0x00
    _REG_RESULT_INTERRUPT_STATUS = 0x13
    _REG_RESULT_RANGE_STATUS = 0x14
    _REG_MODEL_ID = 0xC0

    def __init__(
        self,
        sda_pin: int,
        scl_pin: int,
        i2c_id: int = 0,
        address: int = None,
    ) -> None:
        """
        Initialize VL53L0X sensor.

        Args:
            sda_pin: GPIO number for I2C SDA.
            scl_pin: GPIO number for I2C SCL.
            i2c_id: I2C bus ID (0 or 1, default 0).
            address: I2C address (default 0x29).
        """
        self._address = address or self.DEFAULT_ADDRESS
        self._i2c = I2C(
            i2c_id,
            sda=Pin(sda_pin),
            scl=Pin(scl_pin),
            freq=400000
        )
        self._init_sensor()

    def _init_sensor(self) -> None:
        """Initialize sensor with default configuration."""
        model_id = self._read_reg(self._REG_MODEL_ID)
        if model_id != self.MODEL_ID:
            print(f"Warning: VL53L0X model ID {model_id:#x}, expected {self.MODEL_ID:#x}")

        # Standard initialization sequence
        self._write_reg(0x88, 0x00)
        self._write_reg(0x80, 0x01)
        self._write_reg(0xFF, 0x01)
        self._write_reg(0x00, 0x00)
        self._write_reg(0x00, 0x01)
        self._write_reg(0xFF, 0x00)
        self._write_reg(0x80, 0x00)

    def measure(self) -> float:
        """
        Measure distance to nearest object.

        Triggers single measurement and waits for result.

        Returns:
            Distance in centimeters, or -1.0 on timeout/error.
        """
        # Start measurement
        self._write_reg(self._REG_SYSRANGE_START, 0x01)

        # Wait for measurement complete (max 500ms)
        for _ in range(100):
            sleep_ms(5)
            status = self._read_reg(self._REG_RESULT_INTERRUPT_STATUS)
            if status & 0x07:
                break
        else:
            return -1.0

        # Clear interrupt
        self._write_reg(0x0B, 0x01)

        # Read distance
        data = self._read_reg_multi(self._REG_RESULT_RANGE_STATUS, 12)
        distance_mm = (data[10] << 8) | data[11]

        # Check for out of range
        if distance_mm >= 8190:
            return -1.0

        return distance_mm / 10.0

    def _write_reg(self, reg: int, value: int) -> None:
        """Write single byte to register."""
        self._i2c.writeto_mem(self._address, reg, bytes([value]))

    def _read_reg(self, reg: int) -> int:
        """Read single byte from register."""
        return self._i2c.readfrom_mem(self._address, reg, 1)[0]

    def _read_reg_multi(self, reg: int, length: int) -> bytes:
        """Read multiple bytes starting from register."""
        return self._i2c.readfrom_mem(self._address, reg, length)



# ============================================================
# core/light.py
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
# core/presence.py
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
# core/power.py
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
Uses Factory Pattern for sensor creation - supports multiple sensor types.
"""


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
        print(f"  Light sleep: {PowerConfig.USE_LIGHT_SLEEP}")
        print("Ready.")


def main() -> None:
    """Application entry point."""
    sensor = create_sensor()
    app = MirrorLightApp(sensor)
    app.run()


if __name__ == "__main__":
    main()

