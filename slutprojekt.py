import os
import argparse
from cryptography.fernet import Fernet

def generate_key(key_file_name):
    key = Fernet.generate_key()
    print(f"The key is generated: {key} ")
    with open(key_file_name, "wb") as key_file:
        key_file.write(key)
    print(f"Key is saved to: {key_file_name}")
    
def encrypt_file(file, key_file_name):
    with open(key_file_name, "rb") as key_file:
        key = key_file.read()
        print(f"Using the special key from: {key_file_name}")
        
        cipher_suite = Fernet(key)
        with open(file, "rb") as file_to_encrypt:
            content = file_to_encrypt.read()
            encrypt_content = cipher_suite.encrypt(content)
            
        with open(file, "wb") as encrypted_file:
            encrypted_file.write(encrypt_content)
            print(f"The content in {file} is now encrypted and impossible to read ;)")

def decrypt_file(file, key_file_name):
    with open(key_file_name, "rb") as key_file:
        key = key_file.read()
        print(f"Using the special key from: {key_file_name}")
        
        cipher_suite = Fernet(key)
        with open(file, "rb") as file_to_decrypt:
            content = file_to_decrypt.read()
            decrypt_content = cipher_suite.decrypt(content)
            
        with open(file, "wb") as decrypted_file:
            decrypted_file.write(decrypt_content)
            print(f"The content in {file} is now decrypted and now possible to read, PEEEEW!")
            
def main():
    parser = argparse.ArgumentParser(description="Crypto program: -f [filename] [key] -m [encrypt] or [decrypt]")
    parser.add_argument("-k", "--key", help="Type a filename to create and store a new key")
    parser.add_argument("-f", "--files", nargs=2, help="Specify a file to edit and a key file to use")
    parser.add_argument("-m", "--mode", choices=["encrypt", "decrypt"], help="Choose either 'encrypt' or 'decrypt' mode")
    args = parser.parse_args()
    
    try:
        if args.key:
            if not os.path.exists(args.key):
                generate_key(args.key)
                print("The key is now generated!")
            else:
                print("The key already exists!")
        elif args.files and len(args.files) == 2 and args.mode:
            file, key = args.files
            
            if not os.path.exists(key):
                print(f"ERROR: Key file {key} does not exist. Please create the file using -k [keyfilename].")
                return
            
            if not os.path.exists(file):
                print(f"ERROR: Target file {file} does not exist. Please specify an existing file.")
                return
            
            if os.path.exists(file) and os.path.exists(key):
                if args.mode == "encrypt":
                    encrypt_file(file, key)
                    print("You made it!")
                elif args.mode == "decrypt":
                    decrypt_file(file, key)
                    print("You made it!")
                else:
                    print(f"ERROR: One or both of the files {file} {key} do not exist! :( ")
            else:
                print("Please specify a filename and the keyfile with -f [filename][keyfile] then follow it up with -m and then either [encrypt][decrypt]")
            
    except TypeError as e:
        print(f"ERROR: TypeError: {e}")
    
if __name__ == "__main__":
    main()