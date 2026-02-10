# Home Assistant Setup: Smart Power & Infrastructure

This repository documents my home automation journey using **Home Assistant** hosted on a **Raspberry Pi**. The focus of this project is to integrate local control for power monitoring, security, smart devices and climate systems while maintaining high reliability and data privacy.

## 🛠 Hardware Profile
* **Controller:** Raspberry Pi
* **Protocol Focus:** MQTT (via Tasmota), OCPP, RTSP/ONVIF, and IP-based API integrations.

## ⚡ Integrated Systems

## 📊 1. Solar Inverter Tier (Core Energy Flow)
The system monitors total production, grid export/import, and battery state of charge (SoC) through a multi-inverter setup.

### Supported Inverters & Integrations
* **GoodWe:** Uses the **Core GoodWe Integration**. It polls data locally via UDP (Port 8899).
* **Deye:** Integrated via the **Solarman (HACS)** or **Modbus TCP** integration for real-time register access.
* **Growatt:** Connects via the **Growatt Server** integration (Cloud/API) or **Grott (MQTT)** for local data interception.

### Key Monitoring Metrics
* **Grid Usage:** Real-time import/export tracking via inverter CT clamps.
* **Battery Analytics:** Charge/Discharge rates and SoC directly from the hybrid inverter bus.

## 🔌 2. Device Tier (Appliance Monitoring)
Individual appliance tracking is handled by high-precision smart plugs to identify "energy vampires" and automate load shedding.
* **Hardware:** Athom Tasmota Smart Plugs.
* **Integration:** **MQTT** (Mosquitto Broker).
* **Data Points:** Power (W), Voltage (V), Current (A), and Daily Energy (kWh).

## 🔋 3. Battery Management Tier (BMS & Connectivity)
Advanced battery health monitoring for DIY or custom lithium banks.

### JK BMS Integration
* **Primary Integration:** **Batmon (via MQTT)**. This allows for detailed cell-level monitoring (32 cells), balancing status, and temperature alerts.
* **Connection Method:** Bluetooth Low Energy (BLE).

### Bluetooth Range Extension (ESP32 Proxy)
To overcome the short range of the JK BMS Bluetooth module, an **ESP32** is used as a transparent bridge.
* **Software:** **ESPHome**.
* **Feature:** `bluetooth_proxy`.
* **Architecture:** The ESP32 is placed physically near the battery bank. It captures the BLE signal from the JK BMS and forwards it over the local Wi-Fi network to Home Assistant, effectively making the BMS "network-attached."



## 🛠 Technical Stack
| Layer | Technology |
| :--- | :--- |
| **OS** | Home Assistant OS (Raspberry Pi) |
| **BMS Communication** | Batmon + BLE |
| **Range Extension** | ESPHome Bluetooth Proxy |
| **IoT Protocol** | MQTT / Modbus TCP |
| **Dashboard** | Energy Dashboard (Native) |

### 2. Surveillance & Security
Configured high-definition video feeds using **Hikvision** cameras. 
* **Protocols:** Utilized **RTSP** for low-latency streaming and **ONVIF** for PTZ/event management.
* **Security:** Implemented specific user permissions within the Hikvision NVR/Camera settings to ensure Home Assistant has secure, restricted access.

### 3. Climate Control
Explored the integration of the **AirTouch 5** controller to manage ducted air conditioning systems, focusing on zone control and temperature feedback within the HA dashboard.

## 🤖 Automations & Logic
The system is built using the standard Home Assistant Automation engine, focusing on:
* **Triggers:** State changes from smart plugs and schedule-based events.
* **Conditions:** Ensuring actions only occur during specific time windows or power thresholds.
* **Actions:** Notifying or switching devices based on the logic above.

## 📊 Dashboard UI
The Lovelace dashboard is customized for quick at-a-glance monitoring:
* **Energy Cards:** Visualizing current draw and daily consumption.
* **Live Feeds:** Integration of RTSP camera streams for perimeter monitoring.

## 🚀 Future Roadmap
* Integrate Solar PV and Wind Turbine data (Mini-grid project integration).
* Expand Modbus communication for industrial-grade sensor data.
* Refine automation logic for load shedding based on energy production.
