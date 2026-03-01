# Fuinha - Network Translator 🕵️‍♂️📈

**Fuinha** is a user-centric network monitoring tool designed to demystify internet usage for everyday users. Unlike technical packet sniffers, Fuinha acts as a "Network Translator," mapping abstract data flows into recognizable desktop applications (e.g., YouTube, Torrent, Spotify).

The primary mission is to solve the "Why is my internet slow?" mystery by visually highlighting who is "eating" your bandwidth in real-time.

## ✨ Features

- **Global Speed Header**: High-visibility Download and Upload indicators (MB/s).
- **Process-Level Visibility**: See exactly how many KB/s each application is using.
- **Visual Insights**: A dynamic pie chart showing bandwidth distribution.
- **Insight Engine**: Plain-language tips ("Fuinha's Tip") to help manage your connection.
- **Lightweight & Fast**: Built with Python and `customtkinter` with zero heavy dependencies.
- **Multilingual**: Support for Portuguese (BR) and English.

## 🚀 How to Run

### Linux

Fuinha requires `psutil` and `customtkinter`. To identify specific processes and their network usage on Linux, it is recommended to run as **Superuser (Sudo)**:

```bash
sudo python3 main.py
```

### Windows

Run with Administrator privileges to ensure all process names are captured correctly:

```powershell
python main.py
```

## 🛠️ Requirements

- Python 3.10+
- `psutil`
- `customtkinter`
- `Pillow`
- `pystray` (optional for tray icon)

## 🏗️ Version 3.0 Highlights

This version represents a complete refactor focused on **Aesthetics** and **User Clarity**:
- New **Deep Dark** UI theme.
- Custom **PieChart** widget using pure `tkinter.Canvas`.
- Weighted distribution model for per-process bandwidth estimation.

---
*Developed by Fuinha Team - Translating your internet for you.*
