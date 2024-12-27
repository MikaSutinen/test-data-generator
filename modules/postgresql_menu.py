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

def postgres_menu_option(cur, extract_table_column_info, parse_column_mapping, generate_test_data):
    flush_input()
    options = ["Extract table and column information", "Generate test data"]
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
        print("Select an option (Press 'Q' to quit):")
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
                    selected_option = options[current_index]
                    if selected_option == "Extract table and column information":
                        _ = input()  # This is a hack to prevent the first input from being skipped
                        flush_input()
                        input("Press Enter to continue with schema extraction, or CTRL+C to cancel...")
                        extract_table_column_info(cur)
                    elif selected_option == "Generate test data":
                        _ = input()  # This is a hack to prevent the first input from being skipped
                        flush_input()
                        input("Press Enter to continue with test data generation, or CTRL+C to cancel...")
                        table_definitions = parse_column_mapping('column_mapping.txt')
                        generate_test_data(cur, table_definitions)
                    return
                elif event.scan_code == QUIT_KEY:
                    clean_exit()
    except KeyboardInterrupt:
        clean_exit()