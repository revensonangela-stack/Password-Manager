# 🔐 Python Password Manager

A simple command-line password manager built with Python that securely stores and retrieves credentials using encryption and a master password.

## ✨ Features
- Master password protection (SHA-256 hashing)
- Encrypted password storage using Fernet (AES)
- Supports multiple accounts per service
- Password input masked with `*`
- Secure local storage

## 🛠️ Tech Stack
- Python 3.12
- cryptography (Fernet)
- hashlib

## ▶️ How to Run
```bash
pip install cryptography
python password_manager.py
