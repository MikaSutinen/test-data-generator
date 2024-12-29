"""
postgresql_connector.py

This script provides functions to build a PostgreSQL database connection by prompting the user for connection parameters.
It includes functions to flush input and confirm the collected inputs.

Functions:
- build_postgres_connection(): Prompts the user for database connection parameters and returns a dictionary with the connection details.
- flush_input(): Clears out any leftover characters in stdin on Windows to prevent them from causing issues with the first prompt.
- confirm_inputs(): Confirms the collected inputs and returns True if accepted, False if the user wants to reset inputs, or 'BACK' if the user wants to go back to the database engine selection.

Graceful Exit:
- The script includes a try-except block to handle KeyboardInterrupt (Ctrl+C) gracefully.
- When a KeyboardInterrupt is detected, the script prints an exit message, unhooks all keyboard events using keyboard.unhook_all(), and exits the program.
"""

import maskpass
from modules.handle_exit_input import clean_exit, flush_input
from modules.logger import get_logger

logger = get_logger(__name__)

steps = [
    {"key": "hostname", "prompt": "Enter the hostname: ", "default": None},
    {"key": "port", "prompt": "Enter the port (PostgreSQL default is 5432): ", "default": "5432"},
    {"key": "dbname", "prompt": "Enter the database name: ", "default": None},
    {"key": "username", "prompt": "Enter the username: ", "default": None},
    {"key": "password", "prompt": "Enter the password: ", "default": None, "secure": True},
]

config = {}
current_step = 0

def confirm_inputs(hostname, port, dbname, username):
    try:
        while True:
            print("\nConfirm your inputs:")
            print(f"Hostname: {hostname}")
            print(f"Port: {port}")
            print(f"Database Name: {dbname}")
            print(f"Username: {username}")
            confirmation = input("Are these correct? (yes/y, no/n, back/b): ").strip().lower()

            if confirmation in ["yes", "y"]:
                return True
            elif confirmation in ["no", "n"]:
                return False
            elif confirmation in ["back", "b"]:
                return "BACK"
            else:
                print("Invalid input. Please answer 'yes/y', 'no/n', or 'back/b'.")
    finally:
        pass

def build_postgres_connection(RUNNING_OS):
    global current_step, config
    flush_input(RUNNING_OS)
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print(
        f"\n{YELLOW}[Info]{RESET} Collecting database connection parameters for PostgreSQL.\n"
        f"{YELLOW}[Info]{RESET} Provide your connection string details below.\n"
        f"{YELLOW}[Info]{RESET} Some configurations have default values, if you accept these, just press {YELLOW}Enter{RESET}.\n"
    )

    try:
        current_step = 0
        config.clear()

        while True:
            if current_step == len(steps):
                result = confirm_inputs(
                    config["hostname"],
                    config["port"],
                    config["dbname"],
                    config["username"]
                )

                if result is True:
                    return config
                elif result is False:
                    print("Restarting configuration...\n")
                    config.clear()
                    current_step = 0
                    continue
                elif result == "BACK":
                    return "BACK"

            step = steps[current_step]

            while True:
                if step.get("secure"):
                    user_input = maskpass.askpass(step["prompt"], mask="*").strip()
                else:
                    user_input = input(step["prompt"]).strip()

                if not user_input and step["default"] is not None:
                    user_input = step["default"]
                if step["key"] == "hostname" and not user_input:
                    print("Hostname cannot be empty. Please enter a valid hostname.")
                else:
                    config[step["key"]] = user_input
                    break

            current_step += 1

    except KeyboardInterrupt:
        print("\nExiting...")
        clean_exit(RUNNING_OS)
    except Exception as e:
        logger.error(f"PostgreSQL connection setup failed: {e}")
    finally:
        pass
