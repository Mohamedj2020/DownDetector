# DownDetector

DownDetector is a full-stack web application that monitors the uptime status of websites, logs results in a SQLite database, and displays real-time updates on a responsive dashboard.  
Built using **Flask**, **Bootstrap**, **SQLite**, and **JavaScript**, the app is expanding to include advanced features like scheduled background checks, email and SMS downtime alerts, user authentication, and historical data visualization.

---

## 🚀 Features

- ✅ Check if a website is up or down in real-time
- ✅ Log results to a SQLite database with timestamps
- ✅ Display recent uptime history in a responsive Bootstrap table
- 🔜 Schedule automatic checks with APScheduler
- 🔜 Send email alerts when a site goes down (using `smtplib`)
- 🔜 Send SMS alerts using Twilio API
- 🔜 Authenticate users with Flask-Login
- 🔜 Visualize uptime data with Chart.js graphs
- 🔜 Allow users to manage their own list of monitored URLs
- 🔜 Create downloadable historical uptime reports (CSV/PDF)

---

## 🛠️ Tech Stack

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite
- **Scheduling**: APScheduler
- **Notifications**: smtplib (email), Twilio API (SMS)
- **Authentication**: Flask-Login
- **Data Visualization**: Chart.js
- **Environment Management**: python-dotenv
- **Testing**: pytest or unittest
- **Version Control**: Git + GitHub

---

## ⚙️ How to Run Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/DownDetector.git
   cd DownDetector
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

5. **Visit:**
   ```
   http://127.0.0.1:5000
   ```

## 📈 Upcoming Enhancements

- Scheduled background uptime checks
- Email/SMS notifications on downtime
- Public and private user dashboards
- Dark mode toggle for accessibility
- Downloadable uptime history reports

 
