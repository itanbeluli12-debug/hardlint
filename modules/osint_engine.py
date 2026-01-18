import requests
import time
import hashlib
import phonenumbers
from phonenumbers import geocoder, carrier
from colorama import Fore, Style

def check_url(url, site_name):
    """
    Checks if a profile exists at the given URL.
    Returns True if status code is 200, False otherwise.
    Some sites might need special headers or error handling.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # Specific platform logic for false positives/negatives if needed
        # For now, relying on 200 OK.
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        # Timeout or connection error usually means site is reachable but maybe rate limited or network issue.
        # Treating as not found to avoid false positives.
        return False

def check_gravatar(email):
    """
    Checks if the email has a Gravatar image.
    Gravatar urls are based on MD5 hash of the email.
    """
    email = email.strip().lower()
    hash_email = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"https://www.gravatar.com/avatar/{hash_email}"
        return None
    except:
        return None

def generate_dorks(email):
    """
    Generates Google Dorks to manually search for the email in breaches/pastes.
    """
    domain = email.split("@")[1]
    dorks = [
        f"site:pastebin.com \"{email}\"",
        f"site:linkedin.com \"{email}\"",
        f"intext:\"{email}\" filetype:txt",
        f"intext:\"{email}\" (password | pass | pwd)",
        f"site:github.com \"{email}\""
    ]
    return dorks

def search_username(username):
    print(f"{Fore.CYAN}[*] Searching for username: {username} (Massive Search Enabled - 100+ Sites){Style.RESET_ALL}")
    
    # Dictionary of Site Name -> URL Template
    # Expanded list inspired by Sherlock/Maigret
    sites = {
        "GitHub": f"https://github.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter": f"https://twitter.com/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Patreon": f"https://www.patreon.com/{username}",
        "BitBucket": f"https://bitbucket.org/{username}/",
        "GitLab": f"https://gitlab.com/{username}",
        "About.me": f"https://about.me/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Keybase": f"https://keybase.io/{username}",
        "Kongregate": f"https://www.kongregate.com/accounts/{username}",
        "LiveJournal": f"https://{username}.livejournal.com",
        "AngelList": f"https://angel.co/{username}",
        "Last.fm": f"https://www.last.fm/user/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "CodePen": f"https://codepen.io/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Pastebin": f"https://pastebin.com/u/{username}",
        "Roblox": f"https://www.roblox.com/user.aspx?username={username}",
        "Gumroad": f"https://www.gumroad.com/{username}",
        "Wattpad": f"https://www.wattpad.com/user/{username}",
        "Canva": f"https://www.canva.com/{username}",
        "ProductHunt": f"https://www.producthunt.com/@{username}",
        "Giphy": f"https://giphy.com/{username}",
        "Telegram": f"https://t.me/{username}",
        "Wikipedia": f"https://en.wikipedia.org/wiki/User:{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
        "Codewars": f"https://www.codewars.com/users/{username}",
        "LeetCode": f"https://leetcode.com/{username}",
        "Gravatar": f"http://en.gravatar.com/{username}",
        "Disqus": f"https://disqus.com/by/{username}/",
        "9GAG": f"https://9gag.com/u/{username}",
        "BuzzFeed": f"https://www.buzzfeed.com/{username}",
        "DailyMotion": f"https://www.dailymotion.com/{username}",
        "Etsy": f"https://www.etsy.com/shop/{username}",
        "Fiverr": f"https://www.fiverr.com/{username}",
        "IFTTT": f"https://ifttt.com/p/{username}",
        "Kickstarter": f"https://www.kickstarter.com/profile/{username}",
        "ReverbNation": f"https://www.reverbnation.com/{username}",
        "Slack": f"https://{username}.slack.com",
        "TripAdvisor": f"https://www.tripadvisor.com/members/{username}",
        "Venmo": f"https://venmo.com/{username}",
        "Wix": f"https://{username}.wix.com",
        "WordPress": f"https://{username}.wordpress.com",
    }
    
    found_count = 0
    print(f"{Fore.YELLOW}[!] Scanning 50+ major platforms...{Style.RESET_ALL}")
    
    for site, url in sites.items():
        print(f"{Fore.BLUE}[~] Checking {site}...{Style.RESET_ALL}", end='\r')
        if check_url(url, site):
            print(f"{Fore.GREEN}[+] Found on {site}: {url}{Style.RESET_ALL}")
            found_count += 1
        time.sleep(0.1) # Respectful delay
            
    print(f"                                                                ", end='\r') # Clear last status line
    print(f"{Fore.BLUE}[*] Scan complete. Found {username} on {found_count} platforms.{Style.RESET_ALL}")

def search_email(email):
    print(f"{Fore.CYAN}[*] Searching for email: {email}{Style.RESET_ALL}")
    
    # Basic validation
    if "@" not in email or "." not in email:
        print(f"{Fore.RED}[!] Invalid email format.{Style.RESET_ALL}")
        return

    domain = email.split("@")[1]
    print(f"{Fore.YELLOW}[!] Analyzing domain: {domain}{Style.RESET_ALL}")
    
    # Check if domain has MX records (Simulated via simple request to domain root for now, real MX check requires dns lib)
    # We will just reach out to the domain website.
    try:
        requests.get(f"http://{domain}", timeout=3)
        print(f"{Fore.GREEN}[+] Domain {domain} is active.{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}[!] Domain {domain} does not appear to have an active web server.{Style.RESET_ALL}")
    
    # Gravatar Check
    print(f"{Fore.CYAN}[*] Checking Gravatar...{Style.RESET_ALL}")
    gravatar_url = check_gravatar(email)
    if gravatar_url:
        print(f"{Fore.GREEN}[+] Found Gravatar profile: {gravatar_url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[-] No Gravatar profile found.{Style.RESET_ALL}")

    # Google Dorks for manual breach check
    print(f"\n{Fore.CYAN}[*] Google Dorks for Manual Breach Search (Free & Safe):{Style.RESET_ALL}")
    dorks = generate_dorks(email)
    for dork in dorks:
        print(f"{Fore.BLUE}[~] Google Search: https://www.google.com/search?q={dork.replace(' ', '+').replace('\"', '%22')}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}[+] Search complete. Use the links above to check for leaks manually.{Style.RESET_ALL}")

def search_number(number):
    print(f"{Fore.CYAN}[*] Searching for phone number: {number}{Style.RESET_ALL}")
    
    try:
        # Parse the number
        parsed_number = phonenumbers.parse(number, None)  # None assumes international format (+) or try to guess
        
        if not phonenumbers.is_valid_number(parsed_number):
             print(f"{Fore.RED}[!] Number appears invalid or incomplete.{Style.RESET_ALL}")
             return

        # Get Country
        country = geocoder.description_for_number(parsed_number, "en")
        print(f"{Fore.GREEN}[+] Country: {country}{Style.RESET_ALL}")
        
        # Get Carrier
        mobile_carrier = carrier.name_for_number(parsed_number, "en")
        if mobile_carrier:
            print(f"{Fore.GREEN}[+] Carrier: {mobile_carrier}{Style.RESET_ALL}")
        else:
             print(f"{Fore.YELLOW}[!] Carrier info not available (might be landline or VoIP).{Style.RESET_ALL}")
             
        print(f"{Fore.GREEN}[+] Valid: True{Style.RESET_ALL}")

        # Reverse Lookup Links
        clean_number = str(parsed_number.country_code) + str(parsed_number.national_number)
        print(f"\n{Fore.CYAN}[*] External Reverse Lookup Links (Click to Open):{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] TrueCaller: https://www.truecaller.com/search/global/{clean_number}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] Sync.me: https://sync.me/search/{clean_number}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] Tellows: https://www.tellows.com/num/{clean_number}{Style.RESET_ALL}")
        
    except phonenumbers.NumberParseException as e:
         print(f"{Fore.RED}[!] Error parsing number: {e}. Make sure to include country code (e.g. +39...){Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}[!] Note: For real-time location or activity status, law enforcement APIs are required.{Style.RESET_ALL}")


def search_ip(ip_address):
    ip_address = ip_address.strip()
    print(f"{Fore.CYAN}[*] Geolocation for IP: {ip_address}{Style.RESET_ALL}")
    
    api_url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
    
    try:
        response = requests.get(api_url, timeout=5)
        
        # Check for HTTP errors (like 429 Rate Limit)
        if response.status_code == 429:
             print(f"{Fore.RED}[!] Error: Rate limit exceeded for IP API. Try again later.{Style.RESET_ALL}")
             return
        if response.status_code != 200:
             print(f"{Fore.RED}[!] API Error: Server returned status code {response.status_code}{Style.RESET_ALL}")
             return

        try:
            data = response.json()
        except Exception:
            print(f"{Fore.RED}[!] Error: Invalid response from API. (Are you connected to the internet?){Style.RESET_ALL}")
            return
        
        if data['status'] == 'fail':
            err_msg = data.get('message', 'Unknown error')
            if err_msg == 'reserved range':
                print(f"{Fore.YELLOW}[!] This is a Private/Local IP (Reserved Range).{Style.RESET_ALL}")
                print(f"    Private IPs (like 192.168.x.x or 10.x.x.x) are used only inside your local Wi-Fi/LAN.")
                print(f"    They do not have a geographic location on the public internet.")
            else:
                print(f"{Fore.RED}[!] Failed to locate IP: {err_msg}{Style.RESET_ALL}")
            return

        print(f"\n{Fore.GREEN}[+] Location Data:{Style.RESET_ALL}")
        print(f"    - Country: {data['country']} ({data['countryCode']})")
        print(f"    - Region: {data['regionName']} ({data['region']})")
        print(f"    - City: {data['city']}")
        print(f"    - ZIP: {data['zip']}")
        print(f"    - Timezone: {data['timezone']}")
        print(f"    - Coordinates: {data['lat']}, {data['lon']}")
        
        print(f"\n{Fore.GREEN}[+] Network Data:{Style.RESET_ALL}")
        print(f"    - ISP: {data['isp']}")
        print(f"    - Org: {data['org']}")
        print(f"    - AS: {data['as']}")
        
        print(f"\n{Fore.BLUE}[~] Google Maps: https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error connecting to IP geolocation service: {e}{Style.RESET_ALL}")

