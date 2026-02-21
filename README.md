# Mirror Project

Contactless bathroom mirror light system using ESP32 and MicroPython. Lights turn on automatically when you approach the mirror using a proximity sensor.

## Features

- Contactless activation via proximity sensor
- ESP32-WROOM with MicroPython
- LED strip control
- Configurable distance threshold

## Hardware Requirements

- ESP32-WROOM or compatible
- Proximity sensor (HC-SR04, VL53L0X, or IR sensor)
- LED strip (WS2812B or similar)
- Power supply (5V for LEDs, 3.3V for ESP32)

## Software Requirements

- Python 3.14+
- uv (package manager)
- MicroPython v1.24+

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/wtoloza-dev/mirror-project.git
cd mirror-project
```

### 2. Install dependencies

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### 3. Flash MicroPython to ESP32

Download firmware from [micropython.org](https://micropython.org/download/ESP32_GENERIC/)

```bash
# Erase flash
uv run esptool --port /dev/ttyUSB0 erase-flash

# Flash MicroPython
uv run esptool --port /dev/ttyUSB0 --baud 460800 write-flash -z 0x1000 firmware/esp32-micropython.bin
```

### 4. Upload code to ESP32

```bash
uv run mpremote connect /dev/ttyUSB0 cp src/boot.py :boot.py
uv run mpremote connect /dev/ttyUSB0 cp src/main.py :main.py
uv run mpremote connect /dev/ttyUSB0 reset
```

## WSL2 Setup (Windows)

WSL2 requires USB passthrough via usbipd-win.

### Install usbipd (PowerShell Admin)

```powershell
winget install usbipd
```

### Connect ESP32 to WSL

```powershell
# List USB devices
usbipd list

# Bind device (first time only)
usbipd bind --busid <BUSID>

# Attach to WSL
usbipd attach --wsl --busid <BUSID>
```

**Note**: Run `usbipd attach` again after each ESP32 reset.

## Usage

### Interactive REPL

```bash
uv run mpremote connect /dev/ttyUSB0 repl
```

### List files on ESP32

```bash
uv run mpremote connect /dev/ttyUSB0 ls
```

### Run script

```bash
uv run mpremote connect /dev/ttyUSB0 run src/main.py
```

## Project Structure

```
mirror-project/
├── src/
│   ├── boot.py          # Boot configuration
│   └── main.py          # Main application
├── lib/                 # MicroPython libraries
├── firmware/            # MicroPython firmware
├── scripts/             # Utility scripts
├── platformio.ini       # PlatformIO config (optional)
└── pyproject.toml       # Project configuration
```

## License

MIT
