# Shopping List - AliExpress

Complete list for permanent mirror light installation.

## Option A: Minimal (What You Have + Essentials)

You already have:
- ✅ ESP32-WROOM
- ✅ AJ-SR04M sensor

Need to buy:

| Item | Search Term | Qty | Price |
|------|-------------|-----|-------|
| USB adapter 5V 1A | "5v 1a usb adapter" | 1 | $1-2 |
| Micro USB cable (long) | "micro usb cable 2m" | 1 | $1 |
| Dupont wires | "dupont wire female female 20cm" | 1 pack | $1 |
| MOSFET module | "irf520 mosfet module" | 1 | $0.50 |
| 12V adapter | "12v 1a dc adapter 5.5mm" | 1 | $2-3 |

**Total: ~$6-8 USD**

## Option B: Full Build (Better Quality)

### Microcontroller

| Item | Search Term | Price | Notes |
|------|-------------|-------|-------|
| ESP32-WROOM-32 DevKit | "esp32 devkit v1" | $3-4 | Same as yours |
| **OR** ESP32-C3 Mini | "esp32 c3 mini" | $2-3 | Smaller, newer, enough for this |
| **OR** Wemos D1 Mini | "wemos d1 mini esp8266" | $2 | Cheapest, less features |

**Recommendation**: ESP32-C3 Mini - smaller, cheaper, modern.

### Sensor

| Item | Search Term | Price | Notes |
|------|-------------|-------|-------|
| AJ-SR04M | "aj-sr04m waterproof" | $2-3 | What you have, waterproof |
| **OR** JSN-SR04T | "jsn-sr04t waterproof" | $2-3 | Same but different brand |
| **OR** HC-SR04 | "hc-sr04 ultrasonic" | $0.80 | Cheaper but NOT waterproof |

**Recommendation**: Keep AJ-SR04M for bathroom (humidity resistant).

### LED Options

#### Option 1: Simple LED Strip (Recommended)

| Item | Search Term | Price | Notes |
|------|-------------|-------|-------|
| 12V LED strip warm white | "12v led strip warm white 2835 1m" | $1-2 | Simple, no controller needed |
| MOSFET module IRF520 | "irf520 mosfet module" | $0.50 | To control 12V from ESP32 |
| 12V 2A adapter | "12v 2a adapter 5.5mm" | $3-4 | Powers both LEDs and ESP32 |
| DC-DC buck converter | "lm2596 dc dc converter" | $0.80 | 12V → 5V for ESP32 |

**Wiring:**
```
12V Adapter → LED Strip (via MOSFET)
           → Buck converter → 5V → ESP32
```

#### Option 2: Addressable RGB (Fancy)

| Item | Search Term | Price | Notes |
|------|-------------|-------|-------|
| WS2812B strip 30LED/m | "ws2812b 30 led meter ip65" | $3-5 | Individually addressable |
| 5V 2A adapter | "5v 2a usb adapter" | $2-3 | Powers ESP32 + LEDs |

**Wiring:**
```
5V Adapter → WS2812B → Data pin from ESP32
          → ESP32 (VIN)
```

### Connectors & Cables

| Item | Search Term | Qty | Price |
|------|-------------|-----|-------|
| Dupont wire kit | "dupont wire kit male female" | 1 | $2 |
| DC barrel jack female | "dc 5.5mm female panel mount" | 2 | $0.50 |
| JST connectors 2pin | "jst xh 2pin connector" | 5 | $0.50 |
| Heat shrink tubing | "heat shrink tubing kit" | 1 | $1 |
| Prototype PCB | "pcb prototype board 5x7cm" | 5 | $1 |

### 3D Printing Materials (You Have Printer)

You'll design/print:
- Sensor enclosure (waterproof for bathroom)
- ESP32 enclosure
- LED strip channel/diffuser holder

**Download or design:**
- Thingiverse: "ESP32 case"
- Thingiverse: "LED strip diffuser channel"

**Filament needed:**
- PLA or PETG: ~50g total
- Consider PETG for bathroom (humidity resistant)

## Complete Shopping Cart

### Essential Order (~$15 USD)

```
1x ESP32-C3 Mini                    $2.50
1x AJ-SR04M (if you need spare)     $2.50
1x 12V LED strip 1m warm white      $1.50
1x IRF520 MOSFET module             $0.50
1x LM2596 buck converter            $0.80
1x 12V 2A DC adapter                $3.50
1x DC barrel jack female (2pcs)     $0.50
1x Dupont wires 20cm (40pcs)        $1.00
1x JST XH connectors kit            $1.00
1x Heat shrink kit                  $1.00
───────────────────────────────────────────
TOTAL:                              ~$15 USD
```

### Recommended Stores on AliExpress

1. **WAVGAT Official Store** - Good for ESP32, sensors
2. **GREAT WALL Electronics** - LEDs, connectors
3. **TENSTAR ROBOT Store** - Modules, good prices
4. **DIYmall Store** - Quality components

### Search Tips

- Sort by "Orders" to find reliable sellers
- Check reviews with photos
- Look for "Ships from: China" (cheapest)
- Shipping: 15-40 days to Colombia

## Wiring Diagram for Final Setup

```
                    ┌─────────────────┐
                    │   12V Adapter   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              │              ▼
    ┌─────────────────┐      │    ┌─────────────────┐
    │   LED Strip     │      │    │  Buck Converter │
    │    (12V)        │      │    │   12V → 5V      │
    └────────┬────────┘      │    └────────┬────────┘
             │               │             │
             │    ┌──────────┴──────┐      │
             │    │     MOSFET      │      │
             │    │     IRF520      │      │
             │    └──────────┬──────┘      │
             │               │             │
             └───────────────┤             │
                             │             ▼
                    ┌────────┴─────────────────┐
                    │         ESP32            │
                    │  GPIO13 → Sensor TRIG    │
                    │  GPIO12 ← Sensor ECHO    │
                    │  GPIO2  → MOSFET Gate    │
                    └──────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   AJ-SR04M      │
                    │    Sensor       │
                    └─────────────────┘
```

## 3D Print Files to Create

### 1. Sensor Mount
```
- Hole for sensor transducer (25mm diameter)
- Mounting holes for screws
- Cable routing channel
- Material: PETG (humidity resistant)
```

### 2. ESP32 + MOSFET Enclosure
```
- Fits ESP32 DevKit or C3 Mini
- Space for MOSFET module
- Ventilation holes
- DC jack mount
- Material: PLA or PETG
```

### 3. LED Channel
```
- Profile to hold LED strip
- Diffuser slot (use white PETG or buy diffuser)
- Mounting clips
- Material: White PLA/PETG
```

## Next Steps

1. Order components (2-4 weeks shipping)
2. While waiting:
   - Design 3D printed enclosures
   - Test current setup
   - Learn about MOSFET control
3. When parts arrive:
   - Assemble and test
   - Install in bathroom
