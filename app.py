from flask import Flask, render_template, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)

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
@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        keyword = data.get('query', '')
        
        if keyword:
            recipes = search_recipes(keyword)
            return jsonify({'success': True, 'data': recipes})
        else:
            return jsonify({'success': False, 'message': 'No keyword provided'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Function to search recipes in the database
def search_recipes(keyword):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM recipes WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s"
        cursor.execute(query, ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%'))

        recipes = cursor.fetchall()
        return recipes

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
