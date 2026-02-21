"""
Mirror light controller with proximity sensor.

Turns on LED when presence is detected within threshold distance.
"""
from machine import Pin, time_pulse_us
from time import sleep, sleep_us


TRIGGER_PIN = 13
ECHO_PIN = 12
LED_PIN = 2
DISTANCE_THRESHOLD_CM = 50
TIMEOUT_US = 30000


def measure_distance() -> float:
    """
    Measure distance using AJ-SR04M ultrasonic sensor.

    Returns:
        Distance in centimeters, or -1 if timeout.
    """
    trigger = Pin(TRIGGER_PIN, Pin.OUT)
    echo = Pin(ECHO_PIN, Pin.IN)

    trigger.off()
    sleep_us(2)
    trigger.on()
    sleep_us(10)
    trigger.off()

    duration = time_pulse_us(echo, 1, TIMEOUT_US)

    if duration < 0:
        return -1

    distance_cm = (duration / 2) / 29.1
    return distance_cm


def run() -> None:
    """
    Main loop: monitor proximity and control LED.
    """
    led = Pin(LED_PIN, Pin.OUT)
    led.off()

    print(f"Mirror light ready. Threshold: {DISTANCE_THRESHOLD_CM}cm")

    while True:
        distance = measure_distance()

        if 0 < distance < DISTANCE_THRESHOLD_CM:
            led.on()
            print(f"Presence detected: {distance:.1f}cm - LED ON")
        else:
            led.off()
            if distance > 0:
                print(f"No presence: {distance:.1f}cm - LED OFF")

        sleep(0.2)


if __name__ == "__main__":
    run()
