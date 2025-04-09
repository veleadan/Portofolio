#!/bin/bash

# SQLite database to store users
DB_FILE="user_management.db"

# Ensure SQLite database and users table exist
function setup_database() {
    if [[ ! -f "$DB_FILE" ]]; then
        echo "Creating database and users table..."
        sqlite3 "$DB_FILE" "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    fi
}

# Register a user and set a hashed password
function register_user() {
    read -p "Enter the username to register: " username

    # Check if username already exists in the database
    if sqlite3 "$DB_FILE" "SELECT username FROM users WHERE username='$username';" | grep -q "$username"; then
        echo "Error: User '$username' already exists in the database!"
        return
    fi

    # Set the password during registration
    while true; do
        read -s -p "Enter a password for '$username': " password
        echo
        read -s -p "Confirm the password: " password_confirm
        echo

        if [[ "$password" == "$password_confirm" ]]; then
            break
        else
            echo "Passwords do not match. Please try again."
        fi
    done

    # Generate a hashed password using Python and bcrypt
    hashed_password=$(python3 -c "import bcrypt; print(bcrypt.hashpw(bytes('$password', 'utf-8'), bcrypt.gensalt()).decode())")

    # Add user to the database
    sqlite3 "$DB_FILE" "INSERT INTO users (username, password) VALUES ('$username', '$hashed_password');" && \
    echo "User '$username' registered successfully!" || echo "Failed to register user '$username'."
}

# List all registered users (plaintext for demo purposes—exclude passwords)
function list_registered_users() {
    echo "Registered users in the database:"
    sqlite3 "$DB_FILE" "SELECT id, username, created_at FROM users;"
}

# Verify login credentials
function login_user() {
    read -p "Enter your username: " username
    read -s -p "Enter your password: " password
    echo

    # Fetch the hashed password from the database
    stored_hash=$(sqlite3 "$DB_FILE" "SELECT password FROM users WHERE username='$username';")

    if [[ -z "$stored_hash" ]]; then
        echo "Error: User '$username' does not exist."
        return
    fi

    # Verify the entered password against the stored hash using Python and bcrypt
    is_valid=$(python3 -c "
import bcrypt
valid = bcrypt.checkpw(bytes('$password', 'utf-8'), bytes('$stored_hash', 'utf-8'))
print('True' if valid else 'False')
")
    if [[ "$is_valid" == "True" ]]; then
        echo "Login successful!"
    else
        echo "Invalid password. Login failed."
    fi
}

# Main menu
function show_menu() {
    echo "**************************"
    echo "* User Management Tool *"
    echo "**************************"
    echo "1. Register a User (add to database)"
    echo "2. List Registered Users"
    echo "3. Login User"
    echo "4. Exit"
    echo "**************************"
}

# Setup database when the script starts
setup_database

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-4): " choice
    case $choice in
        1) register_user ;;
        2) list_registered_users ;;
        3) login_user ;;
        4) echo "Exiting script. Goodbye!" ; exit 0 ;;
        *) echo "Invalid choice. Please select a valid option." ;;
    esac
done