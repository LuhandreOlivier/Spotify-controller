# Hardware Documentation

## Raspberry Pi Pico W

The Pico W was selected because it provides:
- Built-in Wi-Fi
- GPIO interrupt support
- Low-latency button handling
- Sufficient RAM for API communication and LCD updates

## LCD Interface

The 16×2 LCD communicates over I2C using a PCF8574 I/O expander.

### Wiring

| LCD Pin | Pico W |
|---|---|
| SDA | GP0 |
| SCL | GP1 |

I2C Address: `0x27`

## Button Layout

| Function | GPIO |
|---|---|
| Next Track | GP2 |
| Play/Pause | GP4 |
| Volume Up | GP5 |
| Volume Down | GP6 |
| Previous Track | GP15 |

## Debouncing

Hardware debouncing was implemented because software debouncing introduced unacceptable input latency during API communication and LCD updates.
