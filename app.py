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
def mon_histogramme(): # <-- Le nom de la fonction est maintenant unique
    return render_template("histogramme.html")

@app.get("/api_atelier")
def api_atelier_data():
  
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current=relative_humidity_2m,cloud_cover"
    response = requests.get(url)
    data = response.json()

    current = data.get("current", {})
    
  
    humidite = current.get("relative_humidity_2m", 0)
    
 
    nuages = current.get("cloud_cover", 0)
    ensoleillement = 100 - nuages


    return jsonify({
        "humidite": humidite,
        "ensoleillement": ensoleillement
    })

@app.route("/atelier")
def mon_atelier():
    return render_template("atelier.html")

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
