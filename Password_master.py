#PASSWORD MANAGER MADE BY LUXUS :D 


import sqlite3
from cryptography.fernet import Fernet
import os

# generate encryption key 
def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Sarting data base
def init_db():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, platform TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# See a new password
def save_password(platform, username, password, fernet):
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    encrypted_password = fernet.encrypt(password.encode())
    c.execute("INSERT INTO passwords (platform, username, password) VALUES (?, ?, ?)",
              (platform, username, encrypted_password))
    conn.commit()
    conn.close()

# See all Passwords
def view_passwords(fernet):
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("SELECT platform, username, password FROM passwords")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        decrypted_password = fernet.decrypt(row[2]).decode()
        print(f"Plataforma: {row[0]}, Usuario: {row[1]}, Contraseña: {decrypted_password}")

# Principal Function
def main():
    generate_key()
    key = load_key()
    fernet = Fernet(key)
    init_db()

    while True:
        print("\nGestor de Contraseñas")
        print("1. Guardar una nueva contraseña")
        print("2. Ver todas las contraseñas")
        print("3. Salir")
        choice = input("Selecciona una opción: ")

        if choice == "1":
            platform = input("Plataforma: ")
            username = input("Usuario: ")
            password = input("Contraseña: ")
            save_password(platform, username, password, fernet)
            print("Contraseña guardada correctamente.")
        elif choice == "2":
            view_passwords(fernet)
        elif choice == "3":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

#Made by Luxus.