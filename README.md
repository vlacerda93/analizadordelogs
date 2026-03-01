# 🕵️‍♂️ Fuinha Network Monitor (v3.0)

**From static log analysis to real-time network sentry.** Fuinha has evolved from a simple Bash log parser into a dynamic, real-time network monitoring tool designed for Information Security (IS) students and Junior SOC Analysts. It acts as a "Network Translator," mapping abstract data packets directly to system processes.

---

## 🚀 The Evolution
We moved beyond processing static `.log` files to dynamic monitoring using Python's `psutil` library. This allows the tool to sniff metrics directly from the OS Kernel (Windows/Linux), providing a live view of your machine's digital footprint.

---

## ✨ Key Features
* **Real-Time Monitoring:** Instant visualization of global Download and Upload throughput.
* **Process Mapping:** Automatic identification of software (Brave, Discord, Steam, etc.) generating network traffic.
* **Smart Interface:** Modern Dark Mode dashboard built for high performance (RAM usage < 50MB).
* **Insight Engine:** A built-in logic system that alerts users about upload saturation.
* **Cross-Platform:** Native support for Windows (.exe) and Linux (.deb).

---

## 🛠️ Tech Stack
* **Python 3.x:** Core application logic.
* **Psutil:** Low-level system and network metric capture.
* **Modern GUI:** Hardware-accelerated interface (CustomTkinter/PySide).
* **Multi-Threading:** Decoupled network sniffing for a responsive UI.

---

## 📋 Project Roadmap
- [x] **Core Engine:** Traffic capture per Process ID (PID).
- [x] **UI v1.0:** Dashboard with global metrics and active process list.
- [ ] **Data Viz:** Donut chart integration for bandwidth distribution.
- [ ] **Security Focus:** Flagging connections to suspicious IPs.
- [ ] **System Tray:** Persistent background operation (Minimize to Tray).
- [ ] **Internationalization:** Full support for Portuguese (PT-BR) and English (EN).

---

## 🔧 How to Run (Dev Environment)
```bash
# Clone the repository
git clone [https://github.com/vlacerda93/fuinha-network-monitor.git](https://github.com/vlacerda93/fuinha-network-monitor.git)

# Navigate to the folder
cd fuinha-network-monitor

# Instale as dependencias
pip install -r requirements.txt

# Run the sentry
python3 main.py
