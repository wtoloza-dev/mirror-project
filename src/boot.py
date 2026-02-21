"""
MicroPython boot configuration.

Runs before main.py on every boot.
"""
import gc


def setup() -> None:
    """Perform boot-time initialization."""
    gc.collect()
    _disable_debug_output()


def _disable_debug_output() -> None:
    """Disable REPL on UART0 if needed for production."""
    pass


setup()
