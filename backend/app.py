from flask import Flask, jsonify
from database import get_latest_prices, init_db

app = Flask(__name__)
init_db()

@app.route("/prices")
def prices():
    data = get_latest_prices()
    result = []
    for row in data:
        result.append({
            "origin": row[0],
            "destination": row[1],
            "date": row[2],
            "price": row[3],
            "airline": row[4],
            "flight_no": row[5],
            "alert": bool(row[6])
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)