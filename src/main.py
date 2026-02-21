"""
Mirror light controller with proximity sensor.

Turns on LED after sustained presence is detected.
Stays on while present, turns off after timeout.
"""
from machine import Pin, time_pulse_us
from time import sleep, sleep_us, ticks_ms, ticks_diff


TRIGGER_PIN = 13
ECHO_PIN = 12
LED_PIN = 2

MAX_DISTANCE_CM = 30
ACTIVATION_SECONDS = 1.5
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
    Main loop: monitor proximity and control LED with activation delay and timeout.
    """
    led = Pin(LED_PIN, Pin.OUT)
    led.off()

    presence_start_time = 0
    last_presence_time = 0
    light_on = False
    presence_active = False

    activation_ms = int(ACTIVATION_SECONDS * 1000)
    timeout_ms = int(TIMEOUT_SECONDS * 1000)

    print(f"Mirror light ready")
    print(f"  Detection: <{MAX_DISTANCE_CM}cm")
    print(f"  Activation: {ACTIVATION_SECONDS}s")
    print(f"  Timeout: {TIMEOUT_SECONDS}s")

    while True:
        distance = measure_distance()
        current_time = ticks_ms()
        presence = is_presence_detected(distance)

        if presence:
            last_presence_time = current_time

            if not presence_active:
                presence_start_time = current_time
                presence_active = True

            presence_duration = ticks_diff(current_time, presence_start_time)

            if not light_on and presence_duration >= activation_ms:
                led.on()
                light_on = True
                print(f"Light ON - presence at {distance:.0f}cm for {ACTIVATION_SECONDS}s")
        else:
            presence_active = False

            if light_on:
                elapsed = ticks_diff(current_time, last_presence_time)
                if elapsed > timeout_ms:
                    led.off()
                    light_on = False
                    print(f"Light OFF - no presence for {TIMEOUT_SECONDS}s")

        sleep(0.15)


if __name__ == "__main__":
    run()
