'''
This is a Python script that generates fake data and inserts it into a PostgreSQL database. 
The script uses the Faker library to generate fake data and the psycopg2 library to connect 
to the PostgreSQL database. The script prompts the user to enter the database connection 
parameters (hostname, port, database name, username, and password) and then connects to the database. 

The script then generates fake data for users, posts, and comments and inserts it into the database. 
The number of users, posts, and comments to generate can be specified in the generate_data function. 

Finally, the script commits the transaction after inserting the data and then closes the database connection.
'''

import psycopg2
from faker import Faker
import pwinput
from modules.extract_table_information import extract_table_column_info
from modules.generate_data import generate_test_data, parse_column_mapping

# Retrieve database parameters from user input
hostname = input("Enter the hostname: ")
port = input("Enter the port (default is 5432): ") or 5432
dbname = input("Enter the database name: ")
username = input("Enter the username: ")
password = pwinput.pwinput("Enter the password: ")

# Database connection parameters
def main():
    db_params = {
        'dbname': dbname,
        'user': username,
        'password': password,
        'host': hostname,
        'port': port
    }

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Prompt the user to select an option
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

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()