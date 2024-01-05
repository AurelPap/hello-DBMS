from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Path to your SQLite database file
DATABASE = './data/CarbonFootprint.db'
# DATABASE = '../local_CarbonFootprint.db'

def query_database(query):
    # try:
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(query)
    data = c.fetchall()
    # conn.close()
    return data
    # except sqlite3.Error as e:
    #     return f"An error occurred: {e}"

@app.route('/')
def index():
    # Example query
    # query = "SELECT * FROM Country WHERE Country LIKE '%Germany%'"
    
    import os

    print("Current working directory:", os.getcwd())
    directory = os.getcwd()
    
    table_name = 'World'
    query = f"SELECT * FROM {table_name}"
    query_result = query_database(query) 
    cols = query_database(f"PRAGMA table_info({table_name});")

    # if isinstance(query_result, str):
    #     # If there's an error, display the error message
    #     return query_result
    return render_template('index.html', directory = directory, query_result=query_result, cols = cols)

if __name__ == '__main__':
    app.run(debug=True)