import csv
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL Database Configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
}

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to create the recipes table
def create_recipes_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500),
            NER VARCHAR(500),
            link VARCHAR(500)
        )
    """)

# Function to import data from a CSV file to the recipes table


# Function to import data from a CSV file to the recipes table
def import_data_to_mysql():
    connection = None  # Initialize connection to None
    cursor = None  # Initialize cursor to None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Create the recipes table if it doesn't exist
        create_recipes_table(cursor)

        # Read data from the CSV file and insert into the recipes table
        with open('formatted_file.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                title, ner, link = row
                print(f'Title: {title}, NER: {ner}, Link: {link}')
                cursor.execute("INSERT INTO recipes (title, NER, link) VALUES (%s, %s, %s)",
                               (title, ner, link))

        connection.commit()
        print('Data imported successfully.')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Run the data import script
if __name__ == '__main__':
    import_data_to_mysql()


