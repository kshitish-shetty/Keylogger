from cryptography.fernet import Fernet
import json



try:
    with open('config.json', 'r+') as f:  # Open file in read and write mode ('r+')

        config = json.load(f)
        backup = f.read()

        key = Fernet.generate_key().decode() # Generate key then decode bytes into String
        config['key'] = key

        f.seek(0)  # Move cursor to the beginning of the file
        json.dump(config, f, indent=2)  # Write updated config dictionary back to file

        f.truncate()  # If new content is shorter, truncate the remaining part
    
    print("Key Generated Successfully!!!")
    print("Updated .json File")
except Exception as e:
    with open('config.json', 'r+') as f:
        f.write(backup)
        
        f.truncate()
        
    print("ERROR:", e)
