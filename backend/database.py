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
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_flight(flight):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO flights (origin, destination, date, price, airline, flight_no)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (flight['origin'], flight['destination'], flight['date'], flight['price'], flight['airline'], flight['flight_no']))
    conn.commit()
    conn.close()

def get_latest_prices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT origin, destination, date, price, airline, flight_no, MAX(timestamp)
        FROM flights
        GROUP BY origin, destination, date
    ''')
    data = c.fetchall()
    conn.close()
    return data
