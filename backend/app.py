from flask import Flask, jsonify, request
import requests
from config import API_KEY, BASE_URL

app = Flask(__name__)

HEADERS = {
    "apikey": API_KEY
}

@app.route("/prices", methods=["GET"])
def get_prices():
    """
    Paramètres attendus :
    - origin : code aéroport départ (ex: CDG)
    - destination : code aéroport destination (ex: JFK)
    - date : date départ format YYYY-MM-DD
    """
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    date = request.args.get("date")

    if not origin or not destination or not date:
        return jsonify({"error": "origin, destination et date requis"}), 400

    # Exemple Tequila / Kiwi API
    url = f"{BASE_URL}/v2/search"
    params = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": date,
        "date_to": date,
        "curr": "EUR",
        "limit": 5
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Impossible de récupérer les données"}), 500

    data = response.json()
    # On renvoie uniquement les infos utiles
    flights = []
    for f in data.get("data", []):
        flights.append({
            "price": f.get("price"),
            "departure": f.get("route")[0].get("local_departure"),
            "arrival": f.get("route")[-1].get("local_arrival"),
            "airline": f.get("route")[0].get("airline"),
            "flight_no": f.get("route")[0].get("flight_no")
        })

    return jsonify(flights)

if __name__ == "__main__":
    app.run(debug=True)