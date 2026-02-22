"""
Base sensor protocol/interface.

Defines the contract that all distance sensors must implement.
"""
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
