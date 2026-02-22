"""
Light controller module.

Handles LED/light strip control with PWM support for fade effects.
"""
from machine import Pin, PWM
from time import sleep_ms


class LightController:
    """
    Controls output for LED or light strip with fade effects.

    Supports both simple on/off and smooth PWM transitions.

    Attributes:
        pin: GPIO pin controlling the light.
        is_on: Current state of the light.
    """

    MAX_DUTY = 65535  # 16-bit PWM resolution

    def __init__(
        self,
        pin: int,
        use_fade: bool = True,
        fade_duration_ms: int = 500,
        fade_steps: int = 50,
        pwm_freq: int = 1000,
    ) -> None:
        """
        Initialize light controller.

        Args:
            pin: GPIO number for light control.
            use_fade: If True, use smooth fade transitions.
            fade_duration_ms: Total duration of fade effect.
            fade_steps: Number of steps in fade (smoothness).
            pwm_freq: PWM frequency in Hz.
        """
        self._use_fade = use_fade
        self._fade_duration_ms = fade_duration_ms
        self._fade_steps = fade_steps
        self._is_on = False
        self._current_duty = 0

        if use_fade:
            self._pwm = PWM(Pin(pin), freq=pwm_freq, duty_u16=0)
        else:
            self._pin = Pin(pin, Pin.OUT)
            self._pin.off()

    @property
    def is_on(self) -> bool:
        """Return current light state."""
        return self._is_on

    def on(self) -> None:
        """Turn light on with optional fade in."""
        if self._is_on:
            return

        if self._use_fade:
            self._fade_to(self.MAX_DUTY)
        else:
            self._pin.on()

        self._is_on = True

    def off(self) -> None:
        """Turn light off with optional fade out."""
        if not self._is_on:
            return

        if self._use_fade:
            self._fade_to(0)
        else:
            self._pin.off()

        self._is_on = False

    def _fade_to(self, target_duty: int) -> None:
        """
        Smoothly transition to target brightness.

        Args:
            target_duty: Target PWM duty cycle (0-65535).
        """
        start_duty = self._current_duty
        step_delay = self._fade_duration_ms // self._fade_steps
        duty_step = (target_duty - start_duty) // self._fade_steps

        for i in range(self._fade_steps):
            self._current_duty = start_duty + (duty_step * (i + 1))
            self._pwm.duty_u16(max(0, min(self.MAX_DUTY, self._current_duty)))
            sleep_ms(step_delay)

        self._current_duty = target_duty
        self._pwm.duty_u16(target_duty)

    def set_brightness(self, percent: int) -> None:
        """
        Set brightness level (0-100%).

        Args:
            percent: Brightness percentage.
        """
        if not self._use_fade:
            return

        duty = int((percent / 100) * self.MAX_DUTY)
        self._pwm.duty_u16(duty)
        self._current_duty = duty
        self._is_on = percent > 0

    def toggle(self) -> None:
        """Toggle light state."""
        if self._is_on:
            self.off()
        else:
            self.on()
