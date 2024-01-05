from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('./data/CarbonFootprint.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    query_result = conn.execute('SELECT * FROM country LIMIT 10').fetchall()
    cols = conn.execute(f"PRAGMA table_info({'country'})").fetchall()
    countries = conn.execute('SELECT Country FROM country').fetchall()
    conn.close()
    return render_template('index.html', query_result=query_result, cols=cols, countries=countries)


@app.route('/update_content/<selected_country>')
def update_content(selected_country):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM country WHERE Country = "{selected_country}"').fetchall()
    cols = conn.execute(f"PRAGMA table_info({'country'})").fetchall()
    conn.close()
    return render_template('content_partial.html', query_result=result, cols=cols)


if __name__ == '__main__':
    app.run(debug=True)
