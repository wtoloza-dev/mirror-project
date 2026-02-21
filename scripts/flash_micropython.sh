#!/bin/bash
# Script to flash MicroPython firmware to ESP32
# Usage: ./scripts/flash_micropython.sh [port] [firmware.bin]

set -e

PORT="${1:-/dev/ttyUSB0}"
FIRMWARE="${2:-}"

if [ -z "$FIRMWARE" ]; then
    echo "Usage: $0 [port] <firmware.bin>"
    echo "Example: $0 /dev/ttyUSB0 esp32-20240222-v1.22.2.bin"
    echo ""
    echo "Download MicroPython firmware from:"
    echo "  https://micropython.org/download/ESP32_GENERIC/"
    exit 1
fi

echo "Erasing flash on $PORT..."
uv run esptool --port "$PORT" erase_flash

echo "Flashing MicroPython firmware..."
uv run esptool --port "$PORT" --baud 460800 write_flash -z 0x1000 "$FIRMWARE"

echo "Done! Connect with: uv run mpremote connect $PORT"
