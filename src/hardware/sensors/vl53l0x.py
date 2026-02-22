"""
VL53L0X Time-of-Flight laser distance sensor driver.

I2C-based sensor using laser ranging for accurate distance measurement.

Specifications:
    - Range: 3cm - 200cm
    - Accuracy: ±3%
    - Interface: I2C (400kHz)
    - Voltage: 2.8V - 5V (3.3V recommended)
    - Default I2C address: 0x29

Pinout:
    VIN -> 3.3V (NOT 5V for ESP32)
    GND -> GND
    SDA -> I2C SDA (with pullup)
    SCL -> I2C SCL (with pullup)
"""
from machine import Pin, I2C
from time import sleep_ms

from hardware.sensors.base import DistanceSensor
from hardware.sensors.factory import SensorFactory


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
