import sys
import os
import signal
import time
import requests
import asyncio
import json
import subprocess
from colorama import init, Fore, Style

# Modules
from modules import banner_art
from modules import domain_tools
from modules import network_tools
from modules import social_tools
from modules import vehicle_tools
from modules import crypto_tools
from modules import leak_tools
from modules import media_tools
from modules import ai_analysis
from modules import dark_web
from modules import phishing_tools
from modules import vpn_tools
from pyngrok import ngrok

# Optional dependencies for Ghost Mode
try:
    from fake_useragent import UserAgent
    ua = UserAgent()
except:
    ua = None

# Initialize colorama
init()

# Global State
GHOST_MODE = False
_original_request = requests.request

# Global Data Collection for AI
TARGET_DATA = {
    'usernames': {},    # {username: {site: url}}
    'emails': {},       # {email: {details}}
    'phones': {},       # {number: {details}}
    'images': [],       # [urls]
    'crypto': [],       # [addresses]
    'domains': [],      # [domains]
    'darkweb': [],      # [onion_results]
}

# --- IO / History Manager ---
import builtins

class HistoryManager:
    def __init__(self):
        self.pages = []  # List of strings (each string is a full command output)
        self.current_buffer = [] # Lines for the currently running command
        self.page_index = -1
        self.viewing_history = False
        self.original_print = builtins.print

    def hook_print(self):
        builtins.print = self._custom_print

    def _custom_print(self, *args, **kwargs):
        # Construct the string exactly as print would
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(map(str, args)) + end
        
        # 1. Print to real terminal
        self.original_print(*args, **kwargs)
        
        # 2. Save to valid buffer
        # We strip ANSI codes if we wanted clean text, but keeping them allows colored replay
        self.current_buffer.append(text)

    def start_new_page(self):
        if self.current_buffer:
             self.pages.append("".join(self.current_buffer))
        self.current_buffer = []
        self.page_index = len(self.pages) # Point to "live" (end)
        self.viewing_history = False

    def go_back(self):
        """Move towards the PRESENT (Newer items)."""
        if not self.viewing_history:
             self.original_print(f"{Fore.YELLOW}[!] Already at latest (Live).{Style.RESET_ALL}")
             return

        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self._show_page(self.page_index)
        else:
            # Return to "live"
            self.viewing_history = False
            self.page_index = len(self.pages)
            clear_screen()
            self.original_print(f"{Fore.GREEN}[*] Back to live session.{Style.RESET_ALL}")
            self.original_print(banner_art.get_header())

    def go_next(self):
        """Move towards the PAST (Older items)."""
        if not self.pages and not self.current_buffer:
             self.original_print(f"{Fore.RED}[!] No history available.{Style.RESET_ALL}")
             return

        # Transition from Live to History
        if not self.viewing_history:
             if self.current_buffer:
                  self.pages.append("".join(self.current_buffer))
                  self.current_buffer = []
             
             self.viewing_history = True
             self.page_index = len(self.pages) - 1 # Start at latest saved
             
             if self.page_index > 0:
                  self.page_index -= 1
        
        elif self.page_index > 0:
            self.page_index -= 1
        else:
            self.original_print(f"{Fore.YELLOW}[!] Limit reached (Oldest page).{Style.RESET_ALL}")
            return

        self._show_page(self.page_index)

    def _show_page(self, index):
        clear_screen()
        self.original_print(f"{Fore.CYAN}--- HISTORY VIEW ({index+1}/{len(self.pages)}) ---{Style.RESET_ALL}")
        self.original_print(self.pages[index])
        self.original_print(f"{Fore.CYAN}--- END OF PAGE (Use 'back'/'next'/'clear') ---{Style.RESET_ALL}")

HISTORY = HistoryManager()
HISTORY.hook_print()

def dump_data():
    """Saves the current session data to a JSON file for the Dashboard."""
    try:
        with open('hardlint_data.json', 'w') as f:
            json.dump(TARGET_DATA, f, indent=4)
            # print(f"{Fore.BLACK}{Style.DIM}[DEBUG] Data synced to dashboard.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to sync data: {e}{Style.RESET_ALL}")

