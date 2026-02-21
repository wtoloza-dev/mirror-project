# Production Hardware - 3 Bathroom Mirrors

## Philosophy

```
Prototype: ESP32-WROOM + MicroPython (what you have)
     ↓
Test & iterate until logic is perfect
     ↓
Production: Smaller chip (ESP32-C3 or ESP8266)
     ↓
Optional: Transcribe to C if needed (probably not)
```

## Production Chip Options

| Chip | MicroPython | Size | Price | Power | Recommendation |
|------|-------------|------|-------|-------|----------------|
| ESP32-WROOM | ✅ Yes | 25x18mm | $4 | 50mA | Overkill |
| **ESP32-C3** | ✅ Yes | 21x18mm | $2.50 | 35mA | **Best choice** |
| ESP8266 | ✅ Yes | 25x15mm | $2 | 70mA | Older, more power |
| ATtiny85 | ❌ No | 8x8mm | $0.80 | 5mA | Needs C, harder |

**Winner: ESP32-C3 Mini** - Same code runs, smaller, cheaper, modern.

## Shopping List for 3 Mirrors

### Core Components (x3)

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| ESP32-C3 Super Mini | "esp32 c3 super mini" | 3 | $2.00 | $6.00 |
| AJ-SR04M sensor | "aj-sr04m waterproof ultrasonic" | 3 | $2.50 | $7.50 |
| IRF520 MOSFET module | "irf520 mosfet module" | 3 | $0.50 | $1.50 |
| LM2596 buck converter | "lm2596 dc dc step down" | 3 | $0.80 | $2.40 |

### LED Strips (x3)

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| 12V LED strip 1m warm white | "12v led strip 2835 warm white ip65" | 3 | $1.50 | $4.50 |

### Power (x3)

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| 12V 2A adapter | "12v 2a dc adapter 5.5mm" | 3 | $3.00 | $9.00 |
| DC jack panel mount | "dc 5.5mm 2.1mm panel female" | 6 | $0.20 | $1.20 |

### Connectors & Cables (shared)

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| Dupont wires 20cm kit | "dupont wire male female kit" | 1 | $2.00 | $2.00 |
| JST XH 2-pin connectors | "jst xh 2pin connector" | 20 | $0.10 | $2.00 |
| JST XH 4-pin connectors | "jst xh 4pin connector" | 10 | $0.15 | $1.50 |
| Heat shrink kit | "heat shrink tubing assortment" | 1 | $1.50 | $1.50 |
| 22AWG wire (red+black) | "22awg silicone wire red black" | 1 | $2.00 | $2.00 |

### Extras (backup/testing)

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| ESP32-C3 extra | "esp32 c3 super mini" | 1 | $2.00 | $2.00 |
| AJ-SR04M extra | "aj-sr04m" | 1 | $2.50 | $2.50 |
| Prototype PCB 5x7cm | "pcb prototype board 5x7" | 5 | $0.30 | $1.50 |

## Total Cost

```
Core (x3):           $17.40
LEDs (x3):            $4.50
Power (x3):          $10.20
Connectors:           $9.00
Extras:               $6.00
─────────────────────────────
SUBTOTAL:           $47.10
Shipping (~15%):     $7.00
─────────────────────────────
TOTAL:              ~$55 USD
```

**Per mirror: ~$18 USD** (including spares and shipping)

## ESP32-C3 Super Mini Pinout

```
         ┌─────────────┐
    3.3V │●           ●│ GND
     IO0 │●           ●│ IO1
     IO2 │●  ESP32-C3 ●│ IO3
     IO4 │●   Super   ●│ IO5
     IO6 │●   Mini    ●│ IO7
     IO8 │●           ●│ IO9
    IO10 │●           ●│ RX
      5V │●           ●│ TX
         └─────────────┘
```

**Your connections on C3:**
- IO4 → MOSFET Gate (LED control)
- IO5 → Sensor TRIG  
- IO6 → Sensor ECHO
- 5V → Buck converter input
- GND → Common ground

