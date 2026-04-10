import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)
# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def mon_histogramme(): 
    return render_template("histogramme.html")

# --- LA ROUTE MANQUANTE EST ICI ---
@app.route("/atelier")
def mon_atelier():
    return render_template("atelier.html")
# ----------------------------------

@app.get("/api_atelier")
def api_atelier_data():
    # On ajoute "&hourly=relative_humidity_2m,cloud_cover" et "&past_days=1" pour avoir l'historique !
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current=relative_humidity_2m,cloud_cover&hourly=relative_humidity_2m,cloud_cover&past_days=1&forecast_days=1"
    response = requests.get(url)
    data = response.json()

    # --- 1. DONNÉES ACTUELLES (Pour les jauges) ---
    current = data.get("current", {})
    humidite_actuelle = current.get("relative_humidity_2m", 0)
    ensoleillement_actuel = 100 - current.get("cloud_cover", 0)

    # --- 2. DONNÉES HISTORIQUES (Pour la courbe) ---
    times = data.get("hourly", {}).get("time", [])
    humidites = data.get("hourly", {}).get("relative_humidity_2m", [])
    nuages = data.get("hourly", {}).get("cloud_cover", [])
    
    historique = []
    n = min(len(times), len(humidites), len(nuages))
    for i in range(n):
        historique.append({
            "datetime": times[i],
            "humidite": humidites[i],
            "ensoleillement": 100 - nuages[i]
        })

    # On renvoie les deux jeux de données
    return jsonify({
        "actuel": {
            "humidite": humidite_actuelle,
            "ensoleillement": ensoleillement_actuel
        },
        "historique": historique
    })

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
