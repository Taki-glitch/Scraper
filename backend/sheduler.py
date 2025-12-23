import requests
from database import save_flight
from config import API_KEY, BASE_URL, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, PRICE_THRESHOLD
import smtplib
from email.message import EmailMessage

# Liste de vols à surveiller
TRACKED_FLIGHTS = [
    {"origin": "CDG", "destination": "JFK", "date": "2026-02-15"},
    {"origin": "ORY", "destination": "LAX", "date": "2026-02-20"},
]

HEADERS = {"apikey": API_KEY}

def fetch_prices(origin, destination, date):
    url = f"{BASE_URL}/v2/search"
    params = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": date,
        "date_to": date,
        "curr": "EUR",
        "limit": 3
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    flights = []
    for f in data.get("data", []):
        flights.append({
            "origin": origin,
            "destination": destination,
            "date": date,
            "price": f.get("price"),
            "airline": f.get("route")[0].get("airline"),
            "flight_no": f.get("route")[0].get("flight_no")
        })
    return flights

def send_email_alert(flight):
    msg = EmailMessage()
    msg['Subject'] = f"Prix bas détecté : {flight['origin']} -> {flight['destination']}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"Prix: {flight['price']}€\nDate: {flight['date']}\nCompagnie: {flight['airline']} {flight['flight_no']}")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Alerte envoyée pour {flight['origin']} -> {flight['destination']} : {flight['price']}€")

def check_flights():
    for f in TRACKED_FLIGHTS:
        flights = fetch_prices(f['origin'], f['destination'], f['date'])
        for flight in flights:
            save_flight(flight)
            if flight['price'] <= PRICE_THRESHOLD:
                send_email_alert(flight)

if __name__ == "__main__":
    check_flights()
