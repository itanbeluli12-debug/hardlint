# HARDLINT V4 - Intelligence Edition 🕵️‍♂️🧠🕸️

> [!IMPORTANT]
> **Hardlint** is a professional-grade asynchronous OSINT framework designed for ethical security researchers and intelligence analysts. V4 "Intelligence" transforms the tool into a full-scale analysis platform.

---

## 🌟 Advanced Intelligence Features

### 🧠 AI Dossier Analyst
Synthesize raw data into actionable intelligence. Hardlint leverages local LLMs (via **Ollama**) to generate professional reports without compromising data privacy.
- **Command**: `analyze` - Generates a structured dossier from the current session.

### 🕸️ Interactive Investigation Dashboard
Visualize connections between entities using a real-time Graph UI. 
- **Command**: `dashboard`
- **Interface**: `http://localhost:5000`

### 👻 Ghost Mode & Anonymity
Stay hidden during investigations with multi-layered anonymity.
- **Tor Routing**: Optional SOCKS5 proxying for all modules.
- **Fingerprint Rotation**: Dynamic User-Agent randomization.
- **VPN Integration**: Native support for Mullvad VPN CLI.
- **Command**: `ghost` (Tor) / `vpn` (Mullvad)

---

## 🛠️ Modules & Capabilities

| category | Module | Syntax | Description |
| :--- | :--- | :--- | :--- |
| **Identity** | `username` | `search <<username "name"` | Scan 100+ social platforms. |
| | `email` | `search <<email "addr"` | Breach check & deep dorks. |
| | `number` | `search <<number "phone"` | Reverse phone lookup. |
| **Forensics** | `exif` | `search <<exif "url"` | Metadata & GPS extraction. |
| | `ocr` | `search <<ocr "url"` | Text recognition in images. |
| | `image` | `search <<image "url"` | Reverse image search links. |
| **Network** | `ip` | `search <<ip "addr"` | Geolocation & Threat Intel. |
| | `scan` | `search <<scan "target"` | Active Port Scanner. |
| | `wifi` | `search <<wifi "bssid"` | BSSID geolocation. |
| **Web** | `domain` | `search <<domain "site"` | DNS, WHOIS, Subdomains. |
| | `darkweb` | `search <<darkweb "query"`| Search Onion sites via Tor. |
| | `leak` | `search <<leak "query"` | Pastebin & breach lookup. |
| **Assets** | `crypto` | `search <<crypto "addr"`| Blockchain wallet analysis. |
| | `vin` | `search <<vin "vin"` | Vehicle VIN decoder. |
| **Red Team** | `phishing` | `launch <template>` | Start Social Engineering sim. |

---

## 🚀 Installation & Setup

1. **System Dependencies**:
   ```bash
   # Debian/Ubuntu
   sudo apt install tor tesseract-ocr mullvad-vpn
   sudo service tor start
   ```

2. **Environment Setup**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Execution**:
   ```bash
   python hardlint.py
   ```

---

## ⚖️ Legal & Ethical Disclaimer

> [!CAUTION]
> **READ CAREFULLY BEFORE USE.**

This tool is provided for **educational and authorized security testing purposes only**. The developers of Hardlint assume no liability for any misuse or damage caused by this program.

### 1. Authorized Use
You may only use Hardlint on systems and entities for which you have explicit, written permission. Unauthorized use against third-party systems is illegal and unethical.

### 2. Regulatory Compliance
Users are responsible for complying with all local, national, and international laws, including but not limited to:
- **GDPR / CCPA**: Handling of Personal Identifiable Information (PII).
- **Computer Misuse Act**: Unauthorized access to computer material.
- **CFAA**: Computer Fraud and Abuse Act.

### 3. Ethical Boundaries
- Never use this tool for stalking, harassment, or malicious doxing.
- Respect the privacy of individuals.
- Use the gathered data responsibly.

### 4. No Warranty
This software is provided "as is", without warranty of any kind, express or implied. Use at your own risk.

---
*Developed by **mrhardlint** | [GitHub Repository](https://github.com/mrhardlint/hardlint)*
