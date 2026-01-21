import aiohttp
import asyncio
import hashlib
import concurrent.futures
import phonenumbers
from phonenumbers import geocoder, carrier
from colorama import Fore, Style

async def check_url(session, url, site_name, headers):
    try:
        async with session.get(url, headers=headers, timeout=5) as response:
            if response.status == 200:
                return (site_name, url)
    except:
        return None
    return None

async def search_username(username):
    print(f"{Fore.CYAN}[*] Searching for username: {username} (Massive Search - Async){Style.RESET_ALL}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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
    
    print(f"{Fore.YELLOW}[!] Scanning 50+ platforms...{Style.RESET_ALL}")
    found_urls = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site, url in sites.items():
            tasks.append(check_url(session, url, site, headers))
        
        for future in asyncio.as_completed(tasks):
            result = await future
            if result:
                site_name, url = result
                print(f"{Fore.GREEN}[+] Found on {site_name}: {url}{Style.RESET_ALL}")
                found_urls[site_name] = url
                
    print(f"{Fore.BLUE}[*] Scan complete. Found {username} on {len(found_urls)} platforms.{Style.RESET_ALL}")
    return found_urls

async def check_gravatar(session, email):
    email = email.strip().lower()
    hash_email = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return f"https://www.gravatar.com/avatar/{hash_email}"
    except:
        pass
    return None

def generate_dorks(email):
    domain = email.split("@")[1]
    return [
        f"site:pastebin.com \"{email}\"",
        f"site:linkedin.com \"{email}\"",
        f"intext:\"{email}\" filetype:txt",
        f"intext:\"{email}\" (password | pass | pwd)",
        f"site:github.com \"{email}\""
    ]

async def search_email(email):
    results = {'email': email, 'gravatar': None, 'dorks': []}
    print(f"{Fore.CYAN}[*] Searching for email: {email}{Style.RESET_ALL}")
    if "@" not in email or "." not in email:
        print(f"{Fore.RED}[!] Invalid email format.{Style.RESET_ALL}")
        return results

    domain = email.split("@")[1]
    print(f"{Fore.YELLOW}[!] Analyzing domain: {domain}{Style.RESET_ALL}")
    
    async with aiohttp.ClientSession() as session:
        gravatar_url = await check_gravatar(session, email)
        if gravatar_url:
            print(f"{Fore.GREEN}[+] Found Gravatar profile: {gravatar_url}{Style.RESET_ALL}")
            results['gravatar'] = gravatar_url
        else:
            print(f"{Fore.YELLOW}[-] No Gravatar profile found.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[*] Google Dorks for Manual Breach Search:{Style.RESET_ALL}")
    dorks = generate_dorks(email)
    for dork in dorks:
        encoded_dork = dork.replace(' ', '+').replace('"', '%22')
        search_url = f"https://www.google.com/search?q={encoded_dork}"
        print(f"{Fore.BLUE}[~] Search: {search_url}{Style.RESET_ALL}")
        results['dorks'].append(search_url)
    
    return results

async def search_number(number):
    results = {'number': number, 'valid': False}
    print(f"{Fore.CYAN}[*] Searching for phone number: {number}{Style.RESET_ALL}")
    try:
        parsed_number = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed_number):
             print(f"{Fore.RED}[!] Number appears invalid.{Style.RESET_ALL}")
             return results
        
        results['valid'] = True
        country = geocoder.description_for_number(parsed_number, "en")
        results['country'] = country
        print(f"{Fore.GREEN}[+] Country: {country}{Style.RESET_ALL}")
        
        mobile_carrier = carrier.name_for_number(parsed_number, "en")
        if mobile_carrier:
            results['carrier'] = mobile_carrier
            print(f"{Fore.GREEN}[+] Carrier: {mobile_carrier}{Style.RESET_ALL}")
             
        clean_number = str(parsed_number.country_code) + str(parsed_number.national_number)
        results['global_format'] = clean_number
        
        print(f"\n{Fore.CYAN}[*] Reverse Lookup Links:{Style.RESET_ALL}")
        # Add links to results? Maybe overkill for now, but good for AI context
        print(f"{Fore.BLUE}[~] TrueCaller: https://www.truecaller.com/search/global/{clean_number}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] Sync.me: https://sync.me/search/{clean_number}{Style.RESET_ALL}")
        
        return results
        
    except Exception as e:
         print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
         return results

async def reverse_image_search(image_url):
    results = {'image_url': image_url}
    print(f"{Fore.CYAN}[*] Generating Reverse Image Search Links...{Style.RESET_ALL}")
    if not image_url.startswith('http'):
        print(f"{Fore.YELLOW}[!] Note: You entered a local path or invalid URL. Showing upload pages instead.{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] Google Images (Click Camera Icon): https://images.google.com/{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[+] Image URL detected. Click these links to search directly:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[~] Google: https://lens.google.com/uploadbyurl?url={image_url}{Style.RESET_ALL}")
        # Just returning the input url for now as there's no data extraction here
    return results
