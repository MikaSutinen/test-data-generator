"""
    This function extracts table column information from a database using the provided cursor object.
    Parameters:
    - cur: The cursor object used to execute the SQL query.
    Returns:
    None
    Description:
    - The function prompts the user to enter the schema name (default is 'public').
    - It executes a SQL query to retrieve the table and column names from the specified schema.
    - The retrieved table and column names are written to a file named 'column_mapping.txt'.
    - The function also prints the table and column names to the console.
    - The file is formatted as follows:
        - Each table and column name is written in the format: '{schema}.{table}.{column} ='
        - If a new table is encountered, a line with '{schema}.{current_table}.rows_to_generate =' is written before it.
        - If the last table has been processed, a line with '{schema}.{current_table}.rows_to_generate =' is written.
    Note:
    - The function assumes that the database connection has already been established.
    - The function does not handle any exceptions that may occur during the execution of the SQL query or file writing.
    """

def extract_table_column_info(cur):
    schema = input("Enter the schema name (default is public): ") or "public"
    cur.execute("""
        SELECT clm.table_name, clm.column_name 
        FROM information_schema.columns AS clm
        INNER JOIN information_schema.tables tbl
        ON clm.table_name = tbl.table_name
        WHERE tbl.table_type = 'BASE TABLE'
        AND tbl.table_schema = %s
        AND tbl.table_name NOT LIKE '%%flyway%%'
        ORDER BY clm.table_name, clm.column_name
    """, (schema,))
    table_columns = cur.fetchall()
    
    with open("column_mapping.txt", "w") as file:
        current_table = None
        for table, column in table_columns:
            if current_table and current_table != table:
                file.write(f"{schema}.{current_table}.rows_to_generate =\n")
            current_table = table
            file.write(f"{schema}.{table}.{column} = \n")
            print(f"Table: {table}, Column: {column}")
        if current_table:
            file.write(f"{schema}.{current_table}.rows_to_generate =\n")