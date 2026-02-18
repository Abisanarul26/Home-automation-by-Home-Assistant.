# 🏠 Home Assistant: Integrated Energy & Security Ecosystem

This repository documents an advanced home automation ecosystem hosted on a **Raspberry Pi**. The project features a multi-inverter solar management system, a custom Python-based security pipeline with Azure cloud synchronization, and AI-powered threat detection.

---

## 🏗️ System Architecture

### 1. Energy Management Tier (Solar & Storage)
The system operates as a professional-grade Energy Management System (EMS), monitoring complex power flows and battery health.

* **Inverter Integration:** Simultaneous local and cloud monitoring of **GoodWe** (UDP), **Deye** (Modbus TCP), and **Growatt** (MQTT via Grott).
* **Battery Analytics (JK BMS):** Detailed 32-cell monitoring via **Batmon (MQTT)** and BLE.
* **Range Extension:** Deployed an **ESP32** using **ESPHome Bluetooth Proxy** to bridge the BMS signal to the Raspberry Pi over Wi-Fi. [View Config](./esphome/jk-bms-proxy.yaml)
* **Appliance Tracking:** High-precision **Athom Tasmota** smart plugs monitoring Power, Voltage, and Current via MQTT.

### 2. Intelligent Security & AI Surveillance
A tiered security architecture that combines local AI processing with off-site cloud redundancy.

* **AI Detection (Frigate NVR):** Local AI human detection using Frigate to eliminate false motion alerts.
* **Real-time Streams:** Zero-latency monitoring via **WebRTC** and optimized **RTSP** streams for EZVIZ hardware.
* **Storage Pipeline (AppDaemon):** A custom Python-based "Store-and-Forward" system. [View Script](./appdaemon/azure_test.py)
    * **Local Tier:** 15-minute segments saved to a local SSD with a **7-day rolling retention policy**.
    * **Cloud Tier:** Synchronized mirroring to **Azure Blob Storage** with a **30-day lifecycle policy**.
* **Smart Notifications:** Critical alerts with person-thumbnails sent via the Home Assistant Companion App upon verified human detection.

### 3. Climate & Infrastructure Control
* **HVAC Bridge:** Non-smart AC units are integrated via an **IR-to-MQTT bridge**, providing full control over modes, temperature, and power.
* **Assumed State Logic:** Custom automation logic tracks the one-way IR commands to maintain a virtual state of the AC unit on the dashboard.

---

## 🎨 User Experience & Dashboard
The UI follows a **Glassmorphism** aesthetic, optimized for high-performance navigation on low-power tablets or mobile devices.

* **Design:** Customized **Frosted Glass Lite** theme (by wessamlauf) using CSS-blur and translucent layers.
* **Navigation:** A **Subview Architecture** keeps the main interface clean, with dedicated deep-dive pages for A/C, Camera, Energy, and Battery systems.
* **Command Center:** A 6-camera live grid provides instant perimeter awareness.

![Dashboard View](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/dashboard.png)

---

## 🤖 Automations & Logical Layers
| Category | Logic Description |
| :--- | :--- |
| **Load Shedding** | Toggling smart plugs based on Inverter SoC and PV production thresholds. |
| **Peak Shaving** | Automatic deactivation of non-essential loads when grid usage exceeds limits. |
| **Watchdog** | Monitoring ESPHome Proxy connectivity to prevent battery deep-discharge. |
| **Data Cleanup** | Scheduled Python tasks at 2:00 AM to purge local recordings older than 7 days. |

---

## 🛠️ Technical Stack
* **OS:** Home Assistant OS (Raspberry Pi)
* **Languages:** YAML (Automations), Python (AppDaemon)
* **Protocols:** MQTT, Modbus TCP, RTSP, ONVIF, BLE, OCPP
* **Integrations:** HACS, WebRTC, ESPHome, Frigate, Solarman, Batmon

---

## 🚀 Future Roadmap
* **Mini-Grid Project:** Integration of 55kW Solar and 10kW Wind data following Sri Lankan microgrid standards.
* **EV Ecosystem:** Integration of EV vehicle telemetry and smart **OCPP EV Charger** management.
* **Zigbee Expansion:** Deploying a Zigbee mesh for environment sensors and lighting.
* **Smart CT Clamps:** Direct grid consumption tracking for higher accuracy.

---
