
Team Members:
-Brian Demyan
-Deni Velasquez
-Derek Allmon

---

# AI Recipes Search

This project provides a simple web interface to search for recipes stored in a MySQL database. Users can enter keywords, and the application will retrieve and display matching recipes from the database.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Database Configuration](#database-configuration)
  - [Install Dependencies](#install-dependencies)
- [Importing Data](#importing-data)
- [Running the Application](#running-the-application)
- [Usage](#usage)

## Prerequisites

Before you begin, make sure you have the following installed:

- [Python](https://www.python.org/)
- [MySQL Server](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/)

## Setup

### Database Configuration

1. Create a MySQL database and note down the database details (host, user, password, and name).

2. Create a `.env` file in the project root and add your MySQL database details:

   ```env
   DB_HOST=your_database_host
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_DATABASE=your_database_name
   ```

### Install Dependencies

1. Open a terminal and navigate to the project directory.

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

## Importing Data

1. Prepare your recipe data in CSV format. Ensure that the CSV file has columns: `title`, `NER`, and `link`.

2. Save the CSV file as `formatted_file.csv` in the project directory. (Dataset is already provided)

3. Run the data import script:

   ```
   pip install --upgrade mysql-connector-python
   ```
   python import_data.py
   ```

## Running the Application

1. Start the Flask application:

   ```
   python app.py
   ```

2. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the application.

## Usage

- Enter keywords in the search bar to find recipes containing the specified keywords.
- The results will be displayed, including the recipe title, ingredients (NER), and a link to the recipe details.


# AI Recipes API Documentation

This API provides endpoints to search for recipes stored in a MySQL database. Users can send search queries to retrieve matching recipes.

## Search Recipes

### Endpoint

`POST /search`

### Request

- **URL:** http://127.0.0.1:5000/search
- **Method:** POST
- **Headers:**
  - Content-Type: application/json
- **Body:**
  - JSON object with the following properties:
    - `query`: (string) The search query.

**Example:**

```json
{
  "query": "chicken"
}
```

### Response

- **Success Response:**
  - **Status Code:** 200 OK
  - **Body:**
    - JSON object with the following properties:
      - `success`: (boolean) Indicates if the request was successful.
      - `data`: (array) List of recipes matching the search query.
        - Each recipe object contains:
          - `title`: (string) Recipe title.
          - `NER`: (string) Ingredients or Named Entity Recognition.
          - `link`: (string) Link to the recipe details.

**Example:**

```json
{
  "success": true,
  "data": [
    {
      "title": "Chicken Parmesan",
      "NER": "chicken, tomato sauce, cheese, pasta",
      "link": "www.cookbooks.com/recipe/chicken-parmesan"
    },
    {
      "title": "Grilled Lemon Herb Chicken",
      "NER": "chicken, lemon, herbs",
      "link": "www.cookbooks.com/recipe/grilled-lemon-herb-chicken"
    }
  ]
}
```

- **Error Response:**
  - **Status Code:** 200 OK
  - **Body:**
    - JSON object with the following properties:
      - `success`: (boolean) Indicates if the request was successful.
      - `message`: (string) Error message.

**Example:**

```json
{
  "success": false,
  "message": "No recipes found"
}
```

---