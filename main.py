from database import initialize_db, add_password, get_password

def main():
    initialize_db()  # Ensure database is set up
    
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_password(website, username, password)
            print("Password saved successfully!")

        elif choice == "2":
            website = input("Enter website to retrieve password: ")
            print(get_password(website))

        elif choice == "3":
            print("Exiting Password Manager.")
            break

        else:
            print("Invalid choice! Please select again.")

if __name__ == "__main__":
    main()
