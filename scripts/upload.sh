#!/bin/bash
# Script to upload MicroPython files to ESP32
# Usage: ./scripts/upload.sh [port]

set -e

PORT="${1:-/dev/ttyUSB0}"

echo "Uploading files to ESP32 on $PORT..."

# Upload boot.py
uv run mpremote connect "$PORT" cp src/boot.py :boot.py

# Upload main.py
uv run mpremote connect "$PORT" cp src/main.py :main.py

# Upload lib folder if exists and not empty
if [ -d "lib" ] && [ "$(ls -A lib 2>/dev/null)" ]; then
    echo "Uploading libraries..."
    for file in lib/*.py; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            uv run mpremote connect "$PORT" cp "$file" ":lib/$filename"
        fi
    done
fi

echo "Upload complete! Resetting device..."
uv run mpremote connect "$PORT" reset

echo "Done! Connect with: uv run mpremote connect $PORT repl"
