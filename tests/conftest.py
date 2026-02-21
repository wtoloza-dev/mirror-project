"""Pytest configuration and fixtures."""
import sys
from unittest.mock import MagicMock

machine_mock = MagicMock()
machine_mock.Pin = MagicMock
machine_mock.time_pulse_us = MagicMock(return_value=1000)
machine_mock.lightsleep = MagicMock()
machine_mock.deepsleep = MagicMock()
sys.modules["machine"] = machine_mock

_current_ticks = [0]


def mock_ticks_ms():
    return _current_ticks[0]


def mock_ticks_diff(a, b):
    return a - b


def mock_sleep(s):
    _current_ticks[0] += int(s * 1000)


def mock_sleep_ms(ms):
    _current_ticks[0] += ms


def advance_time(ms: int):
    _current_ticks[0] += ms


def reset_time():
    _current_ticks[0] = 0


time_mock = MagicMock()
time_mock.ticks_ms = mock_ticks_ms
time_mock.ticks_diff = mock_ticks_diff
time_mock.sleep = mock_sleep
time_mock.sleep_ms = mock_sleep_ms
time_mock.sleep_us = MagicMock()
sys.modules["time"] = time_mock

sys.path.insert(0, "src")
