"""
Mirror light controller with proximity sensor.

Turns on LED when presence is detected. Stays on while present,
turns off after timeout when no presence detected.
"""
from machine import Pin, time_pulse_us
from time import sleep, sleep_us, ticks_ms, ticks_diff


TRIGGER_PIN = 13
ECHO_PIN = 12
LED_PIN = 2

MAX_DISTANCE_CM = 80
TIMEOUT_SECONDS = 5


def measure_distance() -> float:
    """
    Measure distance using AJ-SR04M ultrasonic sensor.

    Returns:
        Distance in centimeters, or -1 if invalid reading.
    """
    trigger = Pin(TRIGGER_PIN, Pin.OUT)
    echo = Pin(ECHO_PIN, Pin.IN)

    trigger.off()
    sleep_us(2)
    trigger.on()
    sleep_us(10)
    trigger.off()

    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return -1

    distance_cm = (duration / 2) / 29.1
    return distance_cm


def is_presence_detected(distance: float) -> bool:
    """
    Check if distance indicates presence.

    Args:
        distance: Measured distance in cm.

    Returns:
        True if presence detected within range.
    """
    if distance < 0:
        return False
    return distance < MAX_DISTANCE_CM


def run() -> None:
    """
    Main loop: monitor proximity and control LED with timeout.
    """
    led = Pin(LED_PIN, Pin.OUT)
    led.off()

    last_presence_time = 0
    light_on = False
    timeout_ms = TIMEOUT_SECONDS * 1000

    print(f"Mirror light ready")
    print(f"  Detection: <{MAX_DISTANCE_CM}cm")
    print(f"  Timeout: {TIMEOUT_SECONDS}s")

    while True:
        distance = measure_distance()
        current_time = ticks_ms()

        if is_presence_detected(distance):
            last_presence_time = current_time
            if not light_on:
                led.on()
                light_on = True
                print(f"Light ON - presence at {distance:.0f}cm")
        else:
            if light_on:
                elapsed = ticks_diff(current_time, last_presence_time)
                if elapsed > timeout_ms:
                    led.off()
                    light_on = False
                    print(f"Light OFF - no presence for {TIMEOUT_SECONDS}s")

        sleep(0.15)


if __name__ == "__main__":
    run()
