"""
This is a Python script that generates fake data and inserts it into a PostgreSQL database. 
The script uses the Faker library to generate fake data and the psycopg2 library to connect 
to the PostgreSQL database. The script prompts the user to enter the database connection 
parameters (hostname, port, database name, username, and password) and then connects 
to the PostgreSQL database. 

The script then generates fake data for users, posts, and comments and inserts it 
into the database. The number of users, posts, and comments to generate can be specified 
in the generate_data function. 

Finally, the script commits the transaction after inserting the data and then closes 
the database connection.
"""

import psycopg2
from faker import Faker
import pwinput
import logging
from modules.extract_table_information import extract_postgres_table_column_info
from modules.generate_data import generate_postgres_test_data, parse_column_mapping
from modules.dbengine_selector import select_database_engine
from modules.postgresql_connector import build_postgres_connection
from modules.postgresql_menu import postgres_menu_option
from modules.handle_exit_input import clean_exit, flush_input

def main():
    logging.basicConfig(level=logging.INFO)

    while True:
        selected_engine = select_database_engine()
        if selected_engine == "QUIT":
            print("Exiting test data generator...")
            return

        if selected_engine == "PostgreSQL":
            _ = input()  # This is a hack to prevent the first input from being skipped
            flush_input()
            input("Press Enter to continue to PostgreSQL connection setup, or CTRL+C to cancel...")

            db_params = build_postgres_connection()
            if db_params == "BACK":
                continue

            conn = psycopg2.connect(
                dbname=db_params["dbname"],
                user=db_params["username"],
                password=db_params["password"],
                host=db_params["hostname"],
                port=db_params["port"]
            )
            cur = conn.cursor()
            postgres_menu_option(
                cur,
                extract_postgres_table_column_info,
                parse_column_mapping,
                generate_postgres_test_data
            )
            conn.commit()
            cur.close()
            conn.close()

        else:
            print("Unsupported database engine selected.")
            # Add support for other database engines, like SQL Server here later on.
            continue

        break

if __name__ == "__main__":
    main()
