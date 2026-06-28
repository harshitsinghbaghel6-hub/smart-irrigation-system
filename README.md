# 🌱 Smart Irrigation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Arduino](https://img.shields.io/badge/Arduino-ESP32-teal?style=for-the-badge&logo=arduino)
![IoT](https://img.shields.io/badge/IoT-Enabled-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**An IoT-based automated irrigation system using ESP32 and soil moisture sensors to eliminate water wastage in agricultural fields.**

[Features](#features) • [Architecture](#architecture) • [Hardware Setup](#hardware-setup) • [Installation](#installation) • [Simulation](#simulation) • [Results](#results)

</div>

---

## 🎯 Problem Statement

Traditional farming wastes **30–50% of water** due to manual irrigation schedules that ignore actual soil conditions. This system solves that by automating irrigation based on **real-time soil moisture data** — no human intervention needed.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 Auto Pump Control | Turns pump ON/OFF based on moisture threshold |
| 📊 Live Dashboard | Real-time sensor data visualization in terminal |
| 🚨 Smart Alerts | Notifies when soil is critically dry or waterlogged |
| 📈 Data Logging | Stores all readings in SQLite for trend analysis |
| 🌐 Remote Monitor | View sensor data from anywhere via serial/Wi-Fi |
| 💧 Water Efficient | Reduces water usage by irrigating only when needed |
| 🔁 Simulation Mode | Test the full system without physical hardware |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FIELD LAYER                        │
│  [Soil Sensor] → [ESP32] → [Relay] → [Water Pump]  │
└─────────────────────┬───────────────────────────────┘
                      │ Serial / Wi-Fi
┌─────────────────────▼───────────────────────────────┐
│                  DATA LAYER                          │
│         Python Data Pipeline + SQLite DB            │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│               DASHBOARD LAYER                        │
│         Live Terminal Dashboard (Rich UI)            │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Hardware Setup

### Components Required

| Component | Quantity | Purpose |
|---|---|---|
| ESP32 / Arduino Uno | 1 | Main microcontroller |
| Soil Moisture Sensor (FC-28) | 1–4 | Read soil humidity |
| 5V Relay Module | 1 | Control water pump |
| Submersible Water Pump | 1 | Irrigation |
| Jumper Wires | ~20 | Connections |
| Breadboard | 1 | Prototyping |
| Power Supply (5V) | 1 | Power ESP32 |

### Wiring Diagram

```
ESP32 Pin Layout:
─────────────────────────────────────
  GPIO 34  ──────► Soil Sensor AOUT
  GPIO 2   ──────► Relay IN
  3.3V     ──────► Sensor VCC
  GND      ──────► Sensor GND / Relay GND
  VIN(5V)  ──────► Relay VCC
─────────────────────────────────────

Relay Output:
  COM  ──── Power Supply (+)
  NO   ──── Water Pump (+)
  Pump (-)  ──── Power Supply (-)
```

### Moisture Threshold Logic

```
Moisture Level    →    Action
──────────────────────────────
< 30%  (Dry)     →    Pump ON  🔴
30–70% (Optimal) →    Pump OFF 🟢
> 70%  (Wet)     →    Pump OFF ✅
```

---

## 📁 Project Structure

```
smart-irrigation-system/
│
├── src/
│   ├── esp32_firmware.ino      # Arduino/ESP32 firmware (C++)
│   ├── dashboard.py            # Live Python dashboard
│   ├── data_pipeline.py        # Data collection & storage
│   └── alert_system.py         # Threshold alerts
│
├── simulation/
│   └── simulator.py            # Run without hardware
│
├── docs/
│   └── setup_guide.md          # Detailed setup instructions
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/harshitsinghbaghel6-hub/smart-irrigation-system.git
cd smart-irrigation-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Flash ESP32 Firmware

- Open `src/esp32_firmware.ino` in **Arduino IDE**
- Select board: `ESP32 Dev Module`
- Select correct COM port
- Click **Upload**

### 4. Run the Dashboard

**With hardware connected:**
```bash
python src/dashboard.py --port COM3
```

**Without hardware (simulation mode):**
```bash
python simulation/simulator.py
```

---

## 🖥️ Simulation Mode

Don't have hardware? Run the full simulation:

```bash
python simulation/simulator.py
```

You'll see a live dashboard showing:
- Real-time moisture readings
- Pump ON/OFF status
- Alert history
- Data trends

---

## 📊 Results

| Metric | Before | After |
|---|---|---|
| Water Usage | Manual schedule | Need-based only |
| Human Effort | Daily monitoring | Zero intervention |
| Pump Runtime | Fixed hours/day | Only when soil is dry |
| Data Logging | None | Full SQLite history |

---

## 🛠️ Tech Stack

**Hardware**
- ESP32 / Arduino Uno
- FC-28 Soil Moisture Sensor
- 5V Relay Module

**Software**
- Python 3.10+
- Embedded C (Arduino IDE)
- SQLite3
- Rich (Terminal UI)

---

## 🔮 Future Improvements

- [ ] Add DHT11 for temperature & humidity monitoring
- [ ] Mobile app dashboard (Flutter/React Native)
- [ ] Weather API integration (skip irrigation if rain expected)
- [ ] Multiple zone support (4+ field sections)
- [ ] Solar power integration
- [ ] ML-based irrigation prediction model

---

## 👤 Author

**Harshit Singh**
- 🎓 B.Tech CSE-IoT — PSIT Kanpur
- 💼 [LinkedIn](https://linkedin.com/in/harshit-singh-eng)
- 🐙 [GitHub](https://github.com/harshitsinghbaghel6-hub)

---

## 📄 License

This project is licensed under the MIT License — feel free to use and modify it.

---

<div align="center">
⭐ Star this repo if you found it helpful!
</div>
