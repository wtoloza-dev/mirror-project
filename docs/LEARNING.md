# Mirror Project - Learning Guide

Complete guide to understand embedded development with ESP32.

## Table of Contents

1. [Why MicroPython vs C](#why-micropython-vs-c)
2. [ESP32 Architecture](#esp32-architecture)
3. [How Ultrasonic Sensors Work](#how-ultrasonic-sensors-work)
4. [Code Deep Dive](#code-deep-dive)
5. [MicroPython Internals](#micropython-internals)
6. [Development Workflow](#development-workflow)

---

## Why MicroPython vs C

### The Two Main Options

| Aspect | MicroPython | C/C++ (Arduino/ESP-IDF) |
|--------|-------------|-------------------------|
| **Learning curve** | Easy (Python syntax) | Steeper (pointers, memory) |
| **Development speed** | Fast (no compile) | Slower (compile cycle) |
| **Performance** | ~10-100x slower | Native speed |
| **Memory usage** | ~256KB+ overhead | Minimal |
| **Flash size** | ~1.5MB firmware | ~200KB typical |
| **Debugging** | REPL interactive | Serial prints, JTAG |
| **Libraries** | Limited | Extensive |

### When to Use Each

**Use MicroPython when:**
- Prototyping and learning
- Simple I/O projects (sensors, LEDs)
- You need fast iteration
- Performance isn't critical
- Project fits in memory

**Use C/C++ when:**
- Timing-critical applications (audio, video)
- Battery-powered devices (need low power)
- Complex protocols (USB host, CAN bus)
- Memory-constrained devices
- Production/commercial products

### Performance Reality Check

For this mirror project:
- Sensor reading: ~30ms (physics limited, not code)
- LED toggle: ~1μs in C, ~100μs in MicroPython
- **Does it matter?** No. Human perception is ~100ms

MicroPython is "slow" but still microseconds. For human-interaction projects, it's plenty fast.

### Memory Comparison

```
ESP32 has:
- 520KB RAM
- 4MB Flash

MicroPython uses:
- ~256KB RAM for interpreter
- ~1.5MB Flash for firmware
- Leaves: ~264KB RAM, ~2.5MB Flash for your code

For this project we use:
- ~5KB RAM
- ~10KB Flash
- Conclusion: No problem
```

---

## ESP32 Architecture

### What is ESP32?

ESP32 is a **microcontroller** - a tiny computer on a single chip.

```
┌─────────────────────────────────────────┐
│              ESP32-WROOM                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  CPU 0  │  │  CPU 1  │  │  WiFi/  │  │
│  │ 240MHz  │  │ 240MHz  │  │   BT    │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │   RAM   │  │  Flash  │  │  GPIO   │  │
│  │  520KB  │  │   4MB   │  │ 34 pins │  │
│  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

### Key Components

**1. CPU (Xtensa LX6)**
- Dual-core at 240MHz
- MicroPython only uses 1 core
- Compare: Arduino Uno = 16MHz single core

**2. RAM (520KB SRAM)**
- Where your variables live
- Lost when power off
- MicroPython interpreter lives here

**3. Flash (4MB)**
- Persistent storage
- Where your .py files are saved
- Survives power off

**4. GPIO (General Purpose Input/Output)**
- 34 programmable pins
- Can be input (read sensors) or output (control LEDs)
- Some have special functions (ADC, PWM, I2C, SPI)

### GPIO Pins We Use

```
GPIO2  - Built-in LED (OUTPUT)
GPIO12 - Echo from sensor (INPUT)
GPIO13 - Trigger to sensor (OUTPUT)
```

### Pin Modes

```python
Pin(2, Pin.OUT)   # Configure as output (we control it)
Pin(12, Pin.IN)   # Configure as input (we read it)
```

---

## How Ultrasonic Sensors Work

### Physics

Sound travels at ~343 m/s (at 20°C).

```
Sensor          Object
  │               │
  │──── PING ────>│
  │               │
  │<─── ECHO ─────│
  │               │
  
Time = distance × 2 / speed
Distance = time × speed / 2
Distance = time × 343 / 2
Distance(cm) = time(μs) × 0.0343 / 2
Distance(cm) = time(μs) / 29.1 / 2
```

### AJ-SR04M Operation

```
1. Trigger pulse (10μs HIGH)
   ___
__|   |________________________________

2. Sensor sends 8 ultrasonic pulses (40kHz)
   (you don't see this)

3. Echo pin goes HIGH until sound returns
   ___________________________
__|                           |________
   <---- time proportional --->
         to distance
```

### The Code That Does This

```python
# 1. Send trigger pulse
trigger.off()
sleep_us(2)      # Ensure clean start
trigger.on()
sleep_us(10)     # 10 microsecond pulse
trigger.off()

# 2. Measure echo duration
duration = time_pulse_us(echo, 1, 30000)
#                             │    │
#                             │    └── timeout (30ms = ~5m max)
#                             └── wait for HIGH pulse

# 3. Calculate distance
distance_cm = (duration / 2) / 29.1
#              │           │
#              │           └── speed of sound factor
#              └── divide by 2 (sound goes and returns)
```

### Why 29.1?

```
Speed of sound = 343 m/s = 34300 cm/s = 0.0343 cm/μs

time(μs) × 0.0343 = distance(cm) × 2

distance = time × 0.0343 / 2
distance = time / 29.1

(29.1 ≈ 1 / 0.0343)
```

---

## Code Deep Dive

### Line by Line: main.py

```python
"""
Mirror light controller with proximity sensor.
...
"""
```
**Docstring**: Describes the module. Required by PEP 257.

---

```python
from machine import Pin, time_pulse_us
from time import sleep, sleep_us, ticks_ms, ticks_diff
```

**Imports from MicroPython:**
- `Pin`: Control GPIO pins
- `time_pulse_us`: Measure pulse duration in microseconds
- `sleep`: Pause in seconds
- `sleep_us`: Pause in microseconds
- `ticks_ms`: Get current time in milliseconds
- `ticks_diff`: Calculate time difference (handles overflow)

---

```python
TRIGGER_PIN = 13
ECHO_PIN = 12
LED_PIN = 2
```

**Constants**: ALL_CAPS by convention. Easy to change hardware config.

---

```python
MAX_DISTANCE_CM = 30
ACTIVATION_SECONDS = 1.5
TIMEOUT_SECONDS = 5
```

**Configuration**: Tune behavior without changing logic.

---

```python
def measure_distance() -> float:
```

**Type hint**: `-> float` says this function returns a decimal number.

---

```python
    trigger = Pin(TRIGGER_PIN, Pin.OUT)
    echo = Pin(ECHO_PIN, Pin.IN)
```

**Pin initialization**: Done inside function for clarity. In C you'd do this once globally for efficiency, but in MicroPython the overhead is negligible.

---

```python
    duration = time_pulse_us(echo, 1, 30000)
```

**Key function**: 
- Waits for pin to go HIGH (1)
- Measures how long it stays HIGH
- Returns after 30000μs (30ms) if no pulse
- Returns -1 or -2 on error

---

```python
def is_presence_detected(distance: float) -> bool:
```

**Single responsibility**: This function only decides yes/no. The measurement is separate. This makes testing easier.

---

```python
def run() -> None:
```

**Main loop function**: `-> None` means no return value.

---

```python
    presence_start_time = 0
    last_presence_time = 0
    light_on = False
    presence_active = False
```

**State variables**: Track what's happening across loop iterations.

---

```python
    activation_ms = int(ACTIVATION_SECONDS * 1000)
```

**Unit conversion**: Config in seconds (human-friendly), code uses milliseconds (computer-friendly).

---

```python
    while True:
```

**Infinite loop**: Embedded systems run forever until power off.

---

```python
        if presence:
            last_presence_time = current_time
            
            if not presence_active:
                presence_start_time = current_time
                presence_active = True
```

**State machine logic**:
- `presence_active`: Are we currently detecting someone?
- `presence_start_time`: When did we first see them?
- `last_presence_time`: When did we last see them?

---

```python
            presence_duration = ticks_diff(current_time, presence_start_time)
```

**Why ticks_diff?**: `ticks_ms()` overflows after ~12 days. Simple subtraction would give wrong results. `ticks_diff` handles this.

---

```python
        sleep(0.15)
```

**Loop delay**: 150ms between readings. Why?
- Sensor needs ~30ms to complete measurement
- Faster polling wastes CPU
- 150ms = ~6 readings/second (plenty for human movement)

---

## MicroPython Internals

### Boot Sequence

```
1. Power on
2. ROM bootloader runs
3. MicroPython firmware loads
4. boot.py executes (if exists)
5. main.py executes (if exists)
6. REPL starts (if main.py ends or Ctrl+C)
```

### File System

ESP32 flash is formatted as FAT filesystem:

```
/
├── boot.py      # Runs first
├── main.py      # Runs second
└── lib/         # Additional modules
```

### Memory Management

```python
import gc
gc.collect()     # Force garbage collection
gc.mem_free()    # Check free memory
```

MicroPython has automatic garbage collection but on microcontrollers you sometimes need to trigger it manually.

### REPL (Read-Eval-Print-Loop)

Interactive Python prompt over serial:

```
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.on()    # LED turns on!
>>> led.off()
```

This is why MicroPython is great for learning - instant feedback.

---

## Development Workflow

### Your Tools

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    uv       │────>│  mpremote   │────>│   ESP32     │
│ (packages)  │     │  (upload)   │     │ (hardware)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Typical Workflow

```bash
# 1. Edit code locally
vim src/main.py

# 2. Upload to ESP32
uv run mpremote connect /dev/ttyUSB0 cp src/main.py :main.py

# 3. Test
uv run mpremote connect /dev/ttyUSB0 run src/main.py

# 4. If good, reset to run from boot
uv run mpremote connect /dev/ttyUSB0 reset

# 5. Commit changes
git add -A && git commit -m "description" && git push
```

### Debugging Strategies

**1. Print debugging**
```python
print(f"distance={distance}, light_on={light_on}")
```

**2. REPL testing**
```bash
uv run mpremote connect /dev/ttyUSB0 repl
>>> # test code interactively
```

**3. Isolate problems**
```python
# Comment out sections to find the bug
# if presence:
#     ...
```

---

## Exercises

### Level 1: Modify Config
1. Change `MAX_DISTANCE_CM` to 50
2. Change `TIMEOUT_SECONDS` to 10
3. Upload and test

### Level 2: Add Feature
1. Make LED blink while waiting for activation
2. Hint: Add a counter in the presence detection loop

### Level 3: Rewrite in C
1. Install PlatformIO extension in Cursor
2. Create equivalent code in `src/main.cpp`
3. Compare binary size and behavior

### Level 4: Add WiFi
1. Connect ESP32 to your WiFi
2. Create a simple web page showing current distance
3. Hint: Look up `import network` and `import socket`

---

## Resources

- [MicroPython Docs](https://docs.micropython.org/)
- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- [ESP32 GPIO Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
