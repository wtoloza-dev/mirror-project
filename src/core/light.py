"""
Light controller module.

Handles LED/light strip control with optional PWM support.
"""
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
