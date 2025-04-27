from flask import Flask, render_template, request, jsonify
import requests   # ← you need this to use requests.get()
import sqlite3
from datetime import datetime



app = Flask(__name__)

# List of popular sites to monitor
popular_sites = [
    "https://www.amazon.com", "https://www.apple.com", "https://www.bing.com",
    "https://www.ebay.com", "https://www.facebook.com", "https://www.google.com",
    "https://www.instagram.com", "https://www.linkedin.com", "https://www.live.com",
    "https://www.microsoft.com", "https://www.netflix.com", "https://www.office.com",
    "https://www.pinterest.com", "https://www.reddit.com", "https://www.twitch.tv",
    "https://www.twitter.com", "https://www.wikipedia.org", "https://www.wordpress.com",
    "https://www.yahoo.com", "https://www.youtube.com"
]

DB_NAME = "logs.db"

    

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            checked_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper to log results
def log_result(url, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO logs (url, status, checked_at) VALUES (?, ?, ?)', 
            (url, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Route for main page
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        url = request.form["url"]

        if not url.startswith('http'):
            url = 'https://' + url  # Auto-add https if missing

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                result = f"{url} is UP ✅ (Status Code: 200)"
            else:
                result = f"{url} is reachable but returned status code {response.status_code} ⚠️"
        except requests.exceptions.RequestException:
            result = f"{url} is DOWN ❌ (Failed to connect)"

        log_result(url, result)

    # Load recent history
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT url, status, checked_at FROM logs ORDER BY id DESC LIMIT 10')
    logs = c.fetchall()
    conn.close()

    return render_template("index.html", result=result, logs=logs)


@app.route("/api/popular_status")
def popular_status():
    statuses = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    for site in popular_sites:
        try:
            response = requests.get(site, headers=headers, timeout=10)
            if response.status_code == 200:
                statuses[site] = "up"
            else:
                statuses[site] = "down"
        except requests.exceptions.RequestException:
            statuses[site] = "down"

    return jsonify({"statuses": statuses})



if __name__ == "__main__":
    app.run(debug=True)


