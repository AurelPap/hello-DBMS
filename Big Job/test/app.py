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
    affichage = "affichage 1"
    return render_template('index.html', query_result=query_result, cols=cols, countries=countries, affichage=affichage)


@app.route('/update_content/<selected_country>')
def update_content(selected_country):
    conn = get_db_connection()
    result = conn.execute(f'''SELECT 
    "Source",
	CASE 
		WHEN "Source" = "Charbon" THEN (SELECT Coal FROM country WHERE Country = "{selected_country}")
		WHEN "Source" = "Gaz naturel" THEN (SELECT Gas FROM country WHERE Country = "{selected_country}")
		WHEN "Source" = "Pétrole" THEN (SELECT Oil FROM country WHERE Country = "{selected_country}")
		WHEN "Source" = "Hydraulique" THEN (SELECT Hydro FROM country WHERE Country = "{selected_country}")
		WHEN "Source" = "Renouvelable (Solaire)" THEN (SELECT Renewable FROM country WHERE Country = "{selected_country}")
		WHEN "Source" = "Nucléaire" THEN (SELECT Nuclear FROM country WHERE Country = "{selected_country}")
	END AS "% d’utilisation",
	"Médiane de gCO2/kWh",
	CASE 
		WHEN "Source" = "Charbon" THEN CAST((SELECT Coal FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Charbon")/100 AS INTEGER)
		WHEN "Source" = "Gaz naturel" THEN CAST((SELECT Gas FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Gaz naturel")/100 AS INTEGER)
		WHEN "Source" = "Pétrole" THEN CAST((SELECT Oil FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Pétrole")/100 AS INTEGER)
		WHEN "Source" = "Hydraulique" THEN CAST((SELECT Hydro FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Hydraulique")/100 AS INTEGER)
		WHEN "Source" = "Renouvelable (Solaire)" THEN CAST((SELECT Renewable FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Renouvelable (Solaire)")/100 AS INTEGER)
		WHEN "Source" = "Nucléaire" THEN CAST((SELECT Nuclear FROM country WHERE Country = "{selected_country}") * (SELECT "Médiane de gCO2/kWh" FROM emmissions_par_source WHERE "Source" = "Nucléaire")/100 AS INTEGER)
	END AS "Contribution en émission gCO2/kWh"
FROM emmissions_par_source''').fetchall()
    cols = ["Source", "% d’utilisation", "Médiane de gCO2/kWh", "Contribution en émission gCO2/kWh"]
    conn.close()
    affichage = "affichage 2"
    return render_template('content_partial.html', query_result=result, cols=cols, affichage=affichage, pays=selected_country)


if __name__ == '__main__':
    app.run(debug=True)
