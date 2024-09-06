"""
This script generates test data for PostgreSQL databases using the Faker library. It reads the structure and content 
definitions from a column_mapping.txt file and inserts the generated data into the specified PostgreSQL tables.

Features:
- Generate fake data for multiple tables and columns.
- Define the number of rows to generate for each table.
- Use various Faker methods to generate different types of data.
- Generate sequential IDs for specified columns.

Functions:
- parse_column_mapping(file_path): Parses the column_mapping.txt file to extract table and column definitions.
- generate_test_data(cur, table_definitions): Generates and inserts test data into the database based on the parsed definitions.
"""

import re
from faker import Faker

# Initialize Faker
fake = Faker()

def parse_column_mapping(file_path):
    table_definitions = {}
    line_count = 0  # Counter for the number of lines read

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            line_count += 1  # Increment the counter for each non-empty line

            # Match for column definitions
            match = re.match(r'(\w+)\.(\w+)\.(\w+) = (.+)', line)
            if match:
                schema, table, column, faker_method = match.groups()
                if column == 'rows_to_generate':
                    table_definitions[(schema, table)]['rows_to_generate'] = int(faker_method)
                else:
                    if (schema, table) not in table_definitions:
                        table_definitions[(schema, table)] = {'columns': {}, 'rows_to_generate': 0}
                    table_definitions[(schema, table)]['columns'][column] = faker_method

    print(f"Total lines read from column_mapping.txt: {line_count}")  # Debugging output
    print(f"Parsed table definitions: {table_definitions}")  # Debugging output
    return table_definitions

def generate_test_data(cur, table_definitions):
    for (schema, table), definition in table_definitions.items():
        columns = definition['columns']
        rows_to_generate = definition['rows_to_generate']
        print(f"Generating data for table {schema}.{table} with {rows_to_generate} rows")  # Debugging output
        
        for _ in range(rows_to_generate):
            column_names = ', '.join(columns.keys())
            column_values = ', '.join(
                f"'{eval(columns[col])}'" if isinstance(eval(columns[col]), str)
                else str(eval(columns[col]))
                for col in columns.keys()
            )
            insert_query = f"INSERT INTO {schema}.{table} ({column_names}) VALUES ({column_values})"
            # print(f"Executing query: {insert_query}")  # Debugging output
            
            try:
                cur.execute(insert_query)
                cur.connection.commit()  # Commit each insert as its own transaction
                print(f"Successfully executed query for table {schema}.{table}")  # Debugging output
            except Exception as e:
                print(f"Error executing query: {insert_query}")
                print(e)
                cur.connection.rollback()  # Rollback in case of error