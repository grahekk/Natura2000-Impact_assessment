import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Define the PostgreSQL connection parameters
load_dotenv()

host_name = os.getenv('host_name')
port = os.getenv('port')
database_name = os.getenv('database_name')
username = os.getenv('username')
password = os.getenv('password')
schema = 'osm'

db_params = {
    "host": host_name,
    "database": database_name,
    "user": username,
    "password": password,
}

# Function to execute a SQL query and return the results as a Pandas DataFrame
def execute_sql_query(query):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()
    return pd.DataFrame(data, columns=columns)

# Execute the first query to get matching functions
query_functions = """
SELECT 
    routine_name AS function_name,
    routines.data_type AS return_type,
    array_agg(parameters.data_type) AS argument_types
FROM 
    information_schema.routines
LEFT JOIN
    information_schema.parameters
ON 
    routines.specific_name = parameters.specific_name
WHERE 
	routine_schema LIKE 'osm'
GROUP BY
    routine_name, routines.data_type
ORDER BY
    routine_name;
"""

# Execute the query and display the result as a table
result_functions = execute_sql_query(query_functions)

query_tables = """
SELECT 
   table_name, 
   ARRAY_AGG(ROW(column_name, data_type)::text) AS columns_and_data_types
FROM 
   information_schema.columns
WHERE 
   table_schema = 'osm'
GROUP BY table_name;
"""

result_tables = execute_sql_query(query_tables)

# Convert the DataFrame into Markdown table format
functions_markdown_table = result_functions.to_markdown(index=False)
tables_markdown_table = result_tables.to_markdown(index=False)

# Load the existing Markdown document
with open('Postgis_database_documentation_README.md', 'r') as md_file:
    markdown_content = md_file.read()

# Identify the location of the old table (e.g., using a marker)
markers = {
    'functions': ('<!-- START FUNCTIONS TABLE -->', '<!-- END FUNCTIONS TABLE -->'),
    'tables': ('<!-- START TABLES TABLE -->', '<!-- END TABLES TABLE -->')
}

updated_markdown_content = markdown_content


# Replace the old table with the updated table
for table_type, (start_marker, end_marker) in markers.items():
    start_index = updated_markdown_content.find(start_marker)
    end_index = updated_markdown_content.find(end_marker)

    if start_index != -1 and end_index != -1:
        updated_markdown_content = (
            updated_markdown_content[:start_index + len(start_marker)] +
            '\n' +  # Add a newline for separation
            (functions_markdown_table if table_type == 'functions' else tables_markdown_table) +
            '\n' +  # Add a newline for separation
            updated_markdown_content[end_index:]
        )

# Write the updated Markdown content back to the file
with open('Postgis_database_documentation_README.md', 'w') as md_file:
    md_file.write(updated_markdown_content)
