"""
Sensor drivers package.

Reusable sensor implementations following the DistanceSensor protocol.
Copy this folder to any project that needs distance sensing.

Available sensors:
    - ultrasonic: HC-SR04, AJ-SR04M, JSN-SR04T (trigger/echo)
    - vl53l0x: VL53L0X Time-of-Flight laser sensor (I2C)

Usage:
    from hardware.sensors import SensorFactory

    # Create sensor by type
    sensor = SensorFactory.create("vl53l0x", sda_pin=8, scl_pin=9)
    distance = sensor.measure()

Adding new sensors:
    1. Create new file in this folder (e.g., my_sensor.py)
    2. Inherit from DistanceSensor
    3. Decorate class with @SensorFactory.register("my_sensor")
    4. Import in this __init__.py
"""
from hardware.sensors.base import DistanceSensor
from hardware.sensors.factory import SensorFactory

import hardware.sensors.ultrasonic  # noqa: F401
import hardware.sensors.vl53l0x  # noqa: F401

__all__ = [
    "DistanceSensor",
    "SensorFactory",
]
