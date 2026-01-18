import sys
import os
import signal
import time
from colorama import init, Fore, Style
from modules import osint_engine
from modules import banner_art

# Initialize colorama
init()

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
        time.sleep(0.04) # Fast scroll effect
    
    print(f"{Fore.YELLOW}Press ENTER to start...{Style.RESET_ALL}")
    input()
    clear_screen()
    print(banner_art.get_header())

def print_help():
    print(f"\n{Fore.YELLOW}Available Commands:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}search <<username \"<name>\"{Style.RESET_ALL}   : Search username across social networks")
    print(f"  {Fore.GREEN}search <<email \"<email>\"{Style.RESET_ALL}      : Analyze email address (Breach & Gravatar)")
    print(f"  {Fore.GREEN}search <<number \"<phone>\"{Style.RESET_ALL}     : Analyze phone number (Reverse Lookup)")
    print(f"  {Fore.GREEN}search <<ip \"<ip_address>\"{Style.RESET_ALL}   : Geolocate IP address")
    
    print(f"  {Fore.GREEN}!help{Style.RESET_ALL}                         : Show this help message")
    print(f"  {Fore.GREEN}exit{Style.RESET_ALL}                          : Exit the tool")

def parse_search_command(cmd_str):
    try:
        # Expected format: search <<type "value"
        parts = cmd_str.split("<<")
        if len(parts) < 2:
            return None, None
            
        rest = parts[1].strip()
        # Split into type and value (handling quotes)
        target_type = rest.split(" ")[0]
        
        # Extract value between quotes
        start_quote = rest.find('"')
        end_quote = rest.rfind('"')
        
        if start_quote == -1 or end_quote == -1:
            return None, None
            
        value = rest[start_quote+1:end_quote]
        return target_type, value
    except:
        return None, None

def main():
    show_splash()
    
    while True:
        try:
            prompt = f"{Fore.BLUE}hardlint > {Style.RESET_ALL}"
            command = input(prompt).strip()
            
            if not command:
                continue
                
            if command == "exit":
                break
                
            if command == "!help":
                print_help()
                continue
                
            if command.startswith("search"):
                # Clear screen before showing results to keep "only hardlint writing" feel?
                # User said: "quando ci scrivi contiuna pero in inglese pulisce il terminale e ci sta solo la scritta hardlint"
                # This might mean they want the screen cleared *after* the command is entered and results shown cleanly?
                # Or maybe just the initial transition.
                # Let's stick to standard behavior roughly unless requested.
                # Actually, "pulisce il terminale" might mean:
                # 1. Shows Splash.
                # 2. Keypress -> Clears.
                # 3. Shows "HARDLINT" header.
                # 4. Prompt.
                # This is what show_splash() does.
                
                target_type, value = parse_search_command(command)
                if not target_type or not value:
                    print(f"{Fore.RED}[!] Invalid syntax. Use !help{Style.RESET_ALL}")
                    continue
                    
                if target_type == "username":
                    osint_engine.search_username(value)
                elif target_type == "email":
                    osint_engine.search_email(value)
                elif target_type == "number":
                    osint_engine.search_number(value)
                elif target_type == "ip":
                    osint_engine.search_ip(value)
                else:
                    print(f"{Fore.RED}[!] Unknown search type: {target_type}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Command not recognized.{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print("\n")
            continue
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print("\n")
            continue
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
