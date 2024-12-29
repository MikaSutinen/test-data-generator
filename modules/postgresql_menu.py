"""
Handles the menu option selected by the user.
Parameters:
- cur: Database cursor object.
- extract_table_column_info: Function to extract table and column information.
- parse_column_mapping: Function to parse the column mapping file.
- generate_test_data: Function to generate test data.
"""

import keyboard
import os
from modules.handle_exit_input import clean_exit, flush_input

def postgres_menu_option(cur, extract_table_column_info, parse_column_mapping, generate_postgres_test_data, RUNNING_OS, UP_KEY, DOWN_KEY, ENTER_KEY, QUIT_KEY):
    flush_input(RUNNING_OS)
    options = ["Extract table and column information", "Generate test data"]
    current_index = 0

    # ANSI escape codes for colors when selecting menu items
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def render_menu(RUNNING_OS):
        if RUNNING_OS == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        print("Select an option (Press 'Q' to quit):")
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
                    selected_option = options[current_index]
                    if selected_option == "Extract table and column information":
                        flush_input(RUNNING_OS)
                        input("Press Enter to continue with schema extraction, or CTRL+C to cancel...")
                        extract_table_column_info(cur, RUNNING_OS)
                    elif selected_option == "Generate test data":
                        flush_input(RUNNING_OS)
                        input("Press Enter to continue with test data generation, or CTRL+C to cancel...")
                        table_definitions = parse_column_mapping('column_mapping.txt', RUNNING_OS)
                        generate_postgres_test_data(cur, table_definitions, RUNNING_OS)
                    return
                elif event.scan_code == QUIT_KEY:
                    clean_exit(RUNNING_OS)
    except KeyboardInterrupt:
        clean_exit(RUNNING_OS)