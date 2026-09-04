from auth import register, login
from vault import (
    add_password,
    view_passwords,
    update_password,
    delete_password,
    search_by_website,
    search_by_category
)


def start_up_menu():
    print("\n========== PASSWORD MANAGER ==========")
    print("1. Login")
    print("2. Register")
    print("3. Exit")


def vault_menu():
    print("\n========== PASSWORD MANAGER ==========")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Update Password")
    print("4. Delete Password")
    print("5. Search by Website")
    print("6. Search by Category")
    print("7. Logout")
    print("8. Exit")


def main():

    while True:                    # Startup loop

        start_up_menu()

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        user_id = None

        match choice:

            case 1:
                user_id = login()

            case 2:
                user_id = register()

            case 3:
                return

            case _:
                print("Invalid choice!")
                continue

        # Login/Register failed
        if user_id is None:
            continue

        # ---------------- Vault ----------------

        while True:

            vault_menu()

            try:
                vchoice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            match vchoice:

                case 1:
                    add_password(user_id)

                case 2:
                    view_passwords(user_id)

                case 3:
                    update_password(user_id)

                case 4:
                    delete_password(user_id)

                case 5:
                    search_by_website(user_id)

                case 6:
                    search_by_category(user_id)

                case 7:
                    print("Logged out successfully.")
                    break          # Back to startup menu

                case 8:
                    return         # Exit program completely

                case _:
                    print("Invalid choice!")


if __name__ == "__main__":
    main()