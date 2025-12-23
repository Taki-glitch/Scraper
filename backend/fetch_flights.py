import requests
import random
from config import API_KEY, BASE_URL

def fetch_flights(origin, destination, date):
    """
    Récupère les vols depuis AviationStack.
    Comme le plan gratuit ne fournit pas toujours les prix, on génère un prix aléatoire.
    """
    params = {
        "access_key": API_KEY,
        "dep_iata": origin,
        "arr_iata": destination,
        "flight_date": date
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    flights = []
    for f in data.get("data", []):
        flights.append({
            "origin": origin,
            "destination": destination,
            "date": date,
            "price": random.randint(150, 600),  # prix simulé
            "airline": f.get("airline", {}).get("name", "Unknown"),
            "flight_no": f.get("flight", {}).get("number", "000")
        })
    return flights
