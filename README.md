# Kali Linux All-in-One Ethical Hacking Tool

![Banner](assets/banner.png)

> **⚠ WARNING**: This tool is for **legal security testing only**. Unauthorized use is illegal. [See full disclaimer](#-legal-notice)

---

## 📖 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Tool Documentation](#-tool-documentation)
- [Legal Notice](#-legal-notice)
- [Contributing](#-contributing)

---

## ✨ Features
| Tool Category       | Functionality                          |
|---------------------|---------------------------------------|
| **Hash Cracking**   | MD5, SHA1, SHA256, SHA512             |
| **Wi-Fi Security**  | WPA/WPA2 handshake capture & cracking |
| **Network Recon**   | Nmap scanning, OS detection           |
| **Brute Force**     | SSH, FTP, RDP attacks                 |
| **Automation**      | Metasploit payload generator          |

---

## 🛠 Installation

### Prerequisites
- Kali Linux 2023.x or newer
- Python 3.10+
- Root/sudo access (for Wi-Fi tools)

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/kali-all-in-one-tool.git
   cd kali-all-in-one-tool

2. **Install dependencies**:

 ```bash
sudo apt update && sudo apt install -y \
aircrack-ng hydra nmap macchanger \
python3-pip
pip3 install -r requirements.txt

3. **Make executable**:

```bash
chmod +x kali_tool.py

4. **Run with root privileges**:

 ```bash
sudo ./kali_tool.py
