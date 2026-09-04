import sqlite3
import time
import re
from database import conn, cursor
from password_utils import generate_password
from crypto_utils import encrypt_password, decrypt_password

def add_password(user_id):
    website = input("Website: ")
    username = input("Username / Email: ")
    user_opinion = input("Generate a secure password? (y/n): ")
    if user_opinion.upper() == 'Y':
        password = generate_password()
        print(f"Your Password is: {password}")
    else:
        password = input("Password: ")

    encrypted_password = encrypt_password(password).decode()
    category = input("Category (optional): ")
    notes = input("Notes (optional): ")

    timestamp = time.strftime("%d-%m-%Y %H:%M:%S")

    try:
        cursor.execute(
            """
            INSERT INTO passwords(
                user_id,
                website,
                username,
                password,
                category,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                website,
                username,
                encrypted_password,
                category,
                notes,
                timestamp,
                timestamp
            )
        )

        conn.commit()
        print("Password added successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def view_passwords(user_id):

    try:
        cursor.execute(
            """
            SELECT
                password_id,
                website,
                username,
                password,
                category,
                notes,
                created_at
            FROM passwords
            WHERE user_id = ?
            """,
            (user_id,)
        )

        values = cursor.fetchall()

        if not values:
            print("No passwords saved.")
            return

        for value in values:

            print("----------------------------------------")
            print(f"Password ID : {value[0]}")
            print(f"Website     : {value[1]}")
            print(f"Username    : {value[2]}")
            print(f"Password    : {decrypt_password(value[3].encode())}")
            print(f"Category    : {value[4]}")
            print(f"Notes       : {value[5]}")
            print(f"Created At  : {value[6]}")
            print("----------------------------------------")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def delete_password(user_id):

    view_passwords(user_id)

    try:
        choice = int(input("Enter Password ID to delete: "))

        cursor.execute(
            """
            DELETE FROM passwords
            WHERE password_id = ?
            AND user_id = ?
            """,
            (choice, user_id)
        )

        if cursor.rowcount == 0:
            print("Password not found.")
        else:
            conn.commit()
            print("Password deleted successfully!")

    except ValueError:
        print("Please enter a valid ID.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def update_password(user_id):

    view_passwords(user_id)

    try:
        password_id = int(input("\nEnter Password ID to update: "))

        header = "------ Update Password ------"
        menu = {
            1: "Website",
            2: "Username",
            3: "Password",
            4: "Category",
            5: "Notes",
            6: "Cancel"
        }

        print(f"\n{header}")

        for key, item in menu.items():
            print(f"{key}. {item}")

        choice = int(input("\nChoice: "))

        updated_at = time.strftime("%d-%m-%Y %H:%M:%S")

        match choice:

            case 1:
                new_website = input("Enter new website: ")

                cursor.execute(
                    """
                    UPDATE passwords
                    SET website = ?, updated_at = ?
                    WHERE password_id = ? AND user_id = ?
                    """,
                    (new_website, updated_at, password_id, user_id)
                )

            case 2:
                new_username = input("Enter new username/email: ")

                cursor.execute(
                    """
                    UPDATE passwords
                    SET username = ?, updated_at = ?
                    WHERE password_id = ? AND user_id = ?
                    """,
                    (new_username, updated_at, password_id, user_id)
                )

            case 3:
                user_opinion = input("Generate a secure password? (y/n): ")
                if user_opinion.upper() == 'Y':
                    new_password = generate_password()
                    print(f"Your Password is: {new_password}")
                else:
                    new_password = input("Password: ")
                cursor.execute(
                    """
                    UPDATE passwords
                    SET password = ?, updated_at = ?
                    WHERE password_id = ? AND user_id = ?
                    """,
                    (encrypt_password(new_password).decode(), updated_at, password_id, user_id)
                )

            case 4:
                new_category = input("Enter new category: ")

                cursor.execute(
                    """
                    UPDATE passwords
                    SET category = ?, updated_at = ?
                    WHERE password_id = ? AND user_id = ?
                    """,
                    (new_category, updated_at, password_id, user_id)
                )

            case 5:
                new_notes = input("Enter new notes: ")

                cursor.execute(
                    """
                    UPDATE passwords
                    SET notes = ?, updated_at = ?
                    WHERE password_id = ? AND user_id = ?
                    """,
                    (new_notes, updated_at, password_id, user_id)
                )

            case 6:
                return

            case _:
                print("Invalid choice.")
                return

        if cursor.rowcount == 0:
            print("Password not found.")
        else:
            conn.commit()
            print("Password updated successfully!")

    except ValueError:
        print("Please enter a valid number.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def search_by_website(user_id):
    web = input("Enter website: ")

    cursor.execute("SELECT password_id, website, username, password, category, notes FROM passwords WHERE user_id = ? AND website LIKE ?", (user_id, f"%{web}%"))
    websites = cursor.fetchall()

    if not websites:
        print("No such passwords exist!")
        return

    for website in websites:
        print("----------------------------------")
        print(f"Password ID : {website[0]}")
        print(f"Website : {website[1]}")
        print(f"Username : {website[2]}")
        print(f"Password : {decrypt_password(website[3]).encode()}")
        print(f"Category : {website[4]}")
        print(f"Notes : {website[5]}")
        print("----------------------------------\n")

def search_by_category(user_id):
    
    cursor.execute("SELECT DISTINCT category FROM passwords WHERE user_id = ?", (user_id,))
    categories = cursor.fetchall()

    if not categories:
        print("You dont have any password!")
        return

    existing_categories = [category[0] for category in categories]

    print("\nAvailable Categories:")
    for category in existing_categories:
        print(f"- {category}")

    user_chosen_category = input("Enter category: ")
    if not user_chosen_category in existing_categories:
        print("No such category exist.")
        return
    
    cursor.execute("SELECT password_id, website, username, password, category, notes FROM passwords WHERE user_id = ? AND category = ?", (user_id, user_chosen_category))

    websites = cursor.fetchall()

    if not websites:
        print("No such passwords exist!")
        return

    for website in websites:
        print("----------------------------------")
        print(f"Password ID : {website[0]}")
        print(f"Website : {website[1]}")
        print(f"Username : {website[2]}")
        print(f"Password : {decrypt_password(website[3].encode())}")
        print(f"Category : {website[4]}")
        print(f"Notes : {website[5]}")
        print("----------------------------------\n")

