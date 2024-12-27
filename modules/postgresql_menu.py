"""
Handles the menu option selected by the user.
Parameters:
- cur: Database cursor object.
- extract_table_column_info: Function to extract table and column information.
- parse_column_mapping: Function to parse the column mapping file.
- generate_test_data: Function to generate test data.
"""

def postgres_menu_option(cur, extract_table_column_info, parse_column_mapping, generate_test_data):

    option = input("Select an option (1: Extract table and column information, 2: Generate test data): ")
    if option == "1":
        print("Extracting table and column information...")
        extract_table_column_info(cur)
    elif option == "2":
        print("Generating test data...")
        table_definitions = parse_column_mapping('column_mapping.txt')
        generate_test_data(cur, table_definitions)
    else:
        print("Invalid option. Please select 1 or 2.")