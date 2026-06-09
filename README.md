# MiniNet-Dashboard

A configurable terminal dashboard for [Uptime Kuma](https://github.com/louislam/uptime-kuma), displaying monitor statuses in a clean CLI layout with night mode, customizable symbols, multi-column support, and a live uptime bar.

Built for headless displays and low-power nodes like a Raspberry Pi with a small attached screen.

---

## Screenshot

![Example MiniNet Readout](images/example.png)

---

## Requirements

- Python 3.8+
- [`uptime-kuma-api`](https://github.com/lucasheld/uptime-kuma-api)

```bash
pip install uptime-kuma-api
```

---

## Setup

**1. Clone or copy the script:**

```bash
git clone https://github.com/immortalbob/MiniNet-Dashboard
cd MiniNet-Dashboard
```

**2. Edit your credentials and preferences (copy example below):**

```bash
nano ~/.kuma-dashboard.json
```

**3. Run:**

```bash
python3 kuma-dashboard.py
```

---

## Configuration

Config lives at `~/.kuma-dashboard.json`. All fields are optional — defaults are used for anything not specified.

| Key | Default | Description |
|-----|---------|-------------|
| `kuma_url` | `http://localhost:3001` | URL of your Uptime Kuma instance |
| `username` | *(required)* | Uptime Kuma username |
| `password` | *(required)* | Uptime Kuma password |
| `refresh_interval` | `30` | Seconds between data refreshes |
| `night_start` | `20` | Hour (24h) when screen blanks |
| `night_end` | `4` | Hour (24h) when screen wakes |
| `dashboard_title` | `MyNetwork` | Title shown in header |
| `title_color` | `red` | Title color: `red` `green` `yellow` `cyan` `blue` `magenta` `white` |
| `use_12hr_time` | `true` | 12-hour vs 24-hour clock |
| `show_date` | `true` | Show date in header |
| `columns` | `2` | Number of columns (1–2) |
| `bar_length` | `50` | Width of the uptime bar in characters |
| `show_percentage` | `true` | Show uptime % next to bar |
| `show_up_count` | `true` | Show UP count in header |
| `show_down_count` | `true` | Show DOWN count in header |
| `status_up_symbol` | `+` | Symbol for UP monitors |
| `status_down_symbol` | `-` | Symbol for DOWN monitors |
| `status_pending_symbol` | `?` | Symbol for PENDING monitors |
| `status_maintenance_symbol` | `!` | Symbol for MAINTENANCE monitors |
| `border_style` | `double` | Border style: `single` `double` `thin` |
| `compact_mode` | `false` | Skip blank lines between monitors and footer |

### Example Config

Copy this to `~/.kuma-dashboard.json` and fill in your credentials:

```json
{
  "kuma_url": "http://localhost:3001",
  "username": "your_username",
  "password": "your_password",
  "refresh_interval": 30,
  "night_start": 20,
  "night_end": 4,
  "dashboard_title": "MyNetwork",
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

### Environment Variable Overrides

Credentials can be set via environment variables, which take precedence over the config file:

```bash
export KUMA_URL=http://localhost:3001
export KUMA_USERNAME=admin
export KUMA_PASSWORD=yourpassword
```

---

## Terminal Sizing

The dashboard is fully responsive to your terminal size. Borders and separators stretch to fill the full width, the uptime bar respects `bar_length` up to the available width, and the footer is pushed to the bottom of the screen. Resizing the terminal or SSH window takes effect on the next refresh cycle.

For small screens (like a 3.5" Pi display running a framebuffer terminal), `compact_mode: true` removes the blank lines between the monitor list and footer, keeping everything visible without scrolling.

---

## Running as a systemd Service

To run the dashboard automatically on boot (e.g. on a headless Pi):

```ini
# /etc/systemd/system/kuma-dashboard.service
[Unit]
Description=Kuma Dashboard
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/youruser/kuma-dashboard/kuma-dashboard.py
Restart=on-failure
User=youruser
Environment=TERM=xterm-256color

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kuma-dashboard
```

---

## Night Mode

The dashboard blanks the screen automatically between `night_start` and `night_end` hours to avoid burn-in on always-on displays. Wraps midnight correctly — e.g. `night_start: 20`, `night_end: 4` blanks from 8 PM to 4 AM.

---

## Error Handling

If a data fetch fails (network blip, Kuma restart), the dashboard holds the last known state rather than crashing or going blank. Errors are silently swallowed and the stale data is redisplayed until the next successful poll.

---

## Contributing

Contributions are welcome. If you have a feature idea, bug fix, or improvement, feel free to open an issue or submit a pull request.

A few areas where help would be appreciated:

- **Combo/multi-monitor grouping** — grouping monitors by tag or parent
- **3-column layout** — the config accepts `columns: 3` but the layout logic caps at 2
- **Border style expansion** — `single`, `double`, and `thin` currently render identically; proper distinct styles would be a nice improvement
- **Color themes** — a full theme system beyond per-element color config

Please keep PRs focused and configs in `config.example.json` rather than hardcoded values. Sensitive data should never be committed.

---

## License

MIT
