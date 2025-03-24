import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import random
import string
import hashlib
from database import add_password, get_password  # Import functions from database.py

# Define a hashed master password (pre-hashed for security)
MASTER_PASSWORD_HASH = hashlib.sha256("cyrus".encode()).hexdigest()

# Function to verify the master password
def verify_master_password():
    entered_password = simpledialog.askstring("Authentication", "Enter Master Password:", show="*")
    if hashlib.sha256(entered_password.encode()).hexdigest() != MASTER_PASSWORD_HASH:
        messagebox.showerror("Access Denied", "Incorrect Master Password!")
        exit()

# Ask for the master password before launching the GUI
verify_master_password()

# Function to check password strength
def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    strength = "Weak"
    color = "red"
    
    if length >= 8 and (has_upper or has_lower) and has_digit:
        strength = "Medium"
        color = "orange"
    if length >= 12 and has_upper and has_lower and has_digit and has_special:
        strength = "Strong"
        color = "green"
    
    strength_label.config(text=strength, foreground=color)

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_button.config(text="🙈")
    else:
        password_entry.config(show="*")
        toggle_button.config(text="👁️")

# Function to generate a random strong password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    check_strength(password)

# Function to save password
def save():
    website = website_entry.get()
    password = password_entry.get()
    
    if website and password:
        add_password(website, password)
        messagebox.showinfo("Success", f"Password for {website} saved!")
        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        strength_label.config(text="")  # Reset strength label
    else:
        messagebox.showerror("Error", "Both fields are required!")

# Function to retrieve password
def retrieve():
    website = website_entry.get()
    
    if website:
        password = get_password(website)
        if password:
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
            messagebox.showinfo("Retrieved", f"Password for {website}: {password}")
        else:
            messagebox.showerror("Error", "No password found for this website.")
    else:
        messagebox.showerror("Error", "Please enter a website.")

# Create the main window
root = tk.Tk()
root.title("Password Manager")
root.geometry("450x350")
root.resizable(False, False)

# Labels and input fields
tk.Label(root, text="Website:").pack(pady=5)
website_entry = tk.Entry(root, width=40)
website_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack(pady=5)

# Password strength label
strength_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
strength_label.pack()

# Bind password entry to strength checker
password_entry.bind("<KeyRelease>", lambda event: check_strength(password_entry.get()))

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Save Password", command=save).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Retrieve Password", command=retrieve).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Generate Password", command=generate_password).grid(row=0, column=2, padx=5)

# Show/Hide Password Button
toggle_button = tk.Button(root, text="👁️", command=toggle_password)
toggle_button.pack()

# Run the GUI loop
root.mainloop()
