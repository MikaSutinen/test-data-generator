"""
dbengine_selector.py

This script provides a simple text-based menu to select a database engine to work with.
It uses the 'keyboard' library to capture keyboard events and navigate through the menu options.

Functions:
- select_database_engine(): Displays a menu to select a database engine and returns the selected option.

Graceful Exit:
- The script includes handling for the 'Q' key to allow the user to quit the program gracefully.
- When the 'Q' key is pressed, the script prints an exit message and exits the program.
"""

import keyboard
import os
import sys
from modules.handle_exit_input import clean_exit
from modules.logger import get_logger

logger = get_logger(__name__)

# ANSI escape codes for colors when selecting menu items
YELLOW = '\033[93m'
RESET = '\033[0m'

def select_database_engine(UP_KEY, DOWN_KEY, ENTER_KEY, QUIT_KEY, RUNNING_OS):
    try:
        options = ["PostgreSQL", "SQL Server (coming soon)"]
        current_index = 0
    except KeyboardInterrupt:
        clean_exit(RUNNING_OS)
    except Exception as e:
        logger.error(f"Failed to initialize database engine selection menu: {e}")
        clean_exit(RUNNING_OS)

    def render_menu(RUNNING_OS):
        if RUNNING_OS == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        print("Select database engine to generate test data to (Press 'Q' to quit):")
        for i, option in enumerate(options):
            if i == current_index:
                print(f"{YELLOW}> {option}{RESET}")
            else:
                print(f"  {option}")

    try:
        while True:
            render_menu(RUNNING_OS)
            event = keyboard.read_event()
            if event.event_type == "down":
                if event.scan_code == UP_KEY:
                    current_index = (current_index - 1) % len(options)
                elif event.scan_code == DOWN_KEY:
                    current_index = (current_index + 1) % len(options)
                elif event.scan_code == ENTER_KEY:
                    return options[current_index]
                elif event.scan_code == QUIT_KEY:
                    clean_exit(RUNNING_OS)
    except KeyboardInterrupt:
        clean_exit(RUNNING_OS)
    except Exception as e:
        logger.error(f"Rending database engine selection menu failed: {e}")
        clean_exit(RUNNING_OS)