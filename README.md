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

![Battery Monitoring Dashboard](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/Screenshot%202026-02-05%20122107.png)


## 🛠 Technical Stack
| Layer | Technology |
| :--- | :--- |
| **OS** | Home Assistant OS (Raspberry Pi) |
| **BMS Communication** | Batmon + BLE |
| **Range Extension** | ESPHome Bluetooth Proxy |
| **IoT Protocol** | MQTT / Modbus TCP |
| **Dashboard** | Energy Dashboard (Native) |

## 📹 2. Advanced Surveillance & Edge-to-Cloud Pipeline

This section covers the implementation of a lag-free monitoring system using **EZVIZ** hardware, bypassing proprietary cloud subscriptions in favor of a custom-built local and cloud storage architecture.

### 🚀 High-Performance Live Streaming
To achieve sub-second latency for real-time monitoring:
* **Hardware:** EZVIZ High-Definition Cameras. 
* **Integration:** **WebRTC Camera** via HACS. 
* **Protocol:** Optimized **RTSP** streams used to eliminate the 5-10 second delay typically found in standard cloud-based viewers, ensuring a "lag-free" dashboard experience without an EZVIZ Cloud subscription.

### 💾 Automated Local Storage Logic
Managed via Home Assistant Automations to ensure data redundancy on the **Raspberry Pi's mounted SSD**:
* **Segmentation:** High-definition streams are captured and stored in 15-minute intervals.
* **Organization:** A custom script distinguishes feeds from **6 individual cameras**, automatically applying standardized naming conventions: `[Camera_Name]_[YYYY-MM-DD_HH-MM]`.
* ![CCTV Backup automation control dashboard](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/Backup.png)

### ☁️ Azure Cloud Sync & AppDaemon Pipeline
To ensure off-site data security, I implemented a Python-based synchronization pipeline using the **AppDaemon** add-on.
* **Dual-Write Strategy:** As soon as a recording is finalized on the local SSD, the AppDaemon script triggers a background upload to an **Azure Blob Storage** container.
* **Logic:** Written in **Python**, this handles the API handshake with Azure, ensuring the cloud copy is an exact mirror of the local repository.

### 🧹 Automated Lifecycle Management (Retention Policy)
To prevent storage overflow and manage costs, I implemented a tiered data retention policy:
* **Local Tier (SSD):** A delayed operation within the AppDaemon Python code automatically purges files older than **7 days**.
* **Cloud Tier (Azure):** Utilizing **Azure Lifecycle Management Policies**, the container is configured to automatically delete blobs after **30 days**, providing a rolling 1-month archive of all security footage. 

| Storage Layer | Retention | Management Method |
| :--- | :--- | :--- |
| Local SSD | 7 Days | AppDaemon (Python) |
| Azure Cloud | 30 Days | Container Lifecycle Management |

## ❄️ 3. HVAC & Climate Control (IR Integration)

To integrate non-smart Air Conditioning units into the ecosystem, I implemented a custom IR-to-MQTT bridge, enabling full granular control without hardware modifications.

### 📡 IR Blaster Architecture
* **Protocol:** **MQTT**. The IR blaster acts as an MQTT client, receiving payload commands from Home Assistant and translating them into specific infrared pulse sequences.
* **Control Scope:** * **Power:** Discrete On/Off commands.
    * **Temperature:** Precise set-point adjustments.
    * **Mode Management:** Seamless switching between Cool, Heat, Fan, and Dry modes.

### 🎨 Customized Climate Dashboard
Instead of a standard button interface, I developed a customized **Lovelace Climate Dashboard** that provides a high-end UI experience:
* **Real-time Feedback:** Visual indicators for current mode and target temperature.
* **State Sync:** Logic implemented to track the "assumed state" of the AC unit based on the last sent MQTT command.
* ![AC control Dashboard](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/AC.png)

## 🤖 4. Automations & Intelligent Logic

The core of this system is a multi-tier automation engine that manages energy distribution, security data pipelines, and hardware protection.

### ⚡ Energy & Load Management
Utilizing real-time data from the **GoodWe, Deye, and Growatt inverters**, the system performs intelligent load shedding:
* **Dynamic Thresholds:** Smart plugs (Athom Tasmota) are toggled based on battery State of Charge (SoC) and PV production.
* **Peak Shaving:** Non-essential loads are automatically deactivated when grid usage exceeds defined amperage limits.

### 📂 Security Data Pipelines (AppDaemon & Python)
Unlike standard automations, the surveillance system uses **AppDaemon** to handle file-system-level operations:
* **Trigger:** Completion of a 15-minute recording segment.
* **Action:** Simultaneous local write to SSD and asynchronous upload to **Azure Blob Storage**.
* **Retention Logic:** A Python-based cleanup script runs on a 7-day delay for local storage, ensuring the Raspberry Pi SSD never reaches capacity.

### 🌡 Climate Intelligence
* **Assumed State Logic:** Since IR is a one-way protocol, the automation engine tracks the "last sent command" via MQTT to maintain a virtual state in the dashboard.
* **Scheduled Comfort:** Temperature set-points are adjusted based on time-of-day and room occupancy sensors.

### 🛡 System Health & Monitoring
* **Connectivity Watchdog:** Monitors the **ESPHome Bluetooth Proxy**; if the connection to the JK BMS is lost, the system sends an urgent notification to prevent battery deep-discharge.
* **Storage Alerts:** Notifies if the Azure upload fails or if the local SSD health degrades. Notifying or switching devices based on the logic above.

## 📊 Dashboard UI
The Lovelace dashboard is customized for quick at-a-glance monitoring:
* **Energy Cards:** Visualizing current draw and daily consumption.
* **Live Feeds:** Integration of RTSP camera streams for perimeter monitoring.

## 🚀 Future Roadmap
* Integrate Solar PV and Wind Turbine data (Mini-grid project integration).
* Expand Modbus communication for industrial-grade sensor data.
* Refine automation logic for load shedding based on energy production.