## Code Changes for ESP32-C3

Only change pin numbers:

```python
# Old (ESP32-WROOM)
TRIGGER_PIN = 13
ECHO_PIN = 12
LED_PIN = 2

# New (ESP32-C3)
TRIGGER_PIN = 5
ECHO_PIN = 6
LED_PIN = 4
```

Everything else stays the same. MicroPython is portable.

## Production Wiring (per mirror)

```
┌──────────────────────────────────────────────────────────┐
│                     12V DC Adapter                       │
└────────────────────────┬─────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               │               ▼
   ┌──────────┐          │        ┌──────────────┐
   │ LED Strip│          │        │Buck Converter│
   │   12V    │          │        │  12V → 5V    │
   └────┬─────┘          │        └──────┬───────┘
        │                │               │
        │       ┌────────┴────────┐      │
        │       │     MOSFET      │      │
        │       │     IRF520      │      │
        │       └────────┬────────┘      │
        │                │               │
        └────────────────┤               │
                         │               │
                ┌────────┴───────────────┴────┐
                │        ESP32-C3             │
                │   IO5 → Sensor TRIG         │
                │   IO6 ← Sensor ECHO         │
                │   IO4 → MOSFET Gate         │
                └─────────────┬───────────────┘
                              │
                      ┌───────┴───────┐
                      │   AJ-SR04M    │
                      │    (5V)       │
                      └───────────────┘
```

## Assembly Checklist (per unit)

```
[ ] Solder headers to ESP32-C3
[ ] Wire buck converter: 12V in → 5V out
[ ] Test buck converter output (should read 5V)
[ ] Wire ESP32: 5V from buck, GND common
[ ] Wire MOSFET: Gate to IO4, Source to GND, Drain to LED-
[ ] Wire LED strip: 12V+, LED- to MOSFET drain
[ ] Wire sensor: 5V (from 12V rail), GND, TRIG to IO5, ECHO to IO6
[ ] Flash MicroPython to ESP32-C3
[ ] Upload main.py (with updated pins)
[ ] Test activation
[ ] Mount in 3D printed enclosure
[ ] Install in bathroom
```

## Transcribing to C (If Needed Later)

You likely won't need this, but options exist:

### Option 1: Arduino Framework (Easiest)

Same logic, C++ syntax:

```cpp
#define TRIGGER_PIN 5
#define ECHO_PIN 6
#define LED_PIN 4

void setup() {
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    float distance = measureDistance();
    // ... same logic
}
```

### Option 2: ESP-IDF (Most Control)

Native Espressif SDK. More complex but smallest binary.

### Option 3: Cython/mypyc (Python to C)

Python 3.14 has improvements but this doesn't apply to MicroPython.
MicroPython runs on the chip - your PC's Python version doesn't matter.

**Reality check**: For this project, MicroPython on ESP32-C3 is perfectly fine.
Transcribe to C only if you need:
- Faster response (<1ms) - you don't
- Lower power (<1mA) - you don't  
- Smaller binary - C3 has 4MB flash, plenty

## Timeline

```
Week 1-4:   Parts shipping from AliExpress
            Design 3D enclosures
            Perfect prototype code

Week 5:     Receive parts
            Test ESP32-C3 with your code
            Adjust pin numbers

Week 6:     Assemble 3 units
            Flash and test each

Week 7:     Install in bathrooms
            Final adjustments
```

## Files Summary

After this project, your repo has:

```
mirror-project/
├── src/
│   ├── boot.py           # Boot config
│   ├── main.py           # Main logic (prototype pins)
│   └── main_c3.py        # Main logic (C3 pins) [create later]
├── docs/
│   ├── LEARNING.md       # How everything works
│   ├── POWER.md          # Electricity consumption
│   ├── SHOPPING.md       # Component options
│   └── PRODUCTION.md     # This file
├── hardware/
│   └── enclosure.stl     # 3D print files [create later]
├── HARDWARE.md           # Hardware specs
└── README.md             # Project overview
```
