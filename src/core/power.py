"""
Power management module.

Handles sleep modes for energy efficiency.
"""
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
