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
import platform
from modules.extract_table_information import extract_postgres_table_column_info
from modules.postgres_generate_data import generate_postgres_test_data, parse_column_mapping
from modules.dbengine_selector import select_database_engine
from modules.postgresql_connector import build_postgres_connection
from modules.postgresql_menu import postgres_menu_option
from modules.handle_exit_input import clean_exit, flush_input
from modules.logger import setup_logging, get_logger

# Set up logging for the code
setup_logging()
logger = get_logger(__name__)

# Determine the OS, needed for few things like mapping arrow keys in menu options for correct codes.
# Platforms: Windows, Linux, Darwin (MacOS)
RUNNING_OS = platform.system()

# Define scan codes based on the platform OS
if RUNNING_OS == "Windows":
    UP_KEY = 72
    DOWN_KEY = 80
    ENTER_KEY = 28
    QUIT_KEY = 16
elif RUNNING_OS == "Linux":
    UP_KEY = 103
    DOWN_KEY = 108
    ENTER_KEY = 96
    QUIT_KEY = 16
elif RUNNING_OS == "Darwin":
    UP_KEY = 126
    DOWN_KEY = 125
    ENTER_KEY = 36
    QUIT_KEY = 16

def main():
    logger.info("Starting test data generator.")

    while True:
        selected_engine = select_database_engine(UP_KEY, DOWN_KEY, ENTER_KEY, QUIT_KEY, RUNNING_OS)
        if selected_engine == "QUIT":
            print("Exiting test data generator...")
            return

        if selected_engine == "PostgreSQL":
            _ = input() # Todo: dirty hack to make it actually stop, and not overflow to next menu.
            flush_input(RUNNING_OS)
            input("Press Enter to continue to PostgreSQL connection setup, or CTRL+C to cancel...")

            db_params = build_postgres_connection(RUNNING_OS)
            if db_params == "BACK":
                continue
            elif db_params is None:
                logger.error("Failed to collect PostgreSQL connection parameters.")
                continue

            try:
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
                    generate_postgres_test_data,
                    RUNNING_OS,
                    UP_KEY,
                    DOWN_KEY,
                    ENTER_KEY,
                    QUIT_KEY
                )
                conn.commit()
                cur.close()
                conn.close()
            except KeyboardInterrupt:
                clean_exit(RUNNING_OS)
            except Exception as e:
                logger.error(f"An error occurred during PostgreSQL data generation: {e}")
                clean_exit(RUNNING_OS)

        else:
            logger.info("This database engine is not supported yet.")
            continue
        
        break

if __name__ == "__main__":
    main()
