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

## 📹 4. Advanced Surveillance & Edge-to-Cloud Pipeline

This section covers the implementation of a lag-free monitoring system using **EZVIZ** hardware, bypassing proprietary cloud subscriptions in favor of a custom-built local and cloud storage architecture.

### 🚀 High-Performance Live Streaming
To achieve sub-second latency for real-time monitoring:
* **Hardware:** EZVIZ High-Definition Cameras. 
* **Integration:** **Frigate Advance Camera card** via HACS. 
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

## 🕵️‍♂️ AI-Powered Object Detection (Frigate NVR)

To reduce "noise" from motion alerts (wind, light changes, animals), I integrated **Frigate NVR** to handle sophisticated local AI object detection.

### 🧠 Human Detection & Real-Time Intelligence
* **Detection Engine:** Leveraged Frigate's real-time AI processing to distinguish humans from other moving objects. 
* **Edge Processing:** The system performs all AI inference locally on the Raspberry Pi, ensuring zero reliance on external cloud AI services for privacy and speed.
* **Notification Engine:** Configured an automation pipeline that sends high-priority **Mobile Notifications** (via the Home Assistant Companion App) only when a human is identified within specific zones.

### 📲 Smart Alert Automation
Instead of constant motion alerts, the system utilizes the following logic:
1. **Frigate** identifies a person in the camera feed.
2. A **MQTT** message is sent to Home Assistant with the detection confidence score.
3. Home Assistant triggers a mobile notification including a **snapshot** of the person and a direct link to the live stream.

## ❄️ 5. HVAC & Climate Control (IR Integration)

To integrate non-smart Air Conditioning units into the ecosystem, I implemented a custom IR-to-MQTT bridge, enabling full granular control without hardware modifications.

### 🎨 Customized Climate Dashboard
Instead of a standard button interface, I developed a customized **Lovelace Climate Dashboard** that provides a high-end UI experience:
* **Real-time Feedback:** Visual indicators for current mode and target temperature.
* **State Sync:** Logic implemented to track the "assumed state" of the AC unit based on the last sent MQTT command.
* ![AC control Dashboard](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/AC.png)


## 🎨 6. Dashboard UI & User Experience

The interface is built with a focus on high-visibility and intuitive navigation, utilizing a modern **Glassmorphism** aesthetic to provide a clean, professional "Command Center" feel.

### 🖼️ Design Philosophy
* **Core Theme:** The visual foundation is built on the [Frosted Glass Theme by wessamlauf](https://github.com/wessamlauf/homeassistant-frosted-glass-themes). This theme brings depth through transparent, blurred card elements and a cohesive color palette.
* **Editions Used:** I utilize the **Lite Edition** for high-performance navigation on the Raspberry Pi, which maintains the glassy look without the heavy processing load of backdrop filters.
* **Customization:** Leveraging the **Frosted Glass Theme Manager**, I have customized the primary colors and backgrounds to match a "Frosted Glass Lite" profile, ensuring comfortable usability and visual appeal.

### 🕹️ Multi-Stream Surveillance & Navigation
* **Subview Architecture:** To maintain a clean primary interface, the dashboard uses navigation-based subviews for **A/C, Camera, Energy,** and **Battery**. 
* **Live Multi-View:** The right-hand panel features a 6-camera grid utilizing **WebRTC** for real-time surveillance monitoring.

### 🖥️ Dedicated Hardware Interface
* **Display Hardware:** Integrated a **Waveshare 7-inch LCD Touchscreen** connected directly to the Raspberry Pi via the DSI/HDMI interface.
* **Kiosk Environment:** Implemented the **HAOS Kiosk Display** add-on. This allows Home Assistant to boot directly into the dashboard as a standalone hardware appliance.
* **System Optimization:** By utilizing a dedicated kiosk environment, the system bypasses the overhead of a standard Linux desktop GUI, significantly reducing CPU and RAM usage on the Raspberry Pi.
* **UI Refinement:** Leveraged the **Kiosk Mode** frontend integration to hide the sidebar and top header, ensuring a seamless, "app-like" experience on the 7-inch display.

![Dashboard Main View](https://github.com/Abisanarul26/Home-automation-by-Home-Assistant./blob/main/images/dashboard.png)


## 🚀 Future Roadmap
The project continues to evolve with the following planned upgrades:
* **Mini-Grid Integration:** Full integration of **Solar PV (55kW)** and **Wind Turbine (10kW)** data for Sri Lankan microgrid standards.
* **EV Ecosystem:** Integration of EV vehicle telemetry and smart **EV Charger** management.
* **Advanced Sensing:** Expansion into **Zigbee** mesh networks for motion sensors and smart lighting.
* **Smart Analytics:** Implementing AI-based **Smart Motion Detection** for security cameras and high-accuracy **Smart CT Clamps** for direct grid consumption tracking.
* **Load Shedding:** Refining automation logic to prioritize essential loads based on real-time energy production.
