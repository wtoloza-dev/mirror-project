# Firmware Options

This project supports two firmware approaches. Choose based on your needs.

## Option 1: MicroPython (src/)

**Best for:** Learning, customization, offline operation

### Download Firmware

```bash
# ESP32-C3 (production)
curl -L -o firmware/esp32c3-micropython.bin \
  https://micropython.org/resources/firmware/ESP32_GENERIC_C3-20240222-v1.22.2.bin

# ESP32-WROOM (development board)
curl -L -o firmware/esp32-micropython.bin \
  https://micropython.org/resources/firmware/ESP32_GENERIC-20240222-v1.22.2.bin
```

### Flash

```bash
# Erase and flash
esptool.py --chip esp32c3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32c3 --port /dev/ttyUSB0 write_flash -z 0x0 firmware/esp32c3-micropython.bin

# Upload application
./scripts/upload.sh /dev/ttyUSB0 prod
```

---

## Option 2: ESPHome (esphome/)

**Best for:** Home Assistant integration, OTA updates, multi-device management

### No Pre-built Firmware

ESPHome compiles firmware specifically for your configuration.
There's no generic `.bin` to download.

### Compile & Flash

```bash
# Install ESPHome
pip install esphome

# Configure WiFi
cd esphome
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml

# Compile and flash
esphome run mirror-light.yaml
```

### OTA Updates

After first flash, updates go over WiFi:

```bash
esphome run mirror-light.yaml
# Select "Over The Air" when prompted
```

---

## Comparison

| Feature | MicroPython | ESPHome |
|---------|-------------|---------|
| **Firmware size** | ~1.5MB | ~400KB |
| **RAM usage** | Higher (interpreter) | Lower (native) |
| **Code** | Python (src/) | YAML config |
| **Updates** | USB cable | WiFi (OTA) |
| **Home Assistant** | Manual integration | Auto-discovery |
| **Web interface** | None | Built-in |
| **Debug** | Serial REPL | WiFi logs |
| **Offline** | Works fully | Needs WiFi setup |
| **Customization** | Unlimited | Limited to YAML |
| **Learning value** | High (programming) | Medium (config) |

## Recommendation

- **3 bathroom mirrors (production)**: ESPHome
- **Learning project**: MicroPython
- **No WiFi available**: MicroPython
- **Home Assistant user**: ESPHome
