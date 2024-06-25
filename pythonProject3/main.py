from cryptography.fernet import Fernet

# Function to generate and save a key
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from the file
def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

# Ensure the key exists by writing it if it does not
try:
    open("key.key", "rb").close()
except FileNotFoundError:
    write_key()

# Load the key and create a Fernet object
key = load_key()
fer = Fernet(key)

pwd = input("What is the master password? ")

def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                if "|" in data:
                    parts = data.split("|")
                    if len(parts) == 2:
                        user = parts[0]
                        passw = fer.decrypt(parts[1].encode()).decode()
                        print("Account:", user, "Password:", passw)
                    else:
                        print("Skipping malformed line:", data)
                else:
                    print("Skipping malformed line:", data)
    except FileNotFoundError:
        print("No passwords saved yet.")
    except Exception as e:
        print(f"An error occurred: {e}")

def add():
    name = input('Account name: ')
    pwd = input("Password: ")

    encrypted_pwd = fer.encrypt(pwd.encode()).decode()

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + encrypted_pwd + "\n")

while True:
    mode = input("Would you like to add a new password or view existing ones(view, add), press q to quit? ").lower()
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue
