"""
Smart Irrigation System — Simulator
=====================================
Run the full system WITHOUT physical hardware.
Simulates soil moisture readings and pump control.

Run:
    python simulation/simulator.py

Install:
    pip install rich
"""

import time
import random
import sqlite3
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.text import Text
    from rich import box
    RICH = True
    console = Console()
except ImportError:
    RICH = False

# ── Config ─────────────────────────────────────
DB_PATH        = "irrigation_data.db"
DRY_THRESHOLD  = 30     # % below → pump ON
WET_THRESHOLD  = 70     # % above → pump OFF
READ_INTERVAL  = 3      # seconds between readings

# ── Database ────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            moisture   REAL,
            pump_on    INTEGER,
            timestamp  TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_reading(moisture: float, pump_on: bool):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO readings (moisture, pump_on, timestamp) VALUES (?, ?, ?)",
        (round(moisture, 1), int(pump_on), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_history(limit=12):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT moisture, pump_on, timestamp FROM readings ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return list(reversed(rows))

# ── Sensor Simulation ───────────────────────────
_moisture = 50.0
_pump_on  = False

def simulate_moisture(pump_on: bool) -> float:
    global _moisture
    # When pump is ON, moisture rises; otherwise it drifts down slowly
    if pump_on:
        change = random.uniform(1.0, 3.5)
    else:
        change = random.uniform(-2.0, 0.3)
    _moisture = max(0.0, min(100.0, _moisture + change))
    return round(_moisture, 1)

def control_pump(moisture: float, pump_on: bool) -> bool:
    if moisture < DRY_THRESHOLD:
        return True
    if moisture >= WET_THRESHOLD:
        return False
    return pump_on   # Keep current state in middle zone

# ── Sparkline ───────────────────────────────────
def sparkline(values, width=20):
    bars = "▁▂▃▄▅▆▇█"
    if not values: return "─" * width
    mn, mx = min(values), max(values)
    span = mx - mn or 1
    chars = [bars[min(7, int((v - mn) / span * 7))] for v in values]
    return "".join(chars[-width:]).ljust(width)

# ── Dashboard ───────────────────────────────────
def render(moisture, pump_on, total_readings):
    history = get_history()
    hist_vals = [h[0] for h in history]
    spark = sparkline(hist_vals)

    # Moisture bar
    filled = int(moisture / 5)
    bar = "█" * filled + "░" * (20 - filled)

    if moisture < DRY_THRESHOLD:
        m_color = "red"
        status_text = "🔴 DRY — Pump ON"
    elif moisture > WET_THRESHOLD:
        m_color = "blue"
        status_text = "💧 WET — Pump OFF"
    else:
        m_color = "green"
        status_text = "✅ OPTIMAL — Pump Off"

    pump_color = "red" if pump_on else "dim"
    pump_str   = "🔴 RUNNING" if pump_on else "⚫ IDLE"

    lines = Text()
    lines.append(f"\n  Moisture   : ", style="bold")
    lines.append(f"{moisture}%", style=f"bold {m_color}")
    lines.append(f"\n  Status     : {status_text}\n")
    lines.append(f"  Water Pump : ", style="bold")
    lines.append(f"{pump_str}\n", style=pump_color)
    lines.append(f"\n  [{m_color}]{bar}[/{m_color}]  {moisture}%\n")
    lines.append(f"  Trend      : [{m_color}]{spark}[/{m_color}]\n")
    lines.append(f"\n  Dry < {DRY_THRESHOLD}%  |  Optimal {DRY_THRESHOLD}–{WET_THRESHOLD}%  |  Wet > {WET_THRESHOLD}%\n", style="dim")
    lines.append(f"  Readings logged: {total_readings}  |  DB: {DB_PATH}\n", style="dim")

    return Panel(lines,
        title="[bold cyan]🌱 Smart Irrigation System — Live Monitor[/bold cyan]",
        subtitle=f"[dim]{datetime.now().strftime('%H:%M:%S')} | Press Ctrl+C to stop[/dim]",
        border_style="cyan"
    )

# ── History Table ───────────────────────────────
def show_history():
    history = get_history(10)
    if not RICH:
        print("\nLast readings:")
        for m, p, ts in history:
            print(f"  {ts[-8:]}  Moisture: {m}%  Pump: {'ON' if p else 'OFF'}")
        return
    table = Table(box=box.SIMPLE, title="[cyan]Last 10 Readings[/cyan]")
    table.add_column("Time",     style="dim")
    table.add_column("Moisture", justify="right")
    table.add_column("Pump",     justify="center")
    for m, p, ts in history:
        pump_str = "[red]ON[/red]" if p else "[dim]OFF[/dim]"
        color = "red" if m < 30 else "green" if m < 70 else "blue"
        table.add_row(
            ts[-8:],
            f"[{color}]{m}%[/{color}]",
            pump_str
        )
    console.print(table)

# ── Main ────────────────────────────────────────
def main():
    global _pump_on
    init_db()
    total = 0

    if not RICH:
        print("Install 'rich' for the full dashboard: pip install rich")
        print("Running in basic mode...\n")
        while True:
            moisture = simulate_moisture(_pump_on)
            _pump_on = control_pump(moisture, _pump_on)
            save_reading(moisture, _pump_on)
            total += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}]  Moisture: {moisture}%  Pump: {'ON' if _pump_on else 'OFF'}")
            time.sleep(READ_INTERVAL)
        return

    console.print(Panel(
        "[bold cyan]🌱 Smart Irrigation Simulator[/bold cyan]\n"
        "[dim]Simulating ESP32 + Soil Moisture Sensor[/dim]",
        border_style="cyan"
    ))
    time.sleep(1)

    with Live(render(50.0, False, 0), refresh_per_second=1, screen=True) as live:
        while True:
            moisture = simulate_moisture(_pump_on)
            _pump_on = control_pump(moisture, _pump_on)
            save_reading(moisture, _pump_on)
            total += 1
            live.update(render(moisture, _pump_on, total))
            time.sleep(READ_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]Simulation stopped. Showing history...[/bold cyan]\n")
        show_history()
        console.print(f"\n[dim]All data saved to {DB_PATH}[/dim]\n")