def enable_ghost():
    global GHOST_MODE
    
    # Check if Tor is actually running on 9050 before enabling
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", 9050))
    except:
        print(f"{Fore.RED}[!] ERROR: Tor service not detected on port 9050.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please start it first: 'sudo service tor start'{Style.RESET_ALL}")
        return
    finally:
        s.close()

    GHOST_MODE = True
    
    # 1. Set Proxy (Tor Default)
    os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050'
    os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050'
    
    # 2. Monkey Patch requests to inject User-Agent
    def ghost_request(method, url, **kwargs):
        headers = kwargs.get('headers', {})
        if ua:
            headers['User-Agent'] = ua.random
        else:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Hardlint-Ghost/1.0'
        kwargs['headers'] = headers
        return _original_request(method, url, **kwargs)
    
    requests.request = ghost_request
    requests.get = lambda url, **kwargs: requests.request('GET', url, **kwargs)
    requests.post = lambda url, **kwargs: requests.request('POST', url, **kwargs)
    
    print(f"{Fore.GREEN}[👻] GHOST MODE ENABLED! (Tor Proxy + Random ID){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Make sure Tor is running (service tor start).{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] WARNING: Many social networks (TikTok, IG) block Tor IPs.{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] You may see FEWER results while in Ghost Mode.{Style.RESET_ALL}")

