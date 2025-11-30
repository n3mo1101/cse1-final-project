from flask import Flask
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flask_api_db'
}


def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return f"Connected to MySQL database: {DB_CONFIG['database']}"

@app.route('/')
def home():
    return f"Hello, Flask!, {get_db_connection()}"


if __name__ == "__main__":
    app.run(debug=True)
