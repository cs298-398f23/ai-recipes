from flask import Flask, render_template, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='static')


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

# Home route serving the HTML page
@app.route('/')
def home():
    return render_template('recipes.html')

# API route for handling search requests
@app.route('/search', methods=['GET'])
def search():
    try:
        page = int(request.args.get('page', 1))  # Get the requested page or default to 1
        items_per_page = 10  # Number of items per page

        # Calculate the offset based on the requested page
        offset = (page - 1) * items_per_page

        keyword = request.args.get('query', '')  # Retrieve the query parameter

        if keyword:
            recipes = search_recipes(keyword, offset, items_per_page)
            return jsonify({'success': True, 'data': recipes})
        else:
            return jsonify({'success': False, 'message': 'No keyword provided'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Function to search recipes in the database
# Function to search recipes in the database
def search_recipes(keyword, offset, limit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Updated query to match your database structure
        query = "SELECT * FROM recipes WHERE LOWER(title) LIKE %s OR LOWER(NER) LIKE %s OR LOWER(link) LIKE %s LIMIT %s OFFSET %s"
        cursor.execute(query, ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%', '%' + keyword.lower() + '%', limit, offset))
        recipes = cursor.fetchall()
        return recipes

    except Exception as e:
        print(f'Error: {e}')
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
