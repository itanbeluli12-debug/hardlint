import subprocess
from colorama import Fore, Style

def run_mullvad_cmd(cmd_list):
    """Helper to run mullvad CLI commands."""
    try:
        result = subprocess.run(['mullvad'] + cmd_list, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def get_status():
    status = run_mullvad_cmd(['status'])
    if "Connected" in status:
        return f"{Fore.GREEN}[🔒] {status}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}[🔓] {status}{Style.RESET_ALL}"

def connect():
    print(f"{Fore.YELLOW}[*] Connecting to Mullvad VPN...{Style.RESET_ALL}")
    run_mullvad_cmd(['connect'])
    return get_status()

def disconnect():
    print(f"{Fore.YELLOW}[*] Disconnecting from Mullvad VPN...{Style.RESET_ALL}")
    run_mullvad_cmd(['disconnect'])
    return get_status()

def set_location(country_code):
    print(f"{Fore.YELLOW}[*] Setting location to: {country_code.upper()}{Style.RESET_ALL}")
    res = run_mullvad_cmd(['relay', 'set', 'location', country_code])
    if "Error" in res:
        return f"{Fore.RED}[!] Failed to set location: {res}{Style.RESET_ALL}"
    return f"{Fore.GREEN}[*] Location set. Reconnecting...{Style.RESET_ALL}\n{connect()}"
