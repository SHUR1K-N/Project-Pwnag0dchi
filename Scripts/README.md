# Scripts for PiSugar 3 + Waveshare V4

Helper scripts for pwnagotchi running on Pi Zero 2W with a PiSugar 3 battery hat and Waveshare 2.13" V4 e-ink display.

## Prerequisites

- Pwnagotchi installed at `/home/pi/.pwn/`
- PiSugar 3 with `pisugar-server` daemon running
- Waveshare 2.13" V4 display (250x122 pixels)

## What's included

| File | Purpose |
|------|---------|
| `epd-shutdown.py` | Draws a sleeping face on the e-ink before power off (persists after power cut) |
| `epd-startup.py` | Draws a waking face on the e-ink at boot (before pwnagotchi loads) |
| `safe-shutdown.sh` | Graceful shutdown: stops pwnagotchi, draws face, powers off. Includes boot-loop guard for low-battery charging |
| `pisugar-watchdog.sh` | Detects when PiSugar 3 MCU wakes from deep sleep and restarts pisugar-server |
| `systemd/epd-startup.service` | Runs `epd-startup.py` early in boot |
| `systemd/pisugar-watchdog.service` | Oneshot service for the watchdog script |
| `systemd/pisugar-watchdog.timer` | Runs the watchdog every 15 seconds |

## Install

```bash
# Copy scripts
sudo cp epd-shutdown.py epd-startup.py /usr/local/bin/
sudo cp safe-shutdown.sh pisugar-watchdog.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/epd-*.py /usr/local/bin/safe-shutdown.sh /usr/local/bin/pisugar-watchdog.sh

# Copy systemd units
sudo cp systemd/*.service systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable epd-startup.service
sudo systemctl enable --now pisugar-watchdog.timer
```

## PiSugar 3 configuration

Set `safe-shutdown.sh` as the power button handler in `/etc/pisugar-server/config.json`:

```json
{
  "soft_poweroff_shell": "sudo /usr/local/bin/safe-shutdown.sh"
}
```

Then restart: `sudo systemctl restart pisugar-server`

## Boot-loop guard

When `auto_power_on` is enabled in PiSugar config and the battery dies, plugging in USB-C triggers: charge -> auto power on -> low battery shutdown -> repeat.

`safe-shutdown.sh` prevents this by checking: if battery < 10% AND charging, skip shutdown and let the Pi charge.

## Hardware guards

- **EPD scripts:** Import the V4-specific driver (`v2in13_V4`). On non-V4 displays, the import fails and the script exits silently — no harm to other setups.
- **PiSugar scripts:** Query `pisugar-server` on port 8423. If pisugar-server isn't running (non-PiSugar setup), commands return empty and the scripts proceed normally or exit.

## button_feedback plugin

The scripts write status messages to `/tmp/.pwnagotchi-button-msg`. Enable the `button_feedback` plugin (in `../Plugins/`) to show these messages on the pwnagotchi display:

```toml
main.plugins.button_feedback.enabled = true
main.plugins.button_feedback.display_seconds = 5
```