def disable_ghost():
    global GHOST_MODE
    GHOST_MODE = False
    
    # Unset Proxy
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    
    # Restore requests
    requests.request = _original_request
    requests.get = lambda url, **kwargs: _original_request('GET', url, **kwargs)
    requests.post = lambda url, **kwargs: _original_request('POST', url, **kwargs)
    
    print(f"{Fore.RED}[✖] GHOST MODE DISABLED. You are visible again.{Style.RESET_ALL}")

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}[!] Exiting hardlint...{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_splash():
    clear_screen()
    splash_text = banner_art.get_splash()
    for line in splash_text.split('\n'):
        print(line)
        time.sleep(0.04)
    
    print(f"{Fore.YELLOW}Press ENTER to start...{Style.RESET_ALL}")
    input()
    clear_screen()
    HISTORY.start_new_page() # Start capturing the first "real" page after splash
    print(banner_art.get_header())

def print_help():
    global GHOST_MODE
    print(f"\n{Fore.YELLOW}Available Commands (Ultimate V4 - AI Enabled){Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}[🛡️ Anonymity]{Style.RESET_ALL}")
    status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if GHOST_MODE else f"{Fore.RED}OFF{Style.RESET_ALL}"
    print(f"  {Fore.MAGENTA}ghost{Style.RESET_ALL}                          : Toggle Ghost Mode (Tor + Random UA) [{status}]")

    print(f"\n{Fore.BLUE}[Identity & Social]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}search <<username \"<name>\"{Style.RESET_ALL}   : Mass search on 100+ sites")
    print(f"  {Fore.GREEN}search <<email \"<email>\"{Style.RESET_ALL}      : Email analysis (Gravatar + Dorks)")
    print(f"  {Fore.GREEN}search <<number \"<phone>\"{Style.RESET_ALL}     : Phone reverse lookup")
    print(f"  {Fore.GREEN}search <<image \"<url>\"{Style.RESET_ALL}       : Reverse image search links")
    
    print(f"\n{Fore.BLUE}[Media Forensics]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}search <<exif \"<url>\"{Style.RESET_ALL}        : Extract Metadata (GPS, Camera)")
    print(f"  {Fore.GREEN}search <<ocr \"<url>\"{Style.RESET_ALL}         : Extract Text from Image")

    print(f"\n{Fore.BLUE}[Network & Domain]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}search <<ip \"<ip>\"{Style.RESET_ALL}           : IP Geolocation")
    print(f"  {Fore.GREEN}search <<mac \"<mac>\"{Style.RESET_ALL}         : MAC Address Vendor Lookup")
    print(f"  {Fore.GREEN}search <<scan \"<ip>\"{Style.RESET_ALL}         : Port Scanner (Active)")
    print(f"  {Fore.GREEN}search <<wifi \"<bssid>\"{Style.RESET_ALL}      : Locate WiFi Router")
    print(f"  {Fore.GREEN}search <<domain \"<site.com>\"{Style.RESET_ALL} : WHOIS, DNS, Tech Stack, Subdomains")
    
    print(f"\n{Fore.BLUE}[Assets & Misc]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}search <<crypto \"<addr>\"{Style.RESET_ALL}     : Bitcoin/Eth Wallet Check")
    print(f"  {Fore.GREEN}search <<vin \"<vin>\"{Style.RESET_ALL}         : Vehicle VIN Decoder")
    print(f"  {Fore.GREEN}search <<leak \"<query>\"{Style.RESET_ALL}      : Search for leaks/pastes")
    print(f"  {Fore.GREEN}search <<darkweb \"<query>\"{Style.RESET_ALL}   : Search Onion sites (Requires Tor)")

    print(f"\n{Fore.BLUE}[🧠 Intelligence]{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}analyze{Style.RESET_ALL}                           : Generate AI Dossier from collected data")
    print(f"  {Fore.CYAN}dashboard{Style.RESET_ALL}                         : Launch Interactive Graph UI (Web)")
    print(f"  {Fore.CYAN}show_data{Style.RESET_ALL}                         : Show currently collected data")

    print(f"\n{Fore.BLUE}[🎣 Phishing & Social Eng]{Style.RESET_ALL}")
    print(f"  {Fore.RED}list_phish{Style.RESET_ALL}                      : List phishing templates")
    print(f"  {Fore.RED}launch <template> [--public]{Style.RESET_ALL}     : Start phishing server")
    print(f"  {Fore.RED}set_phish_token <token>{Style.RESET_ALL}          : Set Ngrok token")
    print(f"  {Fore.RED}phish_logs{Style.RESET_ALL}                      : View captured phish data")

    print(f"\n{Fore.BLUE}[🛡️ VPN Control (Mullvad)]{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}vpn status{Style.RESET_ALL}                      : Check VPN connection")
    print(f"  {Fore.CYAN}vpn connect / disconnect{Style.RESET_ALL}        : Toggle VPN")
    print(f"  {Fore.CYAN}vpn set <country>{Style.RESET_ALL}               : Change server location")

    print(f"\n{Fore.BLUE}[🖥️ Interface]{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}clear{Style.RESET_ALL}                               : Clear terminal screen")
    print(f"  {Fore.WHITE}close help{Style.RESET_ALL}                          : Close help panel")
    print(f"  {Fore.WHITE}back / next{Style.RESET_ALL}                         : Older / Newer history results")
    print(f"  {Fore.GREEN}exit{Style.RESET_ALL}                                : Exit the tool")

def parse_search_command(cmd_str):
    try:
        parts = cmd_str.split("<<")
        if len(parts) < 2:
            return None, None
        rest = parts[1].strip()
        target_type = rest.split(" ")[0]
        start_quote = rest.find('"')
        end_quote = rest.rfind('"')
        if start_quote == -1 or end_quote == -1:
            return None, None
        value = rest[start_quote+1:end_quote]
        return target_type, value
    except:
        return None, None

async def run_sync(func, *args):
    """Helper to run synchronous modules in a thread."""
    return await asyncio.to_thread(func, *args)

async def main():
    show_splash()
    
    # Initialize AI Analyst
    analyst = ai_analysis.AIAnalyst()
    
    # Dashboard Process
    dashboard_process = None

    while True:
        try:
            # We no longer call start_new_page here, it will be called by commands that output data
            prompt = f"{Fore.BLUE}hardlint{Fore.RED if GHOST_MODE else Fore.BLUE} > {Style.RESET_ALL}"
            # Async input to keep the loop responsive (for future background tasks)
            try:
                command = await asyncio.to_thread(input, prompt)
                command = command.strip()
            except EOFError:
                break
            
            if not command:
                continue
            
            # --- Navigation Commands ---
            if command == "exit":
                if dashboard_process:
                    dashboard_process.terminate()
                sys.exit(0) # Force exit
            
            if command == "clear":
                clear_screen()
                # Print header but don't save it to a "new page" yet
                HISTORY.original_print(banner_art.get_header())
                continue
                
            if command == "back":
                HISTORY.go_back()
                continue
            
            if command == "next":
                HISTORY.go_next()
                continue

            if command == "!help":
                HISTORY.start_new_page()
                print_help()
                continue
            
            if command == "close help":
                clear_screen()
                print(banner_art.get_header())
                continue
            
            if command == "dashboard":
                HISTORY.start_new_page()
                print(f"{Fore.GREEN}[*] Launching Dashboard on http://localhost:5000 ...{Style.RESET_ALL}")
                try:
                    # Run app.py in background
                    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard', 'app.py')
                    dashboard_process = subprocess.Popen([sys.executable, app_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"{Fore.YELLOW}[!] Dashboard is running in background. Type 'exit' to stop everything.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Failed to start dashboard: {e}{Style.RESET_ALL}")
                continue

            if command == "show_data":
                HISTORY.start_new_page()
                print(f"\n{Fore.CYAN}[*] Collected Session Data:{Style.RESET_ALL}")
                print(json.dumps(TARGET_DATA, indent=2))
                continue

            if command == "analyze":
                HISTORY.start_new_page()
                print(f"{Fore.MAGENTA}---> Starting AI Analysis <---{Style.RESET_ALL}")
                report = await analyst.generate_dossier(TARGET_DATA)
                print(f"\n{Fore.WHITE}--------------------------------------------------")
                print(f"{Fore.GREEN}INTELLIGENCE DOSSIER{Style.RESET_ALL}")
                print(f"{Fore.WHITE}--------------------------------------------------\n")
                print(report)
                print(f"\n{Fore.WHITE}--------------------------------------------------{Style.RESET_ALL}\n")
                continue

            if command == "ghost":
                HISTORY.start_new_page()
                # Ghost mode toggling modifies global state, can stay sync for now
                if GHOST_MODE:
                    disable_ghost()
                else:
                    enable_ghost()
                continue
            
            # --- Phishing Commands ---
            if command == "list_phish":
                HISTORY.start_new_page()
                template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
                templates = [d for d in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, d))]
                print(f"\n{Fore.CYAN}[*] Available Phishing Templates:{Style.RESET_ALL}")
                for t in templates:
                    print(f"  - {t}")
                continue

            if command.startswith("set_phish_token"):
                HISTORY.start_new_page()
                parts = command.split()
                if len(parts) < 2:
                    print(f"{Fore.RED}[!] Usage: set_phish_token <token>{Style.RESET_ALL}")
                    continue
                token = parts[1]
                with open(".env", "a") as f:
                    f.write(f"\nNGROK_AUTHTOKEN={token}")
                print(f"{Fore.GREEN}[*] Ngrok token saved to .env file.{Style.RESET_ALL}")
                continue

            if command.startswith("launch"):
                HISTORY.start_new_page()
                parts = command.split()
                if len(parts) < 2:
                    print(f"{Fore.RED}[!] Usage: launch <template> [--public]{Style.RESET_ALL}")
                    continue
                
                template = parts[1]
                use_public = "--public" in parts
                
                # Load token if exists
                if use_public:
                    if os.path.exists(".env"):
                        with open(".env", "r") as f:
                            for line in f:
                                if line.strip().startswith("NGROK_AUTHTOKEN="):
                                    token = line.split("=")[1].strip()
                                    ngrok.set_auth_token(token)
                    else:
                        print(f"{Fore.RED}[!] Ngrok token not found. Use 'set_phish_token <token>' first.{Style.RESET_ALL}")
                        continue

                # Default redirects for common templates
                redirects = {
                    'google': 'https://accounts.google.com',
                    'instagram': 'https://instagram.com',
                    'facebook': 'https://facebook.com',
                    'outlook': 'https://outlook.live.com'
                }
                url = redirects.get(template, 'https://google.com')
                
                public_url = None
                if use_public:
                    try:
                        print(f"{Fore.CYAN}[*] Opening Ngrok tunnel...{Style.RESET_ALL}")
                        public_url = ngrok.connect(80).public_url
                        print(f"{Fore.GREEN}[🔥] PUBLIC LINK: {public_url}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}[!] Ngrok error: {e}{Style.RESET_ALL}")
                        continue

                print(f"{Fore.GREEN}[*] Launching phishing server: {template.upper()}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Access it locally at: http://gogle{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Listening on http://0.0.0.0:80 (Requires sudo){Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Press Ctrl+C to stop everything.{Style.RESET_ALL}")
                
                try:
                    await run_sync(phishing_tools.run_server, template, url, 80)
                except KeyboardInterrupt:
                    if public_url:
                        ngrok.disconnect(public_url)
                    print(f"\n{Fore.RED}[!] Server stopped.{Style.RESET_ALL}")
                continue

            if command == "phish_logs":
                HISTORY.start_new_page()
                logs = phishing_tools.get_logs()
                if not logs:
                    print(f"{Fore.RED}[!] No phishing logs captured yet.{Style.RESET_ALL}")
                else:
                    for entry in logs:
                        print(f"\n{Fore.CYAN}--- {entry['timestamp']} ---{Style.RESET_ALL}")
                        print(f"Template: {entry['template']}")
                        print(f"IP: {entry['ip']}")
                        for k, v in entry['data'].items():
                            print(f"{k}: {v}")
                continue
            
            # --- VPN Commands ---
            if command.startswith("vpn"):
                HISTORY.start_new_page()
                parts = command.split()
                if len(parts) < 2:
                    print(f"{Fore.RED}[!] Usage: vpn <status/connect/disconnect/set>{Style.RESET_ALL}")
                    continue
                
                sub_cmd = parts[1]
                if sub_cmd == "status":
                    print(vpn_tools.get_status())
                elif sub_cmd == "connect":
                    print(vpn_tools.connect())
                elif sub_cmd == "disconnect":
                    print(vpn_tools.disconnect())
                elif sub_cmd == "set":
                    if len(parts) < 3:
                        print(f"{Fore.RED}[!] Usage: vpn set <country_code> (es. us, se, it){Style.RESET_ALL}")
                    else:
                        print(vpn_tools.set_location(parts[2]))
                else:
                    print(f"{Fore.RED}[!] Unknown vpn command.{Style.RESET_ALL}")
                continue

            if command.startswith("search"):
                HISTORY.start_new_page()
                target_type, value = parse_search_command(command)
                if not target_type or not value:
                    print(f"{Fore.RED}[!] Invalid syntax. Use !help{Style.RESET_ALL}")
                    continue
                    
                print(f"{Fore.MAGENTA}---> Starting Module: {target_type.upper()} <---{Style.RESET_ALL}\n")
                
                # --- Routing & Data Collection ---
                
                if target_type == "username":
                    res = await social_tools.search_username(value)
                    if res:
                        TARGET_DATA['usernames'][value] = res
                        
                elif target_type == "email":
                    res = await social_tools.search_email(value)
                    if res:
                        TARGET_DATA['emails'][value] = res

                elif target_type == "number":
                    res = await social_tools.search_number(value)
                    if res:
                        TARGET_DATA['phones'][value] = res

                elif target_type == "image":
                    res = await social_tools.reverse_image_search(value)
                    TARGET_DATA['images'].append(value)
                
                elif target_type == "exif":
                    await run_sync(media_tools.get_exif_data, value)
                elif target_type == "ocr":
                    await run_sync(media_tools.ocr_image, value)

                elif target_type == "ip":
                    await run_sync(network_tools.search_ip, value)
                elif target_type == "mac":
                    await run_sync(network_tools.mac_lookup, value)
                elif target_type == "scan":
                    await run_sync(network_tools.scan_ports, value)
                elif target_type == "wifi":
                    await run_sync(network_tools.check_wifi, value)
                elif target_type == "domain":
                    await run_sync(domain_tools.get_whois, value)
                    await run_sync(domain_tools.get_dns_records, value)
                    await run_sync(domain_tools.detect_tech, value)
                    await run_sync(domain_tools.subdomain_scanner, value)
                    TARGET_DATA['domains'].append(value)
                    
                elif target_type == "crypto":
                    await run_sync(crypto_tools.check_crypto, value)
                    TARGET_DATA['crypto'].append(value)
                elif target_type == "vin":
                    await run_sync(vehicle_tools.check_vin, value)
                elif target_type == "leak":
                    await run_sync(leak_tools.check_leaks, value)

                elif target_type == "darkweb":
                    res = await dark_web.search_darkweb(value)
                    if res:
                        TARGET_DATA['darkweb'].extend(res)
                    
                else:
                    print(f"{Fore.RED}[!] Unknown search type: {target_type}{Style.RESET_ALL}")
                    
                # Autosave data for dashboard
                dump_data()
                    
                # print(f"\n{Fore.MAGENTA}---> Module Finished <---{Style.RESET_ALL}")
                # We let the loop logic handle 'Finish' by just prompting next time.
                # The output is captured in HISTORY buffer until start_new_page is called at top of loop.
            else:
                print(f"{Fore.RED}[!] Command not recognized.{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print("\n")
            continue
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
