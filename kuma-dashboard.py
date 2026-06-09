#!/usr/bin/env python3
"""
MiniNet - Configurable Dashboard
Fully customizable via JSON config file.
"""

import time
import os
import signal
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from uptime_kuma_api import UptimeKumaApi

# ============================================================================
# COLORS & STYLES
# ============================================================================

class Style:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    CLEAR = "\033[2J\033[H"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

# Color mapping for configurable title color
COLOR_MAP = {
    "red": Style.RED,
    "green": Style.GREEN,
    "yellow": Style.YELLOW,
    "cyan": Style.CYAN,
    "blue": Style.BLUE,
    "magenta": Style.MAGENTA,
    "white": Style.WHITE,
    "bold": Style.BOLD,
}

# Border styles
BORDER_STYLES = {
    "single": ("=", "-"),
    "double": ("=", "-"),
    "thin": ("-", "."),
}

@dataclass
class Config:
    # Connection settings
    kuma_url: str = "http://localhost:3001"
    username: str = "YOUR_USERNAME_HERE"
    password: str = "YOUR_PASSWORD_HERE"
    refresh_interval: int = 30
    
    # Night mode settings
    night_start: int = 20
    night_end: int = 4
    
    # Display settings
    dashboard_title: str = "MiniNet"
    title_color: str = "red"
    use_12hr_time: bool = True
    show_date: bool = True
    columns: int = 2
    bar_length: int = 50
    show_percentage: bool = True
    show_up_count: bool = True
    show_down_count: bool = True
    
    # Status symbols
    status_up_symbol: str = "+"
    status_down_symbol: str = "-"
    status_pending_symbol: str = "?"
    status_maintenance_symbol: str = "!"
    
    # Style settings
    border_style: str = "double"
    compact_mode: bool = False
    
    # File path
    config_file: str = "~/.kuma-dashboard.json"

# ============================================================================
# CONFIGURATION
# ============================================================================

def load_config():
    config = Config()
    config_path = Path(config.config_file).expanduser()
    
    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
        except Exception as e:
            print(f"{Style.RED}Config error: {e}{Style.RESET}")
    
    # Environment variables override (for sensitive data)
    config.kuma_url = os.getenv("KUMA_URL", config.kuma_url)
    config.username = os.getenv("KUMA_USERNAME", config.username)
    config.password = os.getenv("KUMA_PASSWORD", config.password)
    
    return config

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def get_status_from_heartbeats(heartbeats: Dict, monitor_id: int) -> int:
    """Extract status from heartbeats"""
    hb = heartbeats.get(monitor_id, [])
    if not isinstance(hb, list):
        hb = []
    last = None
    for item in hb:
        if isinstance(item, dict):
            last = item
    status = last.get("status", 3) if last else 3
    return status

def get_status_symbol(status: int, config: Config) -> str:
    """Get status symbol based on config"""
    if status == 1:
        return f"{Style.GREEN}{config.status_up_symbol}{Style.RESET}"
    elif status == 0:
        return f"{Style.RED}{config.status_down_symbol}{Style.RESET}"
    elif status == 2:
        return f"{Style.YELLOW}{config.status_pending_symbol}{Style.RESET}"
    elif status == 3:
        return f"{Style.CYAN}{config.status_maintenance_symbol}{Style.RESET}"
    else:
        return f"{Style.YELLOW}?{Style.RESET}"

def is_night_time(config: Config) -> bool:
    hour = datetime.now().hour
    start, end = config.night_start, config.night_end
    
    if start <= end:
        return start <= hour < end
    else:
        return hour >= start or hour < end

def blank_screen():
    print(Style.CLEAR, end="")

def format_time(config: Config) -> str:
    """Format time based on config (12hr or 24hr)"""
    now = datetime.now()
    if config.use_12hr_time:
        return now.strftime("%I:%M:%S %p").lstrip("0")
    else:
        return now.strftime("%H:%M:%S")

def get_terminal_size():
    """Get terminal height and width"""
    try:
        size = shutil.get_terminal_size()
        return size.lines, size.columns
    except:
        return 24, 80

