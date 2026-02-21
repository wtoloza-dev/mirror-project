# Power Consumption Guide

Understanding electricity consumption for 24/7 operation.

## Current Hardware Consumption

### ESP32-WROOM

| Mode | Current | Power (3.3V) |
|------|---------|--------------|
| Active (WiFi TX) | 240 mA | 792 mW |
| Active (WiFi RX) | 100 mA | 330 mW |
| Active (no WiFi) | 40-50 mA | 130-165 mW |
| Modem sleep | 20-30 mA | 66-99 mW |
| Light sleep | 0.8 mA | 2.6 mW |
| Deep sleep | 10 μA | 0.033 mW |

**Your current setup**: ~50mA (WiFi not used, MicroPython running)

### AJ-SR04M Sensor

| Mode | Current |
|------|---------|
| Standby | 2 mA |
| Measuring | 8 mA |
| Average (measuring every 150ms) | ~5 mA |

### LED (ESP32 onboard)

| State | Current |
|-------|---------|
| OFF | 0 mA |
| ON | 5-10 mA |

### Total System Consumption

```
ESP32 (active, no WiFi):  50 mA
AJ-SR04M (average):        5 mA
LED (50% duty cycle):      3 mA
─────────────────────────────────
TOTAL:                   ~58 mA at 5V
```

## Cost Calculation (24/7 Operation)

### Daily Consumption

```
Power = 5V × 0.058A = 0.29W
Daily = 0.29W × 24h = 6.96 Wh = 0.007 kWh
```

### Monthly Cost

```
Monthly = 0.007 kWh × 30 days = 0.21 kWh

Colombia electricity rate: ~$800 COP/kWh (2024)
Monthly cost: 0.21 × $800 = $168 COP (~$0.04 USD)

US electricity rate: ~$0.15/kWh
Monthly cost: 0.21 × $0.15 = $0.03 USD
```

**Conclusion**: Costs almost nothing to run 24/7 (~$2000 COP/year).

## Comparison: What If You Used Different Hardware?

### Option 1: ESP8266 (Wemos D1 Mini)

| Spec | ESP32 | ESP8266 |
|------|-------|---------|
| Active current | 50 mA | 70 mA |
| Deep sleep | 10 μA | 20 μA |
| Price | $5-8 | $2-4 |
| CPU | 240MHz dual | 80MHz single |

**Result**: ESP8266 actually uses MORE power when active. ESP32 is more efficient.

### Option 2: ATtiny85 (No WiFi, No MicroPython)

| Spec | ESP32 | ATtiny85 |
|------|-------|----------|
| Active current | 50 mA | 5 mA |
| Sleep | 10 μA | 0.1 μA |
| Price | $5-8 | $1-2 |
| Programming | Easy (Python) | Harder (C) |
| Features | WiFi, BT, dual core | Just GPIO |

**Result**: 10x less power, but no WiFi/Python. Good if you never need remote features.

### Option 3: PIR Sensor Instead of Ultrasonic

| Spec | AJ-SR04M | PIR (HC-SR501) |
|------|----------|----------------|
| Current | 5 mA | 50 μA |
| Detection | Distance based | Motion based |
| Angle | 15° narrow | 120° wide |
| Range | 20-400 cm | 3-7 m |
| Response | Continuous | Triggered |

**Result**: PIR uses 100x less power but detects motion, not presence. If you stand still, PIR won't detect you (bad for mirror).

## Power Optimization Strategies

### Level 1: Software (Easy)

**Current code**: Measures every 150ms = 6.6 times/second

```python
sleep(0.15)  # 150ms between readings
```

**Optimization**: Measure every 500ms = 2 times/second

```python
sleep(0.5)  # 500ms between readings
```

**Savings**: ~15% less CPU usage, negligible power savings on ESP32.

### Level 2: Modem Sleep (Medium)

Disable WiFi radio completely (already done by default in our code):

```python
import network
wifi = network.WLAN(network.STA_IF)
wifi.active(False)
```

**Savings**: 240mA → 50mA (already applied)

### Level 3: Light Sleep Between Readings (Advanced)

```python
import machine

def run():
    while True:
        distance = measure_distance()
        # ... handle logic ...
        
        # Sleep ESP32 core for 150ms
        machine.lightsleep(150)  # Instead of time.sleep(0.15)
```

**Savings**: 50mA → 20mA average

**Tradeoff**: Slightly slower wake-up time (~3ms)

### Level 4: Deep Sleep with External Trigger (Complex)

Use PIR to wake ESP32 from deep sleep:

```
PIR ──────> ESP32 GPIO (wake trigger)

ESP32 in deep sleep: 10μA
PIR detects motion → ESP32 wakes → activates ultrasonic
No motion for 10s → ESP32 goes back to deep sleep
```

**Savings**: 50mA → 0.05mA (99.9% reduction)

**Tradeoff**: 
- Need extra PIR sensor
- 2-3 second wake-up delay
- More complex code

## Your USB Adapter Power

The USB adapter providing power also has losses:

```
Typical USB adapter efficiency: 70-85%

Wall power consumption:
= ESP32 consumption / efficiency
= 0.29W / 0.80
= 0.36W from wall

Monthly: 0.26 kWh (~$210 COP)
```

## Heat Generation

```
Power dissipated as heat:
ESP32: ~150mW = 0.15W

For reference:
- Phone charger: ~5W
- LED bulb: ~9W
- Your ESP32: ~0.15W (negligible heat)
```

ESP32 will be barely warm to touch. No cooling needed.

## Recommended Setup for Your Project

### For Development (Current)

```
USB cable from PC → ESP32
- Easy to program
- Powered while coding
- Cost: Free (PC already on)
```

### For Permanent Installation

```
5V USB adapter → ESP32
- Dedicated power
- Recommend: 5V 1A adapter ($3-5)
- Actual usage: ~60mA (1% of capacity)
```

### Overkill Warning

Don't use:
- ❌ 5V 3A adapter (wastes standby power)
- ❌ Smart plugs (add their own consumption)
- ❌ Solar panels (project uses only $2000/year)

## Power Budget for Future LED Strip

When you add LED strip:

```
12V LED strip (4W):
Current at 12V: 4W / 12V = 333 mA

If using WS2812B (5V):
30 LEDs × 20mA each = 600 mA
Power: 5V × 0.6A = 3W

Total system with LEDs:
ESP32:     0.29W
Sensor:    0.025W
LED strip: 3W
─────────────────
Total:     ~3.3W = ~24 kWh/year

Cost: ~$19,000 COP/year ($5 USD/year)
```

Still negligible cost.

## Summary

| Metric | Value |
|--------|-------|
| Current consumption | ~58 mA |
| Power consumption | ~0.29W |
| Monthly electricity | ~0.21 kWh |
| Monthly cost (Colombia) | ~$170 COP |
| Yearly cost (Colombia) | ~$2,000 COP |
| Heat generated | Negligible |
| Recommended adapter | 5V 1A USB |

**Bottom line**: Run it 24/7 without worry. It costs less than leaving a phone charger plugged in.
