# HARDLINT V3 (9.5 EDITION) 🕵️‍♂️👻

**HARDLINT** is a professional-grade, modular OSINT framework designed for researchers and penetration testers. Version 3 introduces advanced anonymity layers ("Ghost Mode"), active network reconnaissance, and media forensics.

![Hardlint Logo](https://via.placeholder.com/800x200?text=HARDLINT+V3+GHOST)

## 🌟 New V3 "God Mode" Features

### 👻 Ghost Mode (Anonymity)
- **Tor Proxying**: Routes all traffic through a local Tor SOCKS5 proxy (default: 127.0.0.1:9050).
- **Random User-Agent**: Automatically rotates browser identities to bypass blocking and evade detection.
- **Toggle Command**: Access via `ghost` command inside the tool.

### 🖼️ Media Forensics
- **EXIF Extraction**: Extracts hidden metadata from images (GPS coordinates, Camera model, Timestamp).
- **OCR (Optical Character Recognition)**: Reads and extracts text active inside images (requires `tesseract-ocr`).

### 🛰️ Active Network Discovery
- **Port Scanner**: Checks target servers for open services (FTP, SSH, HTTP, RDP, etc.).
- **WiFi BSSID Tracker**: Geolocates a router significantly using its BSSID (MAC address).

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/itanbeluli12-debug/hardlint.git
   cd hardlint
   ```

2. **Set up Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   ./venv/bin/pip install -r requirements.txt
   ```

2. **System Requirements (V3):**
   - **Tor**: Required for Ghost Mode (`sudo apt install tor` -> `sudo service tor start`).
   - **Tesseract**: Required for OCR (`sudo apt install tesseract-ocr`).

3. **Run:**
   ```bash
   ./venv/bin/python hardlint.py
   ```

## 📖 Command Reference

| Module | Command | Description |
| :--- | :--- | :--- |
| **Anonymity** | `ghost` | **Toggle Ghost Mode** (ON/OFF). |
| **Identity** | `search <<username "name"` | Search 100+ sites. |
| | `search <<email "addr"` | Email analysis & Dorks. |
| | `search <<number "num"` | Reverse phone lookup. |
| **Media** | `search <<exif "url"` | **[NEW]** Extract GPS/EXIF data. |
| | `search <<ocr "url"` | **[NEW]** Extract text from image. |
| **Network** | `search <<scan "target"` | **[NEW]** Port Scanner. |
| | `search <<wifi "bssid"` | **[NEW]** WiFi Geolocation. |
| | `search <<ip "addr"` | IP Geolocation. |
| **Assets** | `search <<crypto "addr"` | Crypto Wallet Check. |
| | `search <<vin "vin"` | Vehicle VIN Decoder. |
| **Leaks** | `search <<leak "query"` | Search for leaks/pastes. |

## 🛡️ Privacy & Ethics
This tool is for **educational purposes only**. The use of "Active" scanning features (Port Scan) against unauthorized targets may be illegal. Always have permission before scanning.
