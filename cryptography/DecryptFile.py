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
    filenames = sorted(os.listdir(encrypted_file_folder), reverse=True)
    
    current_base_name = None
    first_file = True

    try:
        with open(decrypted_file, 'ab') as df:
            df.write("\n!!!!!!!!!!!!!!!!!!!! START OF DECRYPTED DATA !!!!!!!!!!!!!!!!!!!!\n\n\n".encode())
            
            # Iterate over files in the folder
            for encrypted_file in filenames:         
                source_file_path = os.path.join(encrypted_file_folder, encrypted_file) 
                with open(source_file_path, 'rb') as ef:
                    data = ef.read()
                fernet = Fernet(key)
                decrypted = fernet.decrypt(data)

                # Determine base name without (number)
                base_name = os.path.splitext(encrypted_file)[0].split('(')[0].strip()

                if base_name != current_base_name:    

                    # Seperate the last entry of previous group
                    if not first_file and not current_base_name == None:
                        df.write("\n=== END OF FILE ===\n\n".encode())             
                    # Start a new group
                    current_base_name = base_name
                    df.write(f"### File: {encrypted_file} ###\n\n".encode())
                    first_file = False
    
                # Decrypted content    
                df.write(decrypted)
                df.write("\n".encode())
                
        # Denote end of decrypted file
            df.write("\n\n!!!!!!!!!!!!!!!!!!!! END OF DECRYPTED DATA !!!!!!!!!!!!!!!!!!!!\n\n".encode())
    
    except Exception as e:
        with open(log_file, 'w') as log:
            log.write(f"Error: {str(e)}\n")

else:
    with open(log_file, 'w') as log:
        log.write(f"The source folder {encrypted_file_folder} does not exist or is not a valid directory.\n")








