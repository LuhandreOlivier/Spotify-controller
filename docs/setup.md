# Setup Guide

## Flash MicroPython

Download and install MicroPython for the Pico W:

https://micropython.org/download/rp2-pico-w/

## Upload Files

Copy all files from the `src/` folder onto the Pico W.

## Configure Secrets

Rename:

`secrets.py.example`

to:

`secrets.py`

Then fill in:
- Wi-Fi credentials
- Spotify Client ID
- Spotify Client Secret
- Access token
- Refresh token

## Run

After rebooting, the LCD initializes and connects to Wi-Fi automatically.
