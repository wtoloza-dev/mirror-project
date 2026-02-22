#!/bin/bash
# Script to upload MicroPython files to ESP32
# Usage: ./scripts/upload.sh [port]
#
# Modes:
#   Development mode - uploads full folder structure
#   Production mode  - upload single built file (build/main.py)

set -e

PORT="${1:-/dev/ttyUSB0}"
MODE="${2:-dev}"

echo "Uploading to ESP32 on $PORT (mode: $MODE)..."

if [ "$MODE" = "prod" ]; then
    # Production: single file deployment
    if [ ! -f "build/main.py" ]; then
        echo "Error: build/main.py not found. Run: uv run python scripts/build.py"
        exit 1
    fi
    uv run mpremote connect "$PORT" cp build/main.py :main.py
    uv run mpremote connect "$PORT" cp src/boot.py :boot.py
else
    # Development: full folder structure
    echo "Creating directory structure..."
    uv run mpremote connect "$PORT" mkdir :hardware 2>/dev/null || true
    uv run mpremote connect "$PORT" mkdir :hardware/sensors 2>/dev/null || true
    uv run mpremote connect "$PORT" mkdir :core 2>/dev/null || true
    
    echo "Uploading config..."
    uv run mpremote connect "$PORT" cp src/config.py :config.py
    uv run mpremote connect "$PORT" cp src/boot.py :boot.py
    
    echo "Uploading hardware/sensors..."
    uv run mpremote connect "$PORT" cp src/hardware/__init__.py :hardware/__init__.py
    uv run mpremote connect "$PORT" cp src/hardware/sensors/__init__.py :hardware/sensors/__init__.py
    uv run mpremote connect "$PORT" cp src/hardware/sensors/base.py :hardware/sensors/base.py
    uv run mpremote connect "$PORT" cp src/hardware/sensors/factory.py :hardware/sensors/factory.py
    uv run mpremote connect "$PORT" cp src/hardware/sensors/ultrasonic.py :hardware/sensors/ultrasonic.py
    uv run mpremote connect "$PORT" cp src/hardware/sensors/vl53l0x.py :hardware/sensors/vl53l0x.py
    
    echo "Uploading core..."
    uv run mpremote connect "$PORT" cp src/core/__init__.py :core/__init__.py
    uv run mpremote connect "$PORT" cp src/core/light.py :core/light.py
    uv run mpremote connect "$PORT" cp src/core/presence.py :core/presence.py
    uv run mpremote connect "$PORT" cp src/core/power.py :core/power.py
    
    echo "Uploading main.py..."
    uv run mpremote connect "$PORT" cp src/main.py :main.py
fi

echo "Upload complete! Resetting device..."
uv run mpremote connect "$PORT" reset

echo "Done! Connect with: uv run mpremote connect $PORT repl"
