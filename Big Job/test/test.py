import sqlite3
conn = sqlite3.connect('./data/CarbonFootprint.db')
cur = conn.cursor()

cur.execute("SELECT * FROM World")
rows = cur.fetchall()
print(rows[4])