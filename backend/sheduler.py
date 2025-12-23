from fetch_flights import fetch_flights
from database import save_flight
from config import PRICE_THRESHOLD

TRACKED_FLIGHTS = [
    {"origin": "CDG", "destination": "JFK", "date": "2026-02-15"},
    {"origin": "ORY", "destination": "LAX", "date": "2026-02-20"},
]

def check_flights():
    for f in TRACKED_FLIGHTS:
        flights = fetch_flights(f['origin'], f['destination'], f['date'])
        for flight in flights:
            alert_flag = 1 if flight['price'] <= PRICE_THRESHOLD else 0
            save_flight(flight, alert=alert_flag)
            if alert_flag:
                print(f"⚠️ Alerte : {flight['origin']} -> {flight['destination']} : {flight['price']}€")

if __name__ == "__main__":
    check_flights()