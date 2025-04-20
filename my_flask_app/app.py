from flask import Flask, render_template, request
import requests
from db import init_db, log_result, get_logs  # ✅ Make sure db.py is in the same folder

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        url = request.form["url"]

        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code

            if status_code == 200:
                result = f"{url} is UP ✅ (Status Code: 200)"
            else:
                result = f"{url} is reachable but returned status code {status_code} ⚠️"

        except requests.exceptions.Timeout:
            result = f"{url} is DOWN ❌ (Connection timed out)"
        except requests.exceptions.RequestException:
            result = f"{url} is DOWN ❌ (Failed to connect)"

        log_result(url, result)  # ✅ Log the result to SQLite

    logs = get_logs()  # ✅ Fetch logs after logging
    return render_template("index.html", result=result, logs=logs)  # ✅ Pass logs to template

if __name__ == "__main__":
    app.run(debug=True)

