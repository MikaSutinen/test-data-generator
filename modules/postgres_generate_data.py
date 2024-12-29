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
from modules.logger import get_logger
from modules.handle_exit_input import clean_exit

logger = get_logger(__name__) 

# Initialize Faker
fake = Faker()

def parse_column_mapping(file_path, RUNNING_OS):
    logger.info(f"Parsing column mapping file: {file_path}")
    table_definitions = {}
    line_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                line_count += 1

                match = re.match(r'(\w+)\.(\w+)\.(\w+) = (.+)', line)
                if match:
                    schema, table, column, faker_method = match.groups()
                    if (schema, table) not in table_definitions:
                        table_definitions[(schema, table)] = {'columns': {}, 'rows_to_generate': 0}
                    if column == 'rows_to_generate':
                        table_definitions[(schema, table)]['rows_to_generate'] = int(faker_method)
                    else:
                        table_definitions[(schema, table)]['columns'][column] = faker_method

        logger.info(f"Total lines read from column_mapping.txt: {line_count}")
        return table_definitions
    except Exception as e:      
        logger.error(f"Error parsing column mapping file: {e}")
        clean_exit(RUNNING_OS)

def generate_postgres_test_data(cur, table_definitions, RUNNING_OS):
    logger.info("Starting test data generation for PostgreSQL tables.")
    try:
        for (schema, table), definition in table_definitions.items():
            columns = definition['columns']
            rows_to_generate = definition['rows_to_generate']
            logger.info(f"Generating data for table {schema}.{table} with {rows_to_generate} rows")

            # Keep track of how many rows we successfully insert
            inserted_count = 0

            for _ in range(rows_to_generate):
                column_names = ', '.join(columns.keys())
                column_values = ', '.join(
                    f"'{eval(columns[col])}'" if isinstance(eval(columns[col]), str)
                    else str(eval(columns[col]))
                    for col in columns.keys()
                )
                insert_query = f"INSERT INTO {schema}.{table} ({column_names}) VALUES ({column_values})"

                try:
                    cur.execute(insert_query)
                    cur.connection.commit()
                    inserted_count += 1
                except Exception as e:
                    logger.error(f"Error executing query: {insert_query}")
                    cur.connection.rollback()

            # Log the total number of inserted rows for this table
            logger.info(f"Inserted {inserted_count} rows into {schema}.{table}")

    except Exception as e:
        logger.error(f"Error generating test data: {e}")
        clean_exit(RUNNING_OS)