def center_text(text: str, width: int) -> str:
    """Center text within given width"""
    # Remove ANSI color codes for accurate length calculation
    clean_text = text
    for code in [Style.BOLD, Style.RED, Style.GREEN, Style.CYAN, Style.DIM, Style.RESET,
                 Style.YELLOW, Style.BLUE, Style.MAGENTA, Style.WHITE]:
        clean_text = clean_text.replace(code, '')
    
    text_len = len(clean_text)
    padding = max(0, (width - text_len) // 2)
    return " " * padding + text

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def draw_dashboard(monitors: List[Dict], heartbeats: Dict, config: Config):
    term_lines, term_width = get_terminal_size()
    
    # Sort monitors alphabetically
    monitors = sorted(monitors, key=lambda x: x.get("name", ""))
    total = len(monitors)
    
    # Calculate stats
    up = 0
    down = 0
    other = 0
    
    for mon in monitors:
        mid = mon.get("id")
        status = get_status_from_heartbeats(heartbeats, mid)
        if status == 1:
            up += 1
        elif status == 0:
            down += 1
        else:
            other += 1
    
    # Calculate uptime percentage
    if total > 0:
        percentage = int((up / total) * 100)
    else:
        percentage = 0
    
    # Get title color
    title_color = COLOR_MAP.get(config.title_color, Style.RED)
    
    # Prepare header content
    time_str = format_time(config)
    date_str = datetime.now().strftime("%a %b %d") if config.show_date else ""
    
    # Build header parts
    header_parts = [f"{Style.BOLD}{title_color}{config.dashboard_title}{Style.RESET}", time_str]
    if config.show_date and date_str:
        header_parts.append(date_str)
    
    # Add UP count if enabled
    if config.show_up_count:
        header_parts.append(f"{Style.GREEN}{config.status_up_symbol}{up}{Style.RESET}")
    
    # Add DOWN count if enabled
    if config.show_down_count:
        header_parts.append(f"{Style.RED}{config.status_down_symbol}{down}{Style.RESET}")
    
    header_text = " | ".join(header_parts)
    
    # Generate monitor lines
    monitor_lines = []
    
    # Two-column layout (or single column if configured)
    num_cols = min(config.columns, 3)  # Max 3 columns
    if num_cols >= 2:
        half = (total + 1) // 2
        left_col = monitors[:half]
        right_col = monitors[half:]
        
        # Find max name length for alignment
        max_left = max((len(m.get("name", "")) for m in left_col), default=0)
        max_right = max((len(m.get("name", "")) for m in right_col), default=0)
        col_width = max(max_left, max_right)
        
        for i in range(max(len(left_col), len(right_col))):
            line = ""
            
            # Left column
            if i < len(left_col):
                m = left_col[i]
                mid = m.get("id")
                name = m.get("name", "")
                status = get_status_from_heartbeats(heartbeats, mid)
                line += f"{get_status_symbol(status, config)} {name:<{col_width}}"
            else:
                line += " " * (col_width + 2)
            
            # Separator
            line += "    "
            
            # Right column
            if i < len(right_col):
                m = right_col[i]
                mid = m.get("id")
                name = m.get("name", "")
                status = get_status_from_heartbeats(heartbeats, mid)
                line += f"{get_status_symbol(status, config)} {name}"
            
            monitor_lines.append(line)
    else:
        # Single column
        for m in monitors:
            name = m.get("name", "")
            status = get_status_from_heartbeats(heartbeats, m.get("id"))
            line = f"{get_status_symbol(status, config)} {name}"
            monitor_lines.append(line)
    
    # Prepare footer content
    bar_len = min(config.bar_length, term_width - 20)
    up_len = int(bar_len * up / total) if total > 0 else 0
    down_len = int(bar_len * down / total) if total > 0 else 0
    
    bar = f"{Style.GREEN}{'█' * up_len}{Style.RESET}"
    bar += f"{Style.RED}{'█' * down_len}{Style.RESET}"
    bar += f"{Style.DIM}{'░' * (bar_len - up_len - down_len)}{Style.RESET}"
    
    footer_text = bar
    if config.show_percentage:
        # Choose color for percentage
        if percentage == 100:
            pct_color = Style.GREEN
        elif percentage >= 75:
            pct_color = Style.CYAN
        elif percentage >= 50:
            pct_color = Style.YELLOW
        else:
            pct_color = Style.RED
        footer_text += f"  {pct_color}{percentage}%{Style.RESET}"
    
    # Create dynamic borders that respect terminal width
    border_char, separator_char = BORDER_STYLES.get(config.border_style, ("=", "-"))
    top_border = Style.BOLD + Style.CYAN + border_char * (term_width - 1) + Style.RESET
    separator = Style.BOLD + Style.CYAN + separator_char * (term_width - 1) + Style.RESET
    
    # Calculate content height
    content_height = 3 + len(monitor_lines) + 1  # top border + header + separator + monitors + footer
    lines_to_bottom = term_lines - content_height
    
    # Clear screen
    print(Style.CLEAR, end="")
    
    # TOP BORDER (full width, left-aligned)
    print(top_border)
    
    # Header (centered)
    print(center_text(header_text, term_width))
    
    # Separator (full width, left-aligned)
    print(separator)
    
    # Monitor list (left-aligned)
    for line in monitor_lines:
        print(line)
    
    # Add blank lines to push footer to bottom (only if not compact mode)
    if not config.compact_mode:
        for _ in range(max(0, lines_to_bottom - 1)):
            print()
    
    # Footer (centered)
    print(center_text(footer_text, term_width))

# ============================================================================
# API & MAIN LOOP
# ============================================================================

def fetch_data(config: Config):
    with UptimeKumaApi(config.kuma_url, timeout=60) as api:
        api.login(config.username, config.password)
        return api.get_monitors(), api.get_heartbeats()

def signal_handler(sig, frame):
    print(Style.SHOW_CURSOR, end="")
    print(Style.CLEAR, end="")
    sys.exit(0)

def main():
    config = load_config()
    
    if config.username == "YOUR_USERNAME_HERE":
        print(f"{Style.RED}Error: Configure credentials in ~/.kuma-dashboard.json{Style.RESET}")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    print(Style.HIDE_CURSOR, end="")
    
    was_night = False
    last_monitors = None
    last_heartbeats = None
    
    while True:
        try:
            current_night = is_night_time(config)
            
            if current_night and not was_night:
                blank_screen()
                was_night = True
            elif not current_night and was_night:
                was_night = False
            
            if not current_night:
                try:
                    monitors, heartbeats = fetch_data(config)
                    last_monitors, last_heartbeats = monitors, heartbeats
                    draw_dashboard(monitors, heartbeats, config)
                except Exception:
                    if last_monitors:
                        draw_dashboard(last_monitors, last_heartbeats, config)
            
            time.sleep(config.refresh_interval)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()