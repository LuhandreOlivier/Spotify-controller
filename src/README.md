# Raspberry Pi Pico W Spotify Controller

**Custom hardware controller for Spotify playback using Raspberry Pi Pico W and a 16×2 LCD.**

---

## Overview

This project implements a physical Spotify controller using a Raspberry Pi Pico W, five buttons, and a 16×2 LCD. The controller allows the user to skip tracks, adjust volume, and play/pause Spotify playback directly from dedicated hardware controls.

The LCD displays the currently playing song and artist. Long titles automatically scroll across the display while the system continues handling button interrupts responsively in real time.

The project interfaces directly with the Spotify Web API and combines interrupt-driven embedded programming with Wi-Fi networking and hardware debouncing.

---

## Technical Stack

### Hardware

- Raspberry Pi Pico W
- 16×2 I2C LCD display
- 5 push buttons
- Pull-up resistors
- Hardware debouncing circuitry
- Custom 3D printed enclosure

### Software

- MicroPython firmware
- Spotify Web API integration
- Interrupt-driven button handling
- LCD scrolling system
- Wi-Fi reconnect handling

---

## Features

- Playback control using dedicated hardware buttons
- Real-time track and artist display
- Automatic scrolling for long titles
- Interrupt-driven responsiveness
- Hardware debouncing for reliable input
- Spotify playback control over Wi-Fi
- LCD recovery handling after communication failures

---

## Engineering Challenges

### Hardware Debouncing

Software debouncing introduced noticeable latency due to polling delays. Hardware debouncing was implemented to provide immediate and reliable button recognition.

### LCD Scrolling

Long track names needed to scroll independently without blocking playback controls. The solution used timed scrolling routines while button actions remained interrupt-driven.

### Spotify API Freezing

Spotify DJ mode occasionally prevents playback information from updating. Playback control remains functional because interrupts operate independently from the API update logic.

---

## Learnings

- Interrupt-driven embedded systems improve responsiveness significantly
- Hardware debouncing can outperform software-only approaches
- Network APIs require robust recovery handling on embedded hardware
- Separating display logic from control logic improves system stability

---

## Current Status

- Fully functional playback controller
- Stable hardware debouncing implementation
- Real-time responsive controls
- LCD scrolling operational
- 3D enclosure prototype completed
- API freeze issue identified but not yet resolved

---

## Future Improvements

- Better API freeze recovery
- Album artwork support
- Larger display support
- Additional Spotify metadata
- Improved enclosure redesign

---

## Project Structure

```text
spotify-controller/
├── src/
│   ├── main.py
│   ├── lcd_api.py
│   ├── pico_i2c_lcd.py
│   └── secrets.py.example
├── docs/
│   ├── hardware.md
│   ├── setup.md
│   ├── api.md
│   └── architecture.md
├── assets/
│   ├── diagrams/
│   ├── demo/
│   └── images/
├── README.md
└── .gitignore
```

---

## License

MIT License
