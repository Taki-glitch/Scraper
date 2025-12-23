import sqlite3

DB_NAME = "flights.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT,
            destination TEXT,
            date TEXT,
            price REAL,
            airline TEXT,
            flight_no TEXT,
            alert INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_flight(flight, alert=0):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO flights (origin, destination, date, price, airline, flight_no, alert)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (flight['origin'], flight['destination'], flight['date'], flight['price'], flight['airline'], flight['flight_no'], alert))
    conn.commit()
    conn.close()

def get_latest_prices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT origin, destination, date, price, airline, flight_no, alert
        FROM flights
        ORDER BY timestamp DESC
    ''')
    data = c.fetchall()
    conn.close()
    return data