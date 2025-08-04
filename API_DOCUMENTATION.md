# 📚 DownDetector API Documentation

## Table of Contents
- [Overview](#overview)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Database Functions](#database-functions)
- [Frontend Components](#frontend-components)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)

## Overview

DownDetector is a Flask-based web application that monitors website uptime status. It provides real-time monitoring, historical logging, and a responsive dashboard for tracking website availability.

### Architecture
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, Bootstrap, Chart.js
- **Real-time Updates**: JavaScript with periodic API calls

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd downdetector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd my_flask_app
   python app.py
   ```

4. **Access the application**
   - Local: `http://localhost:5000`
   - The database will be automatically initialized on first run

### Required Dependencies
```txt
Flask==3.1.0
requests==2.32.3
APScheduler==3.11.0
gunicorn==23.0.0
```

---

## API Endpoints

### 1. Home Route - Website Status Checker

**Endpoint**: `/`  
**Methods**: `GET`, `POST`  
**Description**: Main page for checking website status and viewing history

#### GET Request
Returns the main dashboard with recent check history.

**Response**: HTML template with:
- Website status check form
- Recent check history (last 10 entries)
- Live status charts for popular websites

#### POST Request
Checks the status of a specified website.

**Parameters**:
- `url` (string, required): Website URL to check

**Request Example**:
```html
<form method="POST">
  <input type="text" name="url" value="https://example.com">
  <button type="submit">Check Status</button>
</form>
```

**Response Behavior**:
- Automatically adds `https://` if protocol is missing
- Returns status message with emoji indicators
- Logs result to database with timestamp

**Status Messages**:
- ✅ `{url} is UP (Status Code: 200)`
- ⚠️ `{url} is reachable but returned status code {code}`
- ❌ `{url} is DOWN (Failed to connect)`

### 2. Popular Sites Status API

**Endpoint**: `/api/popular_status`  
**Method**: `GET`  
**Description**: Returns status of predefined popular websites

**Response Format**:
```json
{
  "statuses": {
    "https://www.google.com": "up",
    "https://www.facebook.com": "down",
    "https://www.amazon.com": "up"
  }
}
```

**Monitored Sites** (20 popular websites):
- Amazon, Apple, Bing, eBay, Facebook
- Google, Instagram, LinkedIn, Live, Microsoft
- Netflix, Office, Pinterest, Reddit, Twitch
- Twitter, Wikipedia, WordPress, Yahoo, YouTube

**Usage Example**:
```javascript
fetch('/api/popular_status')
  .then(response => response.json())
  .then(data => {
    console.log('Site statuses:', data.statuses);
  });
```

---

## Database Functions

### Database Schema

**Table**: `logs`
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    checked_at TEXT NOT NULL
);
```

### Core Database Functions

#### `init_db()`
**File**: `app.py`, `db.py`  
**Description**: Initializes the SQLite database and creates the logs table if it doesn't exist.

```python
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
```

**Usage**: Automatically called when the application starts.

#### `log_result(url, status)`
**File**: `app.py`, `db.py`  
**Description**: Logs a website check result to the database.

**Parameters**:
- `url` (string): The website URL that was checked
- `status` (string): The status message/result

**Example**:
```python
log_result("https://example.com", "https://example.com is UP ✅ (Status Code: 200)")
```

#### `get_logs(limit=10)`
**File**: `db.py`  
**Description**: Retrieves recent log entries from the database.

**Parameters**:
- `limit` (int, optional): Number of records to return (default: 10)

**Returns**: List of tuples `(url, status, checked_at)`

**Example**:
```python
recent_logs = get_logs(5)
for url, status, timestamp in recent_logs:
    print(f"{timestamp}: {url} - {status}")
```

---

## Frontend Components

### 1. Status Check Form

**Location**: `templates/index.html` (lines 13-18)  
**Description**: Interactive form for checking website status

**Features**:
- Input validation (required field)
- Automatic protocol detection
- Bootstrap styling

**HTML Structure**:
```html
<form method="POST" class="mb-4">
  <div class="input-group">
    <input type="text" name="url" class="form-control" 
           placeholder="https://example.com" required>
    <button type="submit" class="btn btn-primary">Check Status</button>
  </div>
</form>
```

### 2. Live Status Chart

**Location**: `templates/index.html` (lines 63-119)  
**Description**: Real-time bar chart showing popular website statuses

**Dependencies**: Chart.js

**Features**:
- Updates every 5 seconds
- Color-coded bars (green=up, red=down)
- Responsive design
- Abbreviated site names for readability

**JavaScript Function**:
```javascript
async function updatePopularBarChart() {
  const res = await fetch('/api/popular_status');
  const data = await res.json();
  // Chart updating logic...
}
```

### 3. Current Outages Table

**Location**: `templates/index.html` (lines 121-142)  
**Description**: Table showing only websites that are currently down

**Features**:
- Auto-refresh every 5 seconds
- Shows "No current outages" when all sites are up
- Bootstrap badge styling for status

**JavaScript Function**:
```javascript
async function updateStatusTable() {
  // Fetches data and populates outages table
}
```

### 4. Check History Table

**Location**: `templates/index.html` (lines 44-58)  
**Description**: Server-rendered table showing last 10 website checks

**Features**:
- Server-side rendering with Jinja2
- Bootstrap table styling
- Shows URL, status, and timestamp

---

## Usage Examples

### Basic Website Check
```python
# Example POST request to check a website
import requests

response = requests.post('http://localhost:5000/', data={
    'url': 'https://example.com'
})
# Returns HTML page with status result
```

### API Integration
```javascript
// Fetch current status of popular sites
async function getPopularStatus() {
  try {
    const response = await fetch('/api/popular_status');
    const data = await response.json();
    
    // Check if Google is up
    const googleStatus = data.statuses['https://www.google.com'];
    console.log('Google is:', googleStatus); // 'up' or 'down'
    
    // Count total outages
    const outages = Object.values(data.statuses)
      .filter(status => status !== 'up').length;
    console.log('Total outages:', outages);
    
  } catch (error) {
    console.error('Failed to fetch status:', error);
  }
}
```

### Database Queries
```python
# Get all logs from the last hour
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('logs.db')
c = conn.cursor()

one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
c.execute(
    "SELECT * FROM logs WHERE checked_at > ? ORDER BY checked_at DESC", 
    (one_hour_ago,)
)
recent_logs = c.fetchall()
conn.close()
```

### Custom Status Monitoring
```python
# Add your own monitoring logic
def check_custom_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            status = f"{url} is UP ✅ (Status Code: 200)"
        else:
            status = f"{url} returned status code {response.status_code} ⚠️"
    except requests.exceptions.RequestException:
        status = f"{url} is DOWN ❌ (Failed to connect)"
    
    log_result(url, status)
    return status
```

---

## Error Handling

### Request Timeouts
- All HTTP requests have a 10-second timeout
- Failed requests are caught and logged as "DOWN"

### Database Errors
- Database connections are properly closed in `finally` blocks
- Automatic database initialization on startup

### Frontend Error Handling
```javascript
// Chart.js error handling
try {
  // Chart update logic
} catch (err) {
  console.error("Chart.js failed to render:", err);
}
```

### Common Error Scenarios

1. **Invalid URL Format**
   - Application automatically adds `https://` protocol
   - Empty URLs are rejected by form validation

2. **Network Connectivity Issues**
   - Caught by `requests.exceptions.RequestException`
   - Logged as DOWN status with appropriate message

3. **Database Connection Failures**
   - SQLite database is created automatically if missing
   - Connection errors are handled gracefully

### HTTP Response Codes

| Status Code | Meaning | Application Response |
|-------------|---------|---------------------|
| 200 | OK | Site is UP ✅ |
| 3xx | Redirect | Site is reachable ⚠️ |
| 4xx/5xx | Error | Site returned error code ⚠️ |
| Connection Failed | Network Error | Site is DOWN ❌ |

---

## Configuration

### Environment Variables
```bash
# Optional: Set Flask environment
export FLASK_ENV=development
export FLASK_DEBUG=True

# Optional: Custom database path
export DB_NAME=custom_logs.db
```

### Popular Sites Configuration
Edit the `popular_sites` list in `app.py` to monitor different websites:

```python
popular_sites = [
    "https://your-site1.com",
    "https://your-site2.com",
    # Add up to 20 sites for optimal chart display
]
```

### Chart Update Intervals
Modify the JavaScript intervals in `index.html`:

```javascript
// Update every 10 seconds instead of 5
setInterval(updatePopularBarChart, 10000);
setInterval(updateStatusTable, 10000);
```

---

## Performance Considerations

- **Concurrent Requests**: Popular sites are checked sequentially to avoid overwhelming the server
- **Database**: SQLite is suitable for small to medium traffic; consider PostgreSQL for high traffic
- **Caching**: Consider implementing Redis caching for frequent status checks
- **Rate Limiting**: No built-in rate limiting; add if needed for production

## Security Notes

- Uses realistic User-Agent headers to avoid blocking
- No authentication system (suitable for internal use)
- Consider adding CSRF protection for production use
- Database queries use parameterized statements to prevent SQL injection