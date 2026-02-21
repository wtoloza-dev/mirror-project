#!/usr/bin/env python3
"""
Simulator for testing without ESP32.

Mocks hardware modules and simulates sensor readings.
"""
import sys
import time
import random
from unittest.mock import MagicMock

sys.path.insert(0, str(__file__).replace("scripts/simulate.py", "src"))

machine_mock = MagicMock()
machine_mock.Pin = MagicMock
machine_mock.time_pulse_us = MagicMock(return_value=1000)
machine_mock.lightsleep = MagicMock()
machine_mock.deepsleep = MagicMock()
sys.modules["machine"] = machine_mock


class SimulatedSensor:
    """Simulates ultrasonic sensor readings."""

    def __init__(self) -> None:
        self._base_distance = 100.0
        self._presence = False

    def measure(self) -> float:
        """Return simulated distance."""
        if self._presence:
            return random.uniform(15.0, 25.0)
        return random.uniform(80.0, 120.0)

    def set_presence(self, present: bool) -> None:
        """Simulate presence or absence."""
        self._presence = present


class SimulatedLight:
    """Simulates LED output."""

    def __init__(self) -> None:
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    def on(self) -> None:
        if not self._is_on:
            print("💡 LED ON")
            self._is_on = True

    def off(self) -> None:
        if self._is_on:
            print("   LED OFF")
            self._is_on = False


def run_simulation() -> None:
    """Run interactive simulation."""
    from lib.presence import PresenceDetector

    sensor = SimulatedSensor()
    light = SimulatedLight()

    detector = PresenceDetector(
        activation_ms=1500,
        timeout_ms=5000,
        on_activate=light.on,
        on_deactivate=light.off,
    )

    print("=" * 50)
    print("Mirror Light Simulator")
    print("=" * 50)
    print("Commands:")
    print("  p = Toggle presence (simulate someone approaching)")
    print("  q = Quit")
    print("=" * 50)
    print()

    presence = False

    import threading
    import select

    stop_event = threading.Event()

    def input_thread():
        nonlocal presence
        while not stop_event.is_set():
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                cmd = sys.stdin.readline().strip().lower()
                if cmd == "p":
                    presence = not presence
                    status = "PRESENT" if presence else "AWAY"
                    print(f"\n>>> Simulating: {status}\n")
                    sensor.set_presence(presence)
                elif cmd == "q":
                    stop_event.set()

    input_handler = threading.Thread(target=input_thread, daemon=True)
    input_handler.start()

    try:
        while not stop_event.is_set():
            distance = sensor.measure()
            is_present = distance < 30.0

            detector.update(is_present)

            status = f"Distance: {distance:5.1f}cm | State: {detector.state:10} | Light: {'ON ' if light.is_on else 'OFF'}"
            print(f"\r{status}", end="", flush=True)

            time.sleep(0.15)

    except KeyboardInterrupt:
        pass

    print("\n\nSimulation ended.")


if __name__ == "__main__":
    run_simulation()
