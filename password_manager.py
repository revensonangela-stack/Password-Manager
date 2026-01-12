import hashlib
import os
import msvcrt
from cryptography.fernet import Fernet


# -------------------------------
# Password masking with *
# (Windows only)
# -------------------------------
def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""

    while True:
        char = msvcrt.getch()

        # Enter key
        if char == b"\r":
            print()
            break

        # Backspace
        elif char == b"\x08":
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)

        # Ignore special keys
        elif char in {b"\x00", b"\xe0"}:
            msvcrt.getch()
            continue

        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)

    return password


# -------------------------------
# Master password hashing
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------
# Master password setup
# -------------------------------
def set_master_password():
    password = input_password("Create master password: ")
    confirm = input_password("Confirm master password: ")

    if password != confirm:
        print("Passwords do not match!")
        return set_master_password()

    with open("master.hash", "w") as file:
        file.write(hash_password(password))

    print("Master password set successfully!")


# -------------------------------
# Master password verification
# -------------------------------
def verify_master_password():
    password = input_password("Enter master password: ")

    with open("master.hash", "r") as file:
        stored_hash = file.read()

    if hash_password(password) == stored_hash:
        return True
    else:
        print("Incorrect master password!")
        return False


# -------------------------------
# Encryption key handling
# -------------------------------
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("secret.key", "rb").read()


# -------------------------------
# Store encrypted password
# -------------------------------
def add_password(service, username, password, fernet):
    encrypted_password = fernet.encrypt(password.encode())

    with open("passwords.txt", "a") as file:
        file.write(f"{service}|{username}|{encrypted_password.decode()}\n")

    print("Password stored securely!")


# -------------------------------
# Retrieve and decrypt password
# -------------------------------
def get_password(service, username, fernet):
    with open("passwords.txt", "r") as file:
        for line in file:
            stored_service, stored_username, encrypted_password = line.strip().split("|")

            if stored_service == service and stored_username == username:
                decrypted_password = fernet.decrypt(
                    encrypted_password.encode()
                ).decode()

                print(f"\nService: {service}")
                print(f"Username: {username}")
                print(f"Password: {decrypted_password}")
                return

    print("No matching credentials found.")


# -------------------------------
# Main application flow
# -------------------------------
def main():
    # First-time setup
    if not os.path.exists("master.hash"):
        set_master_password()

    # Verify master password
    if not verify_master_password():
        return

    # Generate encryption key if missing
    if not os.path.exists("secret.key"):
        generate_key()

    key = load_key()
    fernet = Fernet(key)

    while True:
        print("\n1. Add Password")
        print("2. Get Password")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Service name: ")
            username = input("Username: ")
            password = input_password("Password: ")
            add_password(service, username, password, fernet)

        elif choice == "2":
            service = input("Service name: ")
            username = input("Username: ")
            get_password(service, username, fernet)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


# -------------------------------
# Run program
# -------------------------------
main()
