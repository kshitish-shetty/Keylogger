from cryptography.fernet import Fernet
import json
import os

with open('config.json') as f:
    config = json.load(f)
    
    
key = config["key"]
encrypted_file_folder = config["encrypted_files_folder_path"]
decrypted_file_folder = config["decrypted_files_folder_path"]
log_file = os.path.join(decrypted_file_folder, 'error_log.txt')
decrypted_file = os.path.join(decrypted_file_folder, 'decrypted_file.txt')

# Check if the destination folder exists, create it if it doesn't
if not os.path.exists(decrypted_file_folder):
    try:
        os.makedirs(decrypted_file_folder)
    except Exception as e:
        with open("error_log.txt", 'w') as log:
            log.write(f"Error: {str(e)}\n")
            
    
if os.path.exists(encrypted_file_folder) and os.path.isdir(encrypted_file_folder):
    filenames = sorted(os.listdir(encrypted_file_folder))
    
    current_base_name = None
    first_file_in_group = True

    try:
        # Iterate over files in the folder
        for encrypted_file in filenames:
                with open(encrypted_file, 'rb') as f:
                    data = f.read()
                fernet = Fernet(key)
                decrypted = fernet.decrypt(data)
                with open(decrypted_file, 'ab') as f:
                    if not first_file_in_group and not current_base_name == None:
                        f.write("\n=== END OF FILE ===\n\n")
                    # Determine base name without (number)
                    base_name = os.path.splitext(encrypted_file)[0].split('(')[0].strip
                    if base_name != current_base_name:               
                        # Start a new group
                        current_base_name = base_name
                        f.write(f"### File: {encrypted_file} ###\n")
                        first_file_in_group = False
                    #copy decrypted content    
                    f.write(decrypted)
    except Exception as e:
        with open(log_file, 'w') as log:
            log.write(f"Error: {str(e)}\n")

else:
    with open(log_file, 'w') as log:
        log.write(f"The source folder {encrypted_file_folder} does not exist or is not a valid directory.\n")








