"""
MicroPython main application entry point.

This file runs after boot.py on every boot.
"""
from machine import Pin
from time import sleep


def blink_led(pin: int = 2, interval: float = 0.5) -> None:
    """
    Blink the onboard LED.

    Args:
        pin: GPIO pin number for the LED (default 2 for most ESP32 boards).
        interval: Time in seconds between state changes.
    """
    led = Pin(pin, Pin.OUT)
    while True:
        led.value(not led.value())
        sleep(interval)


if __name__ == "__main__":
    print("Mirror Project - ESP32 MicroPython")
    blink_led()
