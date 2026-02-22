# Mirror Project

Contactless bathroom mirror light system using ESP32 and MicroPython.

## Features

- Contactless activation via proximity sensor
- Configurable activation delay and timeout
- **Modular, reusable architecture** - sensors are decoupled and portable
- Factory Pattern for sensor instantiation
- Single-file deployment for production

## Quick Start

```bash
# Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Build and upload
uv run python scripts/build.py
uv run mpremote connect /dev/ttyUSB0 cp build/main.py :main.py
```

## Project Architecture

```
src/
├── config.py              # Configuration (pins, timing, sensor type)
├── main.py                # Application entry point
├── boot.py                # MicroPython boot sequence
│
├── hardware/              # Hardware abstraction (reusable)
│   └── sensors/           # ← Copy this folder to any project
│       ├── base.py        # Abstract base class (DistanceSensor)
│       ├── factory.py     # Factory Pattern for sensor creation
│       ├── ultrasonic.py  # HC-SR04, AJ-SR04M driver
│       └── vl53l0x.py     # VL53L0X ToF driver
│
└── core/                  # Application logic
    ├── light.py           # LED/relay controller
    ├── presence.py        # State machine
    └── power.py           # Sleep management
```

### Reusing Sensors in Other Projects

```python
# Copy hardware/sensors/ folder to your project, then:
from hardware.sensors import SensorFactory

# Create any registered sensor
sensor = SensorFactory.create("vl53l0x", sda_pin=8, scl_pin=9)
# or
sensor = SensorFactory.create("ultrasonic", trigger_pin=13, echo_pin=12)

distance = sensor.measure()  # Returns cm or -1 on error
```

### Adding New Sensors

1. Create file in `hardware/sensors/` (e.g., `my_sensor.py`)
2. Inherit from `DistanceSensor` and implement `measure()`
3. Register with `@SensorFactory.register("my_sensor")`
4. Import in `hardware/sensors/__init__.py`

## Development Mode

Edit source files in `src/` with full IDE support and type hints.

```bash
# Upload full structure (for debugging)
./scripts/upload.sh /dev/ttyUSB0 dev

# Run tests without hardware
uv run pytest tests/

# Simulate without ESP32
uv run python scripts/simulate.py
```

### Configuration

Edit `src/config.py`:

```python
class SensorConfig:
    SENSOR_TYPE: str = "vl53l0x"  # or "ultrasonic"
    MAX_DISTANCE_CM: float = 60.0
    MIN_DISTANCE_CM: float = 3.0

class TimingConfig:
    ACTIVATION_MS: int = 1500   # Time to activate (ms)
    TIMEOUT_MS: int = 5000      # Time to deactivate (ms)
```

## Production Mode

Build combines all files into single `main.py` for deployment.

```bash
# 1. Build single file
uv run python scripts/build.py

# 2. Upload to ESP32
./scripts/upload.sh /dev/ttyUSB0 prod

# Or manually:
uv run mpremote connect /dev/ttyUSB0 cp build/main.py :main.py
uv run mpremote connect /dev/ttyUSB0 cp src/boot.py :boot.py
uv run mpremote connect /dev/ttyUSB0 reset
```

### Enable Light Sleep (saves ~60% power)

Edit `src/config.py`:

```python
class PowerConfig:
    USE_LIGHT_SLEEP: bool = True  # Enable for production
```

**Note**: Light sleep disables serial REPL. To reprogram, enter bootloader mode (hold BOOT + press EN).

## Testing Without Hardware

### Simulation Mode

```bash
uv run python scripts/simulate.py
```

Simulates sensor readings and state machine without ESP32.

### Unit Tests

```bash
uv run pytest tests/ -v
```

## WSL2 Setup (Windows)

```powershell
# Install usbipd (PowerShell Admin)
winget install usbipd

# Connect ESP32 to WSL
usbipd list
usbipd bind --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

**After each ESP32 reset**, reconnect:
```powershell
usbipd attach --wsl --busid <BUSID>
```

## Hardware

See [HARDWARE.md](HARDWARE.md) for wiring and components.

## Documentation

- [HARDWARE.md](HARDWARE.md) - Wiring and components
- [docs/LEARNING.md](docs/LEARNING.md) - How everything works
- [docs/POWER.md](docs/POWER.md) - Power consumption analysis
- [docs/SHOPPING.md](docs/SHOPPING.md) - AliExpress shopping list
- [docs/PRODUCTION.md](docs/PRODUCTION.md) - Production deployment

## License

MIT
