# 🔧 Function Reference Guide

## Table of Contents
- [Backend Functions](#backend-functions)
- [Database Functions](#database-functions)
- [Frontend Functions](#frontend-functions)
- [Utility Functions](#utility-functions)
- [Configuration](#configuration)

---

## Backend Functions

### Flask Route Handlers

#### `home()`
**File**: `my_flask_app/app.py` (lines 52-84)  
**Route**: `/` (GET, POST)  
**Description**: Main route handler for the website status checker

**Parameters**: None (uses Flask request object)  
**Returns**: Rendered HTML template with context data

**Request Handling**:
- **GET**: Returns dashboard with recent logs
- **POST**: Processes URL check form submission

**Form Data**:
- `url` (string): Website URL to check (from `request.form["url"]`)

**Context Variables**:
```python
{
    'result': str,  # Status check result message
    'logs': List[Tuple[str, str, str]]  # Recent check history
}
```

**Example Usage**:
```python
# Manual function call (typically handled by Flask)
with app.test_request_context(method='POST', data={'url': 'https://google.com'}):
    response = home()
```

**Error Handling**:
- Automatically adds `https://` protocol if missing
- Handles `requests.exceptions.RequestException` for failed connections
- Logs all results regardless of success/failure

#### `popular_status()`
**File**: `my_flask_app/app.py` (lines 87-104)  
**Route**: `/api/popular_status` (GET)  
**Description**: API endpoint that returns status of predefined popular websites

**Parameters**: None  
**Returns**: JSON response with site statuses

**Response Schema**:
```json
{
  "statuses": {
    "site_url": "up" | "down"
  }
}
```

**Example Usage**:
```python
# Direct function call
status_data = popular_status()
print(status_data.json)  # Access JSON data
```

**Performance Notes**:
- Checks 20 websites sequentially
- Each request has 10-second timeout
- Total execution time: ~10-200 seconds depending on site availability

---

## Database Functions

### Core Database Operations

#### `init_db()`
**Files**: `my_flask_app/app.py` (lines 26-38), `my_flask_app/db.py` (lines 6-18)  
**Description**: Initializes SQLite database and creates logs table

**Parameters**: None  
**Returns**: None  
**Side Effects**: Creates `logs.db` file and `logs` table if they don't exist

**Database Schema Created**:
```sql
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    checked_at TEXT NOT NULL
);
```

**Example Usage**:
```python
# Initialize database (usually called automatically)
init_db()
```

**Error Handling**:
- Uses `IF NOT EXISTS` to prevent errors on repeated calls
- Properly closes database connection in all cases

#### `log_result(url, status)`
**Files**: `my_flask_app/app.py` (lines 43-49), `my_flask_app/db.py` (lines 20-26)  
**Description**: Logs a website status check result to the database

**Parameters**:
- `url` (str): The website URL that was checked
- `status` (str): The status message/result from the check

**Returns**: None  
**Side Effects**: Inserts new record into `logs` table

**Timestamp Format**: `YYYY-MM-DD HH:MM:SS`

**Example Usage**:
```python
log_result("https://example.com", "https://example.com is UP ✅ (Status Code: 200)")
log_result("https://down-site.com", "https://down-site.com is DOWN ❌ (Failed to connect)")
```

**Database Insert**:
```sql
INSERT INTO logs (url, status, checked_at) VALUES (?, ?, ?)
```

#### `get_logs(limit=10)`
**File**: `my_flask_app/db.py` (lines 28-35)  
**Description**: Retrieves recent log entries from the database

**Parameters**:
- `limit` (int, optional): Maximum number of records to return (default: 10)

**Returns**: `List[Tuple[str, str, str]]` - List of (url, status, checked_at) tuples

**SQL Query**:
```sql
SELECT url, status, checked_at FROM logs 
ORDER BY id DESC LIMIT ?
```

**Example Usage**:
```python
# Get last 5 checks
recent_checks = get_logs(5)
for url, status, timestamp in recent_checks:
    print(f"{timestamp}: {url} -> {status}")

# Get default last 10 checks
all_recent = get_logs()
```

**Return Example**:
```python
[
    ('https://google.com', 'https://google.com is UP ✅ (Status Code: 200)', '2024-01-15 14:30:25'),
    ('https://example.com', 'https://example.com is DOWN ❌ (Failed to connect)', '2024-01-15 14:29:15')
]
```

---

## Frontend Functions

### JavaScript Functions

#### `updatePopularBarChart()`
**File**: `my_flask_app/templates/index.html` (lines 63-119)  
**Description**: Updates the Chart.js bar chart with current website statuses

**Parameters**: None  
**Returns**: `Promise<void>`  
**Dependencies**: Chart.js library, `/api/popular_status` endpoint

**Async Behavior**: Fetches data from API and updates chart

**Chart Configuration**:
```javascript
{
  type: 'bar',
  data: {
    labels: Array<string>,        // Website URLs
    datasets: [{
      label: 'Website Status (1 = UP, 0 = DOWN)',
      data: Array<number>,        // 1 for up, 0 for down
      backgroundColor: Array<string>  // Green for up, red for down
    }]
  }
}
```

**Example Usage**:
```javascript
// Manual call
await updatePopularBarChart();

// Automatic updates (already implemented)
setInterval(updatePopularBarChart, 5000);
```

**Error Handling**:
```javascript
try {
  // Chart update logic
} catch (err) {
  console.error("Chart.js failed to render:", err);
}
```

#### `updateStatusTable()`
**File**: `my_flask_app/templates/index.html` (lines 121-142)  
**Description**: Updates the outages table showing only down websites

**Parameters**: None  
**Returns**: `Promise<void>`  
**Dependencies**: `/api/popular_status` endpoint

**DOM Manipulation**: Updates `#statusTable tbody` content

**Logic Flow**:
1. Fetch status data from API
2. Clear existing table rows
3. Add rows only for sites with status !== 'up'
4. Show "No current outages" message if all sites are up

**Example Usage**:
```javascript
// Manual call
await updateStatusTable();

// Automatic updates (already implemented)
setInterval(updateStatusTable, 5000);
```

**Generated HTML Structure**:
```html
<!-- For each down site -->
<tr>
  <td>https://example.com</td>
  <td><span class="badge bg-danger">DOWN</span></td>
</tr>

<!-- When no outages -->
<tr>
  <td colspan="2" class="text-center text-muted">
    No current outages detected.
  </td>
</tr>
```

---

## Utility Functions

### HTTP Request Configuration

#### Default Headers
**Location**: Multiple locations in `app.py`  
**Description**: Standard User-Agent header used for all HTTP requests

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
```

**Purpose**: 
- Avoid being blocked by websites that filter bot traffic
- Mimic real browser requests
- Consistent across all status checks

### URL Processing

#### Automatic Protocol Addition
**Location**: `my_flask_app/app.py` (lines 59-60)  
**Description**: Automatically adds HTTPS protocol if missing from user input

```python
if not url.startswith('http'):
    url = 'https://' + url
```

**Examples**:
- Input: `"google.com"` → Output: `"https://google.com"`
- Input: `"http://example.com"` → Output: `"http://example.com"` (unchanged)
- Input: `"https://site.com"` → Output: `"https://site.com"` (unchanged)

### Status Message Generation

#### Response Status Mapping
**Location**: `my_flask_app/app.py` (lines 67-73)  
**Description**: Converts HTTP responses to user-friendly status messages

**Mapping Logic**:
```python
if response.status_code == 200:
    result = f"{url} is UP ✅ (Status Code: 200)"
else:
    result = f"{url} is reachable but returned status code {response.status_code} ⚠️"
```

**Exception Handling**:
```python
except requests.exceptions.RequestException:
    result = f"{url} is DOWN ❌ (Failed to connect)"
```

**Status Categories**:
- **UP** (✅): HTTP 200 response
- **WARNING** (⚠️): Non-200 HTTP response (3xx, 4xx, 5xx)
- **DOWN** (❌): Network/connection failure

---

## Configuration

### Global Variables

#### `popular_sites`
**File**: `my_flask_app/app.py` (lines 11-19)  
**Type**: `List[str]`  
**Description**: List of popular websites to monitor

**Current Sites** (20 total):
```python
[
    "https://www.amazon.com", "https://www.apple.com", 
    "https://www.bing.com", "https://www.ebay.com",
    "https://www.facebook.com", "https://www.google.com",
    "https://www.instagram.com", "https://www.linkedin.com",
    "https://www.live.com", "https://www.microsoft.com",
    "https://www.netflix.com", "https://www.office.com",
    "https://www.pinterest.com", "https://www.reddit.com",
    "https://www.twitch.tv", "https://www.twitter.com",
    "https://www.wikipedia.org", "https://www.wordpress.com",
    "https://www.yahoo.com", "https://www.youtube.com"
]
```

**Customization**:
```python
# Add your own sites
popular_sites.extend([
    "https://your-site.com",
    "https://another-site.org"
])

# Replace entirely
popular_sites = [
    "https://custom-site1.com",
    "https://custom-site2.com"
]
```

#### `DB_NAME`
**Files**: `my_flask_app/app.py` (line 21), `my_flask_app/db.py` (line 4)  
**Type**: `str`  
**Value**: `"logs.db"`  
**Description**: SQLite database filename

**Customization**:
```python
# Use different database file
DB_NAME = "custom_monitoring.db"

# Use full path
DB_NAME = "/path/to/database/monitoring.db"
```

### Request Configuration

#### Timeout Settings
**Location**: Multiple locations  
**Value**: `timeout=10` (seconds)  
**Description**: Maximum time to wait for HTTP responses

**Customization**:
```python
# Shorter timeout for faster feedback
response = requests.get(url, headers=headers, timeout=5)

# Longer timeout for slow sites
response = requests.get(url, headers=headers, timeout=30)
```

### Frontend Configuration

#### Update Intervals
**Location**: `my_flask_app/templates/index.html` (lines 144-148)  
**Description**: How often frontend components refresh

**Current Settings**:
```javascript
// Update charts and tables every 5 seconds
setInterval(updatePopularBarChart, 5000);
setInterval(updateStatusTable, 5000);
```

**Customization**:
```javascript
// Update every 10 seconds
setInterval(updatePopularBarChart, 10000);

// Update every 30 seconds
setInterval(updateStatusTable, 30000);

// Different intervals for different components
setInterval(updatePopularBarChart, 5000);   // Charts update faster
setInterval(updateStatusTable, 15000);      // Tables update slower
```

---

## Function Call Examples

### Complete Workflow Example
```python
# 1. Initialize application
from flask import Flask
app = Flask(__name__)

# 2. Setup database
init_db()

# 3. Check a website manually
url = "https://example.com"
headers = {"User-Agent": "Mozilla/5.0..."}

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        status = f"{url} is UP ✅ (Status Code: 200)"
    else:
        status = f"{url} returned status code {response.status_code} ⚠️"
except requests.exceptions.RequestException:
    status = f"{url} is DOWN ❌ (Failed to connect)"

# 4. Log the result
log_result(url, status)

# 5. Retrieve recent logs
recent_logs = get_logs(5)
for url, status, timestamp in recent_logs:
    print(f"{timestamp}: {status}")
```

### API Integration Example
```javascript
// Frontend integration with backend functions
async function monitorWebsites() {
  try {
    // Get current popular site statuses
    const response = await fetch('/api/popular_status');
    const data = await response.json();
    
    // Process results
    const upSites = Object.entries(data.statuses)
      .filter(([site, status]) => status === 'up')
      .map(([site, status]) => site);
    
    const downSites = Object.entries(data.statuses)
      .filter(([site, status]) => status === 'down')
      .map(([site, status]) => site);
    
    console.log(`${upSites.length} sites up, ${downSites.length} sites down`);
    
    // Update UI components
    await updatePopularBarChart();
    await updateStatusTable();
    
  } catch (error) {
    console.error('Monitoring failed:', error);
  }
}

// Run monitoring every 5 seconds
setInterval(monitorWebsites, 5000);
```