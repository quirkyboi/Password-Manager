from database import conn, cursor
import sqlite3
import time
import bcrypt


def user_exists(username):
    try:
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        return cursor.fetchone() is not None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def register():
    username = input("Choose a username: ")

    if user_exists(username):
        print("Username already exists.")
        return

    master_password_i = input("Choose a master password: ")
    # hash the master_password before storing into database
    # use bcrypt.hashpw

    master_password = bcrypt.hashpw(
        master_password_i.encode(),
        bcrypt.gensalt()
    ).decode()

    created_at = time.strftime("%d-%m-%Y %H:%M:%S")

    try:
        cursor.execute(
            """
            INSERT INTO users(username, master_password, created_at)
            VALUES (?, ?, ?)
            """,
            (username, master_password, created_at)
        )

        conn.commit()
        print("Registration successful!")
        return login()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def login():
    print("\n---Enter your login credentials---\n")
    username = input("Username: ")

    if not user_exists(username):
        choice = input("User doesn't exist.\nDo you want to register? (yes/no): ")

        if choice.lower() in ("yes", "y"):
            return register()
        else:
            print("Goodbye!")
            return None

    password = input("Master Password: ")

    try:
        cursor.execute(
            """
            SELECT user_id, master_password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        result = cursor.fetchone()

        if result is None:
            print("User not found.")
            return None

        if bcrypt.checkpw(
            password.encode(),
            result[1].encode()
        ):
            print("Login successful!")
            return result[0]      # user_id

        print("Incorrect password.")
        return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None