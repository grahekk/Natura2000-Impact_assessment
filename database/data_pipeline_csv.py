import os
import psycopg2
import csv

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host='your_db_host',
            database='your_db_name',
            user='your_db_user',
            password='your_db_password'
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None

table_name = 'table_name'
schema_name = 'schema_wfs'

def load_csv_files(folder_path):
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                with open(os.path.join(folder_path, filename), 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row if it exists
                    for row in reader:

                        insert_query = f"""
                        INSERT INTO {table_name} (column1, column2, ...)
                        VALUES (%s, %s, ...);
                        """
                        cursor.execute(insert_query, tuple(row))

        conn.commit()
        print("CSV files loaded successfully into the database.")
    except (psycopg2.Error, csv.Error) as e:
        conn.rollback()
        print("Error loading CSV files:", e)
    finally:
        cursor.close()
        conn.close()
