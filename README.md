# HARDLINT V4 (INTELLIGENCE EDITION) 🕵️‍♂️🧠🕸️

**HARDLINT** is an advanced, high-performance asynchronous OSINT framework. Version 4 transforms it into a full-scale intelligence platform with AI-driven analysis, interactive visualization, and an anonymity layer.

## 🌟 New V4 "Intelligence" Features

### 🧠 AI Dossier Analyst
- **Automated Reporting**: Synthesizes all gathered intelligence into a professional report.
- **Privacy First**: Defaults to **Ollama** (Local LLM) for secure, offline analysis.
- **Command**: Type `analyze` in the shell.

### 🕸️ Interactive Relationship Map (Graph UI)
- **Visual Investigation**: A web-based dashboard showing connections between aliases, emails, and data points.
- **Real-time Sync**: Updates automatically as you run searches.
- **Command**: Type `dashboard` and visit `http://localhost:5000`.

### 👻 Ghost Mode (Advanced Anonymity)
- **Tor Routing**: All outgoing requests are optionally routed through the Tor network.
- **Identity Obfuscation**: Randomizes User-Agents for every request to prevent fingerprinting.
- **Command**: Type `ghost` to toggle.

### 📜 Page-based History Navigation
- **State Persistence**: Navigate between previous search results using browser-like history commands.
- **Commands**: Type `back` or `next`.

### ⚡ Async Core
- **Performance**: High-speed parallel scanning of 100+ platforms using `aiohttp`.

---

## 🚀 Installation

1. **System Requirements:**
   - **Tor**: Required for Dark Web & Ghost Mode (`sudo apt install tor` -> `sudo service tor start`).
   - **Tesseract**: Required for OCR (`sudo apt install tesseract-ocr`).

2. **Setup (Virtual Environment):**
   ```bash
   python3 -m venv venv
   ./venv/bin/pip install -r requirements.txt
   ```

3. **Run:**
   ```bash
   ./venv/bin/python hardlint.py
   ```

## 📖 Command Reference

| Category | Command | Description |
| :--- | :--- | :--- |
| **Intelligence** | `analyze` | Generate AI Dossier. |
| | `dashboard` | Launch Web Graph UI. |
| | `show_data` | Review collected session data. |
| **Anonymity** | `ghost` | Toggle Tor Proxy + Random UA. |
| **Dark Web** | `search <<darkweb "query"` | Search Onion sites (Ahmia). |
| **Social** | `search <<username "name"`| High-speed 100+ site lookup. |
| | `search <<email "addr"` | Gravatar & Deep Dorks. |
| | `search <<number "phone"` | Reverse phone lookup. |
| **Network** | `search <<ip "addr"` | Geolocation & Threat intel. |
| | `search <<mac "addr"` | MAC Vendor lookup. |
| | `search <<scan "target"` | Active Port Scanner. |
| | `search <<wifi "bssid"` | Geolocation via BSSID. |
| **Media** | `search <<exif "url"` | Metadata/GPS extraction. |
| | `search <<ocr "url"` | Text recognition in images. |
| | `search <<image "url"` | Reverse image search links. |
| **Assets** | `search <<domain "site"` | WHOIS, DNS, & Subdomains. |
| | `search <<crypto "addr"` | Crypto wallet analysis. |
| | `search <<vin "vin"` | Vehicle VIN decoder. |
| | `search <<leak "query"` | Pastebin & Leak lookup. |
| **Interface** | `back` / `next` | History navigation. |
| | `clear` | Clear terminal screen. |

## 🛡️ Privacy & Ethics
Usage for **educational purposes only**. Always ensure you have appropriate authorization before performing active scans.
