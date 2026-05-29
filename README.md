# 🕵️‍♂️ Fuinha Network Monitor (v3.0)

**From static log analysis to real-time network sentry.** Fuinha has evolved from a simple Bash log parser into a dynamic, real-time network monitoring tool designed for Information Security (IS) students and Junior SOC Analysts. It acts as a "Network Translator," mapping abstract data packets directly to system processes.

---

## 🚀 The Evolution
We moved beyond processing static `.log` files to dynamic monitoring using Python's `psutil` library. This allows the tool to sniff metrics directly from the OS Kernel (Windows/Linux), providing a live view of your machine's digital footprint.

---

## ✨ Key Features
- **Real-Time Monitoring**: Instant visualization of global Download and Upload throughput (MB/s).
- **Process Mapping**: Automatic identification of software (Brave, Discord, Steam, etc.) generating network traffic.
- **Process-Level Visibility**: See exactly how much bandwidth each application is using.
- **Visual Insights**: A dynamic pie chart showing bandwidth distribution among top processes.
- **Security Auditor (v4.0)**: Automatically scan local auth logs for intrusion attempts and brute-force attacks.
- **Open Ports Detector**: Real-time listing of all applications acting as servers and waiting for connections.
- **Insight Engine**: Plain-language tips ("Fuinha's Tip") to help manage your connection and alerts about upload saturation.
- **Smart Interface**: Modern Dark Mode dashboard built for high performance (RAM usage < 50MB) using `customtkinter`.
- **Custom Branding**: Features a unique geometric neon weasel icon across the UI and system tray.
- **Multilingual**: Support for Portuguese (PT-BR) and English (EN).
- **Cross-Platform**: Native support for Windows (.exe) and Linux (.deb).

---

## 🛠️ Tech Stack
* **Python 3.10+**: Core application logic.
* **Psutil**: Low-level system and network metric capture.
* **Modern GUI**: Hardware-accelerated interface (CustomTkinter/PySide).
* **Multi-Threading**: Decoupled network sniffing for a responsive UI.
* **Pillow**: Image processing for UI elements.
* **pystray**: (Optional) System tray integration.

---

## 📋 Project Roadmap
- [x] **Core Engine:** Traffic capture per Process ID (PID).
- [x] **UI v1.0:** Dashboard with global metrics and active process list.
- [x] **Data Viz:** Pie chart integration for bandwidth distribution (v3.0).
- [x] **Security Focus:** Flagging connections to suspicious IPs.
- [x] **System Tray:** Persistent background operation (Minimize to Tray).
- [x] **Internationalization:** Full support for Portuguese (PT-BR) and English (EN).

---

## 🔧 How to Run (Dev Environment)

### Linux
Fuinha requires `psutil` and `customtkinter`. To identify specific processes and their network usage on Linux, it is recommended to run as **Superuser (Sudo)**:

```bash
# Clone the repository
git clone https://github.com/vlacerda93/fuinha-network-monitor.git

# Navigate to the folder
cd fuinha-network-monitor

# Install dependencies
pip install -r requirements.txt

# Run the sentry
sudo python3 ver3.0/main.py
```

### Windows
Run with Administrator privileges to ensure all process names are captured correctly:

```powershell
python ver3.0/main.py
```

---
*Developed by Fuinha Team - Translating your internet for you.*
