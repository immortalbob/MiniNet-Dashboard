# MiniNet Dashboard

A lightweight terminal dashboard for displaying Uptime Kuma monitor status on small displays, kiosks, Raspberry Pis, and dedicated monitoring screens.

Designed for always-on monitoring, MiniNet connects directly to your Uptime Kuma instance and presents a clean, color-coded overview of monitor health in a terminal window.

## Features

- Real-time monitor status
- Configurable refresh intervals
- Automatic night mode screen blanking
- Multi-column layouts
- Custom colors and symbols
- Dynamic terminal sizing
- Small-screen friendly operation

Originally built for a Raspberry Pi 4B with a SunFounder 3.5" IPS display running a dedicated status screen, but it automatically adapts to virtually any terminal size.

---

## Installation

### Requirements

- Python 3.8+
- Uptime Kuma instance
- Terminal capable of ANSI colors

```bash
pip install uptime-kuma-api
```

```bash
git clone https://github.com/yourname/mininet-dashboard.git
cd mininet-dashboard
```

```bash
cp .kuma-dashboard.json ~/.kuma-dashboard.json
```

Edit your configuration:

```bash
nano ~/.kuma-dashboard.json
```

Run:

```bash
python3 kuma-dashboard.py
```

---

## Example Configuration

```json
{
  "kuma_url": "http://localhost:3001",
  "username": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "refresh_interval": 30,
  "night_start": 20,
  "night_end": 4,
  "dashboard_title": "MiniNet",
  "title_color": "red",
  "use_12hr_time": true,
  "show_date": true,
  "columns": 2,
  "bar_length": 50,
  "show_percentage": true,
  "show_up_count": true,
  "show_down_count": true,
  "status_up_symbol": "+",
  "status_down_symbol": "-",
  "status_pending_symbol": "?",
  "status_maintenance_symbol": "!",
  "border_style": "double",
  "compact_mode": false
}
```

---

## Configuration Options

### Connection

| Option | Description |
|----------|-------------|
| kuma_url | URL of the Uptime Kuma server |
| username | Login username |
| password | Login password |
| refresh_interval | Refresh interval in seconds |

### Night Mode

| Option | Description |
|----------|-------------|
| night_start | Hour to blank the display (24h format) |
| night_end | Hour to resume display |

### Display

| Option | Description |
|----------|-------------|
| dashboard_title | Dashboard title |
| title_color | red, green, yellow, cyan, blue, magenta, white, bold |
| use_12hr_time | Use 12-hour clock |
| show_date | Display current date |
| columns | 1–3 monitor columns |
| compact_mode | Reduce vertical spacing |

### Status Bar

| Option | Description |
|----------|-------------|
| bar_length | Width of uptime bar |
| show_percentage | Show uptime percentage |
| show_up_count | Show online count |
| show_down_count | Show offline count |

### Status Symbols

| Option | Description |
|----------|-------------|
| status_up_symbol | Online symbol |
| status_down_symbol | Offline symbol |
| status_pending_symbol | Pending symbol |
| status_maintenance_symbol | Maintenance symbol |

### Borders

Supported values:

- single
- double
- thin

---

## Environment Variables

Environment variables override configuration values:

```bash
export KUMA_URL=http://localhost:3001
export KUMA_USERNAME=admin
export KUMA_PASSWORD=secret
```

---

## Raspberry Pi Use Case

Tested configuration:

- Raspberry Pi 4B
- SunFounder 3.5" IPS Display
- Raspberry Pi OS Lite
- Uptime Kuma

The dashboard dynamically scales to terminal dimensions and should work on:

- Small SPI displays
- HDMI monitors
- Tablets running terminal kiosks
- Desktop monitors
- SSH sessions

---

## License

MIT License
