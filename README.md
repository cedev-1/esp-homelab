# ESP Homelab Dashboard

A MicroPython-based dashboard for displaying homelab information on a 2.8" TFT screen (240x320 pixels). Currently integrates with AdGuard Home to show DNS query statistics and ad blocking metrics.

## Features

- Real-time display of AdGuard Home statistics
- DNS queries count
- Blocked ads count
- Percentage of blocked queries with visual progress bar
- UI with rounded cards and progress bars

## Hardware Requirements

- ESP-WROOM-32 microcontroller
- 2.8" TFT LCD display (ILI9341 controller, 240x320 resolution)
- Appropriate wiring connections (SPI interface)

## Software Requirements

- MicroPython firmware for ESP32
- Thonny IDE for development and flashing
- Required libraries:
  - `ili9341.py` from [rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341)

## Setup Instructions

1. **Flash MicroPython on ESP32:**
   - Use Thonny IDE to flash MicroPython firmware onto your ESP-WROOM-32

2. **Create Project Structure:**
   - Create `boot.py` (default file created by MicroPython)
   - Copy `main.py` content into `boot.py` (or keep as separate files if preferred)
   - Create `ui_pack.py` with the UI components
   - Download and copy `ili9341.py` from the repository linked above

3. **Configure Settings:**
   - Edit the variables in `main.py`:
     - `WIFI_SSID` and `WIFI_PASS` for WiFi connection
     - `ADGUARD_IP`, `ADGUARD_PORT`, `ADGUARD_USER`, `ADGUARD_PASS` for AdGuard Home API access
     - Set `DEBUG = True` for console output during development

4. **Hardware Connections:**
   - Connect the TFT display to ESP32 pins as specified in the code comments:
     - CS: D15
     - RESET: D4
     - DC: D2
     - SDI(MOSI): D23
     - SCK: D18
     - LED: 3V
     - SDO(MISO): D19
     - VCC: 3V
     - GND: GND

5. **Upload Files:**
   - Use Thonny to upload `main.py`, `ui_pack.py`, and `ili9341.py` to the ESP32

## Usage

Once powered on, the ESP32 will:
1. Connect to WiFi
2. Display the dashboard with static elements
3. Continuously fetch and update AdGuard Home statistics every 5 seconds
4. Show a red indicator in the bottom-right if API calls fail

## TODO

- [ ] Create reusable UI components library
- [ ] Add more homelab service integrations (e.g., Jellyfin, Pi-hole, Docker stats, system monitoring)
- [ ] Implement different dashboard layouts/modes
- [ ] Add touch input support for interactive features
- [ ] Create 3D printed enclosure model
- [ ] Add configuration menu for WiFi and API settings
- [ ] Add more visual indicators and alerts
- [ ] Battery/power management features