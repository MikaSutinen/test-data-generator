"""
dbengine_selector.py

This script provides a simple text-based menu to select a database engine to work with.
It uses the 'keyboard' library to capture keyboard events and navigate through the menu options.

Functions:
- select_database_engine(): Displays a menu to select a database engine and returns the selected option.

Keyboard Handling:
- The script uses scan codes to handle keyboard events for 'up', 'down', 'enter', and 'Q' keys to navigate the menu.
- UP_KEY (72): Moves the selection up in the menu.
- DOWN_KEY (80): Moves the selection down in the menu.
- ENTER_KEY (28): Selects the current menu option.
- QUIT_KEY (16): Quits the program gracefully.

Graceful Exit:
- The script includes handling for the 'Q' key to allow the user to quit the program gracefully.
- When the 'Q' key is pressed, the script prints an exit message and exits the program.
"""

import keyboard
import os
import sys
from modules.handle_exit_input import clean_exit, flush_input

def select_database_engine():
    options = ["PostgreSQL", "SQL Server (coming soon)"]
    current_index = 0

    # Scan codes for up, down, enter, and Q keys
    UP_KEY = 72
    DOWN_KEY = 80
    ENTER_KEY = 28
    QUIT_KEY = 16

    # ANSI escape codes for colors when selecting menu items
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def render_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Select database engine to generate test data to (Press 'Q' to quit):")
        for i, option in enumerate(options):
            if i == current_index:
                print(f"{YELLOW}> {option}{RESET}")
            else:
                print(f"  {option}")

    try:
        while True:
            render_menu()
            event = keyboard.read_event()
            if event.event_type == "down":
                if event.scan_code == UP_KEY:
                    current_index = (current_index - 1) % len(options)
                elif event.scan_code == DOWN_KEY:
                    current_index = (current_index + 1) % len(options)
                elif event.scan_code == ENTER_KEY:
                    return options[current_index]
                elif event.scan_code == QUIT_KEY:
                    clean_exit()
    except KeyboardInterrupt:
        clean_exit()