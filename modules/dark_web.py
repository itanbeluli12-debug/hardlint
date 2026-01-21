import aiohttp
import asyncio
from bs4 import BeautifulSoup
from colorama import Fore, Style
import socks

# Tor Onion Search Engine (Ahmia)
AHMIA_URL = "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/"

async def check_tor_connection():
    """Checks if Tor is running on the default port 9050."""
    try:
        # We need to construct a session that uses the SOCKS proxy
        connector = aiohttp_socks.ProxyConnector.from_url('socks5://127.0.0.1:9050')
        async with aiohttp.ClientSession(connector=connector) as session:
            # Check-tor project URL
            async with session.get('https://check.torproject.org/', timeout=10) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if "Congratulations. This browser is configured to use Tor" in text:
                        return True
    except Exception as e:
        # print(f"Tor Error: {e}")
        return False
    return False

async def search_darkweb(query):
    results = []
    print(f"{Fore.CYAN}[*] Connecting to the Dark Web (Tor Network)...{Style.RESET_ALL}")

    try:
        import aiohttp_socks
    except ImportError:
        print(f"{Fore.RED}[!] Missing dependency 'aiohttp_socks'. Install it with: pip install aiohttp_socks{Style.RESET_ALL}")
        return results

    connector = aiohttp_socks.ProxyConnector.from_url('socks5://127.0.0.1:9050')
    
    # Custom headers to look like Tor Browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'
    }

    params = {'q': query}

    print(f"{Fore.YELLOW}[!] Searching Ahmia.onion for: {query}... (This may take 10-20s){Style.RESET_ALL}")
    
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(AHMIA_URL, params=params, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Ahmia Results parsing
                    search_results = soup.select('li.result')
                    
                    for item in search_results:
                        try:
                            link = item.find('a')['href']
                            title = item.find('a').text.strip()
                            desc = item.find('p').text.strip() if item.find('p') else "No description"
                            
                            print(f"{Fore.GREEN}[+] found .onion: {title[:50]}...{Style.RESET_ALL}")
                            # print(f"    Link: {link}")
                            
                            results.append({
                                'title': title,
                                'link': link, 
                                'description': desc,
                                'source': 'Ahmia'
                            })
                        except:
                            continue
                else:
                    print(f"{Fore.RED}[!] Tor Gateway Error: {resp.status}{Style.RESET_ALL}")
                    
    except Exception as e:
        print(f"{Fore.RED}[!] Tor Connection Failed. Is Tor running? (sudo service tor start){Style.RESET_ALL}")
        # print(f"Detail: {e}")

    print(f"{Fore.BLUE}[*] Dark Web Scan Finished. Found {len(results)} hidden links.{Style.RESET_ALL}")
    return results
