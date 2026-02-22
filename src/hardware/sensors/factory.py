"""
Sensor factory for creating distance sensor instances.

Implements Factory Pattern with self-registration via decorators.
"""
from hardware.sensors.base import DistanceSensor


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
