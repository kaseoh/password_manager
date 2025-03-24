import sqlite3
from encryption import encrypt_password, decrypt_password

DB_FILE = "passwords.db"

# Create table if not exists
def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a password
def add_password(website, username, password):
    encrypted_password = encrypt_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", 
                   (website, username, encrypted_password))
    
    conn.commit()
    conn.close()

# Retrieve a password
def get_password(website):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
    result = cursor.fetchone()

    conn.close()

    if result:
        username, encrypted_password = result
        password = decrypt_password(encrypted_password)
        return f"Username: {username}\nPassword: {password}"
    else:
        return "No password found for this website."
