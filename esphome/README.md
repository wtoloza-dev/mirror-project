# ESPHome Version

Alternative implementation using ESPHome instead of MicroPython.

## Comparison

| Aspect | MicroPython (src/) | ESPHome |
|--------|-------------------|---------|
| Code | 12 Python files | 1 YAML file |
| Size | ~21KB | ~400KB compiled |
| Speed | Interpreted | Native C++ |
| Updates | USB required | OTA via WiFi |
| Debug | Serial REPL | Web logs + WiFi |
| Home Assistant | Manual | Automatic |
| Learning | Architecture patterns | YAML config |

## Quick Start

### 1. Install ESPHome

```bash
# Using pip
pip install esphome

# Or using Docker
docker pull esphome/esphome
```

### 2. Configure secrets

```bash
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your WiFi credentials
```

### 3. First flash (USB required)

```bash
# Compile and upload
esphome run mirror-light.yaml

# Or step by step:
esphome compile mirror-light.yaml
esphome upload mirror-light.yaml --device /dev/ttyUSB0
```

### 4. Subsequent updates (OTA)

```bash
# After first flash, updates go over WiFi
esphome run mirror-light.yaml
# Select OTA when prompted
```

## Multiple Mirrors

For 3 bathrooms, create copies with different names:

```bash
cp mirror-light.yaml bathroom1.yaml
cp mirror-light.yaml bathroom2.yaml
cp mirror-light.yaml bathroom3.yaml
```

Edit each file's `name:` field:
- `name: bathroom1-mirror`
- `name: bathroom2-mirror`
- `name: bathroom3-mirror`

## Home Assistant Integration

ESPHome devices are auto-discovered by Home Assistant.

1. Go to Settings → Devices & Services
2. ESPHome integration should show your device
3. Click Configure and enter your API key

## Web Interface

Each device has a local web server at:
- `http://mirror-light.local` (mDNS)
- `http://<device-ip>` (direct IP)

Features:
- Real-time sensor values
- Manual light control
- Logs viewer

## Wiring

Same as MicroPython version:

```
ESP32-C3          VL53L0X
--------          -------
3.3V      ───────  VIN
GND       ───────  GND
GPIO8     ───────  SDA
GPIO9     ───────  SCL

ESP32-C3          LED/MOSFET
--------          ----------
GPIO4     ───────  Gate/Signal
GND       ───────  GND (common)
```

## Customization

### Change timing

Edit `filters:` in the `binary_sensor:` section:

```yaml
filters:
  - delayed_on: 2000ms   # Activation delay
  - delayed_off: 10000ms # Timeout
```

### Change distance range

Edit the `lambda:` condition:

```yaml
lambda: |-
  float dist = id(distance_sensor).state;
  return dist > 5 && dist < 80;  # 5cm - 80cm
```

### Use ultrasonic sensor instead

Replace the `sensor:` section:

```yaml
sensor:
  - platform: ultrasonic
    trigger_pin: 13
    echo_pin: 12
    name: "Distance"
    id: distance_sensor
    update_interval: 150ms
```

## Troubleshooting

### Device not found
```bash
# List available ports
esphome upload mirror-light.yaml --device /dev/ttyUSB0
```

### WiFi won't connect
Device creates fallback hotspot:
- SSID: `Mirror-Light-Fallback`
- Password: `mirror123`

Connect and access `http://192.168.4.1` to reconfigure.

### Logs
```bash
esphome logs mirror-light.yaml
```
