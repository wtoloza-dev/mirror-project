# Shopping List - AliExpress

Updated list for 3 bathroom mirrors with VL53L0X sensor.

## Final Shopping List

### Sensors (x5 pack)

| Item | Search Term | Qty | Price |
|------|-------------|-----|-------|
| **VL53L0X ToF Sensor** | "VL53L0X time of flight sensor 5pcs" | 1 pack (5 pcs) | $21,480 COP |

### Microcontrollers

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| ESP32-C3 Super Mini (with pins) | "esp32 c3 super mini soldered" | 4 | $8,000 COP | $32,000 COP |

### Power Control

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| IRF520 MOSFET module | "irf520 mosfet module" | 3 | $2,000 COP | $6,000 COP |
| LM2596 Buck converter | "lm2596 dc dc step down" | 3 | $3,200 COP | $9,600 COP |

### LED Strips

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| 12V LED strip 1m warm white | "12v led strip 2835 warm white ip65" | 3 | $6,000 COP | $18,000 COP |

### Power Supply

| Item | Search Term | Qty | Unit | Total |
|------|-------------|-----|------|-------|
| 12V 2A DC adapter | "12v 2a dc adapter 5.5mm" | 3 | $12,000 COP | $36,000 COP |
| DC jack panel mount | "dc 5.5mm 2.1mm panel female" | 6 | $800 COP | $4,800 COP |

## Total Cost

```
VL53L0X sensors (5 pcs)      $21,480 COP
ESP32-C3 Super Mini (4 pcs)  $32,000 COP
IRF520 MOSFET (3 pcs)         $6,000 COP
LM2596 Buck converter (3)     $9,600 COP
LED Strip 1m (3 pcs)         $18,000 COP
12V 2A Adapter (3 pcs)       $36,000 COP
DC Jack panel (6 pcs)         $4,800 COP
────────────────────────────────────────
SUBTOTAL:                   $127,880 COP
Shipping (~15%):             $19,000 COP
────────────────────────────────────────
TOTAL:                     ~$147,000 COP (~$36 USD)
```

**Per mirror: ~$49,000 COP (~$12 USD)**

## You Already Have

- ✅ ESP32-WROOM (for prototyping)
- ✅ AJ-SR04M sensor (for prototyping)
- ✅ Waterproof connectors (50 pcs)
- ✅ 3D Printer

## VL53L0X vs AJ-SR04M Comparison

| Feature | VL53L0X | AJ-SR04M |
|---------|---------|----------|
| Price (5 pcs) | $21,480 COP | $82,441 COP |
| Size | 10x13mm | 45x20mm + cable |
| Min range | 3cm | 20cm |
| Max range | 200cm | 450cm |
| Waterproof | No (use sealed case) | Yes |
| Interface | I2C (2 wires) | Trigger/Echo (2 wires) |
| Best for | Indoor, bathroom sink | Outdoor, wet areas |

## Wiring Diagram (VL53L0X)

```
┌─────────────────┐
│  12V Adapter    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌────────────┐
│  LED  │  │   Buck     │
│ Strip │  │ 12V → 5V   │
│ (12V) │  └─────┬──────┘
└───┬───┘        │
    │       ┌────┴────┐
    │       │         │
    │       ▼         ▼
    │   ┌───────┐  ┌─────────┐
    │   │ESP32  │  │ VL53L0X │
    │   │ C3    │  │  (3.3V) │
    │   └───┬───┘  └────┬────┘
    │       │           │
    │       │    I2C    │
    │       │ SDA ◄────►│
    │       │ SCL ◄────►│
    │       │           │
    │   ┌───┴───┐       │
    │   │MOSFET │       │
    │   │IRF520 │       │
    │   └───┬───┘       │
    │       │           │
    └───────┘           │
                        │
```

## VL53L0X Connections

```
VL53L0X          ESP32-C3
-------          --------
VIN ──────────── 3.3V
GND ──────────── GND
SDA ──────────── GPIO8 (I2C SDA)
SCL ──────────── GPIO9 (I2C SCL)
```

**Note**: VL53L0X uses 3.3V, NOT 5V.

## Search Terms for AliExpress

```
"VL53L0X time of flight 5pcs"
"esp32 c3 super mini soldered headers"
"irf520 mosfet module"
"lm2596 dc dc step down"
"12v led strip 2835 warm white ip65 1m"
"12v 2a dc adapter 5.5mm"
"dc 5.5mm panel mount female"
```

## Assembly Checklist (per unit)

```
[ ] Wire buck converter: 12V in → 5V out
[ ] Wire ESP32-C3: 5V from buck (VIN), GND
[ ] Wire VL53L0X: 3.3V from ESP32, GND, SDA to GPIO8, SCL to GPIO9
[ ] Wire MOSFET: Gate to GPIO4, Source to GND, Drain to LED-
[ ] Wire LED strip: 12V+, LED- to MOSFET drain
[ ] Flash MicroPython to ESP32-C3
[ ] Upload main.py
[ ] Test activation
[ ] Mount in 3D printed enclosure
[ ] Seal with silicone (for bathroom with shower)
[ ] Install
```
