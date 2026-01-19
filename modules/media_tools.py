import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pytesseract
from io import BytesIO
from colorama import Fore, Style

def get_exif_data(image_url):
    print(f"{Fore.CYAN}[*] Analyzying Image Metadata (EXIF): {image_url}{Style.RESET_ALL}")
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        exif_data = image._getexif()
        if not exif_data:
            print(f"{Fore.YELLOW}[-] No EXIF metadata found in this image.{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}[+] Metadata Found:{Style.RESET_ALL}")
        gps_info = {}
        
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "GPSInfo":
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_info[sub_tag] = value[t]
            else:
                # Filter out very long binary data
                if isinstance(value, bytes) and len(value) > 50:
                    value = "(Binary data)"
                print(f"    - {tag_name}: {value}")

        if gps_info:
            print(f"\n{Fore.GREEN}[+] GPS Coordinates Found!{Style.RESET_ALL}")
            # Simplified GPS decoding (DMS to Decimal conversion logic would go here)
            # For now, printing raw GPS data
            print(f"    - Raw GPS: {gps_info}")
            print(f"{Fore.YELLOW}[!] Note: Convert these coordinates to Decimal to view on Maps.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error processing image: {e}{Style.RESET_ALL}")

def ocr_image(image_url):
    print(f"{Fore.CYAN}[*] Performing OCR (Text Extraction): {image_url}{Style.RESET_ALL}")
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        try:
            text = pytesseract.image_to_string(image)
            if text.strip():
                print(f"{Fore.GREEN}[+] Extracted Text:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{text.strip()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[-] No text detected.{Style.RESET_ALL}")
        except pytesseract.TesseractNotFoundError:
            print(f"{Fore.RED}[!] Tesseract is not installed or not in PATH.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Limitazione Linux: Installa tesseract con 'sudo apt install tesseract-ocr'{Style.RESET_ALL}")
        except Exception as e:
             print(f"{Fore.RED}[!] OCR Error: {e}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error loading image: {e}{Style.RESET_ALL}")
