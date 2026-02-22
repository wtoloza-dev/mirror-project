# Mirror Project

Contactless bathroom mirror light system using ESP32.

## Two Approaches Available

| Approach | Best For | Folder |
|----------|----------|--------|
| **MicroPython** | Learning, customization, offline | `src/` |
| **ESPHome** | Production, Home Assistant, OTA | `esphome/` |

See [firmware/README.md](firmware/README.md) for detailed comparison.

---

## Quick Start - MicroPython

```bash
# Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Build and upload
uv run python scripts/build.py
uv run mpremote connect /dev/ttyUSB0 cp build/main.py :main.py
```

## Quick Start - ESPHome

```bash
pip install esphome
cd esphome
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with WiFi credentials
esphome run mirror-light.yaml
```

---

## MicroPython Architecture

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

sensor = SensorFactory.create("vl53l0x", sda_pin=8, scl_pin=9)
distance = sensor.measure()  # Returns cm or -1 on error
```

### Adding New Sensors

1. Create file in `hardware/sensors/` (e.g., `my_sensor.py`)
2. Inherit from `DistanceSensor` and implement `measure()`
3. Register with `@SensorFactory.register("my_sensor")`
4. Import in `hardware/sensors/__init__.py`

## Development Mode

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

```bash
# 1. Build single file
uv run python scripts/build.py

# 2. Upload to ESP32
./scripts/upload.sh /dev/ttyUSB0 prod
```

### Enable Light Sleep (saves ~60% power)

```python
class PowerConfig:
    USE_LIGHT_SLEEP: bool = True  # Enable for production
```

**Note**: Light sleep disables serial REPL. To reprogram, hold BOOT + press EN.

## Testing Without Hardware

```bash
# Simulation
uv run python scripts/simulate.py

# Unit tests
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

## Documentation

- [HARDWARE.md](HARDWARE.md) - Wiring and components
- [firmware/README.md](firmware/README.md) - Firmware comparison
- [esphome/README.md](esphome/README.md) - ESPHome guide
- [docs/LEARNING.md](docs/LEARNING.md) - How everything works
- [docs/POWER.md](docs/POWER.md) - Power consumption analysis
- [docs/SHOPPING.md](docs/SHOPPING.md) - AliExpress shopping list
- [docs/PRODUCTION.md](docs/PRODUCTION.md) - Production deployment

## License

MIT
