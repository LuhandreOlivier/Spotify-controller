# Software Architecture

## Interrupt-Driven Design

All buttons use GPIO interrupts rather than polling.

Advantages:
- Immediate responsiveness
- Lower CPU overhead
- Reliable playback control during display updates

## LCD Scrolling

Track names longer than 16 characters scroll independently while interrupts remain active.

## Wi-Fi Recovery

The firmware continuously checks Wi-Fi status and reconnects automatically if connectivity is lost.

## Memory Management

Garbage collection is manually triggered periodically to avoid memory fragmentation during repeated API requests.
