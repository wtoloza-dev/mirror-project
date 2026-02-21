# Hardware

## Current Setup

| Component | Model | Notes |
|-----------|-------|-------|
| Microcontroller | ESP32-WROOM | Overkill for this project, but works great |
| Proximity Sensor | AJ-SR04M | Waterproof ultrasonic sensor, ideal for bathrooms |
| LED Strip | TBD | |
| Power Supply | TBD | |

### AJ-SR04M Specifications

- Voltage: 3.3V - 5.5V
- Range: 20cm - 450cm
- Waterproof: IP67
- Interface: UART or Trigger/Echo

### ESP32-WROOM Specifications

- CPU: Dual-core 240MHz
- RAM: 520KB
- Flash: 4MB
- Wi-Fi: 802.11 b/g/n
- Bluetooth: 4.2 + BLE
- GPIO: 34 pins

## Minimum Recommended

For a simple mirror light project, you don't need all ESP32 features.

| Component | Model | Price (approx) |
|-----------|-------|----------------|
| Microcontroller | ESP8266 (NodeMCU/Wemos D1 Mini) | $3-5 |
| Proximity Sensor | HC-SR04 or AJ-SR04M | $2-5 |
| LED Strip | WS2812B (30 LEDs/m) | $5-10 |
| Power Supply | 5V 2A | $3-5 |

### Why ESP8266 is enough

- Single purpose: detect proximity + control LEDs
- No Bluetooth needed
- No dual-core needed
- Cheaper and smaller
- MicroPython compatible

### Even simpler alternative

For the most basic setup without Wi-Fi:

| Component | Model | Price (approx) |
|-----------|-------|----------------|
| Microcontroller | ATtiny85 or Arduino Nano | $2-3 |
| Proximity Sensor | HC-SR04 | $2 |
| LED Strip | Simple 12V LED strip with MOSFET | $3-5 |
| Power Supply | 12V 1A | $3 |

**Trade-off**: No OTA updates, no remote control, harder to program.

## Wiring Diagram

```
ESP32/ESP8266          AJ-SR04M
-----------            --------
3.3V  ────────────────  VCC
GND   ────────────────  GND
GPIO5 ────────────────  TRIG
GPIO4 ────────────────  ECHO

ESP32/ESP8266          LED Strip (WS2812B)
-----------            -------------------
5V    ────────────────  VCC (from power supply)
GND   ────────────────  GND
GPIO2 ────────────────  DIN
```

## Power Considerations

- ESP32/ESP8266: 3.3V logic, can be powered via USB or 5V VIN
- AJ-SR04M: Works with 3.3V (unlike HC-SR04 which needs 5V)
- WS2812B LEDs: 5V, ~60mA per LED at full brightness
- For 30 LEDs: 5V 2A power supply recommended
