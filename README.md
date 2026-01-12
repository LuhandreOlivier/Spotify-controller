# Raspberry Pi Pico W Spotify Controller

**Custom hardware controller for Spotify playback using Raspberry Pi Pico W and a 16×2 LCD.**

---

## Overview

This project implements a **physical Spotify controller** using a Raspberry Pi Pico W, five buttons, and a 16×2 LCD. The controller allows you to **skip tracks, adjust volume, and play/pause** your Spotify playback directly from the hardware. The LCD displays the current track name and automatically scrolls for titles longer than 16 characters.

The project interfaces with the **Spotify Web API** and handles button debouncing and display scrolling with a combination of **hardware debouncing and timed updates**.

---

## Technical Stack

### Hardware

- Raspberry Pi Pico W  
- 16×2 I2C LCD display  
- 5 push buttons (Skip Forward, Skip Back, Volume Up, Volume Down, Play/Pause)  
- Pull-up resistors for buttons and hardware debouncing  
- Miscellaneous wiring and connectors  

**Justification:**  
The Pico W provides Wi-Fi connectivity for Spotify API integration and supports low-latency button interrupts. Hardware debouncing ensures reliable button input given the long debounce times required by the software.

### Software

- MicroPython firmware for the Pico W  
- Spotify Web API integration for playback control  
- LCD scrolling logic for track titles longer than 16 characters  
- Button interrupt handling with hardware debouncing  

---

## My Role

- Designed the full hardware layout and button wiring  
- Implemented hardware debouncing circuits for reliable input  
- Programmed the Pico W to interface with Spotify API and LCD  
- Developed scrolling logic for track titles on a 16×2 display  
- Integrated all components into a functioning prototype
- Designed and 3D printed an enclosure

---

## Key Features

- **Playback Control:** Skip forward/back, play/pause, and adjust volume with dedicated buttons  
- **Track Display:** Shows current song title and artist; scrolls long track names across the 16×2 LCD  
- **Reliable Input:** Hardware debouncing ensures consistent button recognition  
- **Spotify API Integration:** Directly controls Spotify playback on a connected device  
- **Interrupt-Driven Controls:** Buttons trigger immediate actions without waiting for the main loop  

---

## Challenges & Learnings

**Challenge:** Software debouncing required impractically long delays due to slow button polling, causing sluggish response.  
**Solution:** Implemented hardware debouncing to achieve instant, reliable button recognition.  

**Challenge:** LCD scrolling for track names longer than 16 characters while maintaining responsive button control.  
**Solution:** Created a timed scrolling routine that runs independently from button interrupts.  

**Challenge:** Spotify “DJ mode” occasionally freezes API updates, preventing the display from refreshing.  
**Solution:** Interrupts still function for buttons, so playback control remains operational even when the display fails.  

**Learnings:**  
- Hardware debouncing is often more reliable for low-latency embedded input  
- Interrupt-driven systems allow responsive controls even under partial software failures  
- Integrating a network API with real-time embedded hardware requires careful timing and error handling  

---

## Current Status

- Fully functional playback controller with responsive buttons  
- 16×2 LCD scrolls song titles and shows currently playing track (updates work except during DJ-induced API freezes)  
- Hardware debouncing fully implemented and reliable  
- Buttons and firmware tested for real-time responsiveness
- DJ freezing problem has not been adressed, but due to button functionality this is not a priority at the moment
- 3D printed enclosure has a hole for the micro usb port that does not properly line up. The 3D print was manipulated to make it work for the moment, but a redesign is required

---

## Future Enhancements

- Implement robust error handling for Spotify API freezes to maintain display updates  
- Expand to show additional metadata (album, progress, or artwork)  
- Add multi-device control or custom playlists integration  
- Upgrade to larger or color LCD for improved readability and user experience  

---

## Acknowledgements

- Spotify Web API documentation and community examples  
- CircuitPython / MicroPython communities for embedded device tutorials  
- Hardware debouncing references from electronics and embedded systems guides  

---

[GitHub Repository]((https://github.com/LuhandreOlivier/Spotify-controller))
