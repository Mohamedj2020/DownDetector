# 🛠️ DownDetector Developer Guide

## Table of Contents
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Deployment](#deployment)
- [API Extensions](#api-extensions)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.7+ installed
- Basic knowledge of Flask and JavaScript
- Text editor or IDE (VS Code recommended)

### 5-Minute Setup
```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd downdetector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
cd my_flask_app
python app.py

# 4. Open browser
# Visit: http://localhost:5000
```

### First Test
1. Enter a website URL (e.g., `google.com`)
2. Click "Check Status"
3. View the result and check the history table
4. Watch the live charts update automatically

---

## Development Setup

### Recommended Environment
```bash
# Create virtual environment
python -m venv downdetector_env

# Activate virtual environment
# On Windows:
downdetector_env\Scripts\activate
# On macOS/Linux:
source downdetector_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest flask-testing
```

### IDE Configuration

#### VS Code Settings (`.vscode/settings.json`)
```json
{
    "python.defaultInterpreterPath": "./downdetector_env/Scripts/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.associations": {
        "*.html": "html"
    }
}
```

#### Debugging Configuration (`.vscode/launch.json`)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/my_flask_app/app.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

### Environment Variables
Create a `.env` file in the project root:
```bash
# Development settings
FLASK_ENV=development
FLASK_DEBUG=True

# Database configuration
DB_NAME=logs.db

# API settings (future use)
API_RATE_LIMIT=100
```

---

## Code Structure

### Project Layout
```
downdetector/
├── my_flask_app/           # Main application directory
│   ├── app.py             # Flask application and routes
│   ├── db.py              # Database functions
│   ├── templates/         # HTML templates
│   │   └── index.html     # Main page template
│   ├── logs.db           # SQLite database (auto-generated)
│   └── .gitignore        # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
├── API_DOCUMENTATION.md  # Complete API docs
├── FUNCTION_REFERENCE.md # Function documentation
└── DEVELOPER_GUIDE.md    # This file
```

### Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Flask App    │    │   Database      │
│   (HTML/JS)     │◄──►│    (Python)     │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │
│ • Form Input    │    │ • Route Handlers│    │ • logs table    │
│ • Chart.js      │    │ • Status Check  │    │ • Timestamps    │
│ • Auto Updates  │    │ • API Endpoints │    │ • Status History│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components

#### 1. Flask Application (`app.py`)
- **Route Handlers**: Process HTTP requests
- **Status Checking Logic**: Website availability testing
- **Database Integration**: Log results and retrieve history

#### 2. Database Layer (`db.py`)
- **Schema Management**: Table creation and maintenance
- **Data Access**: CRUD operations for logs
- **Query Functions**: Retrieve filtered data

#### 3. Frontend (`templates/index.html`)
- **User Interface**: Form inputs and result display
- **Real-time Updates**: JavaScript polling for live data
- **Visualization**: Chart.js for status graphs

---

## Adding New Features

### Example 1: Add Email Notifications

#### Step 1: Install Email Dependencies
```bash
pip install flask-mail
```

#### Step 2: Add Email Configuration
```python
# In app.py, add after imports
from flask_mail import Mail, Message
import os

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)
```

#### Step 3: Create Email Function
```python
def send_alert_email(url, status):
    """Send email alert when site goes down"""
    if "DOWN" in status:
        msg = Message(
            subject=f'Site Down Alert: {url}',
            sender=app.config['MAIL_USERNAME'],
            recipients=['admin@yourcompany.com']
        )
        msg.body = f'Alert: {url} is currently down.\n\nStatus: {status}\nTime: {datetime.now()}'
        mail.send(msg)
```

#### Step 4: Integrate with Status Checking
```python
# In home() function, after log_result():
log_result(url, result)
send_alert_email(url, result)  # Add this line
```

### Example 2: Add Response Time Tracking

#### Step 1: Update Database Schema
```python
# Add to init_db() function
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time REAL,  -- Add this field
            checked_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
```

#### Step 2: Measure Response Time
```python
# In home() function, modify the status check:
import time

start_time = time.time()
try:
    response = requests.get(url, headers=headers, timeout=10)
    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    if response.status_code == 200:
        result = f"{url} is UP ✅ (Status Code: 200, {response_time:.0f}ms)"
    else:
        result = f"{url} returned status code {response.status_code} ⚠️ ({response_time:.0f}ms)"
except requests.exceptions.RequestException:
    response_time = None
    result = f"{url} is DOWN ❌ (Failed to connect)"

# Update log_result call
log_result(url, result, response_time)
```

#### Step 3: Update Database Function
```python
def log_result(url, status, response_time=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)', 
            (url, status, response_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
```

### Example 3: Add User Authentication

#### Step 1: Install Flask-Login
```bash
pip install flask-login
```

#### Step 2: Create User Model
```python
# Add to db.py
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

def create_user_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
```

#### Step 3: Add Login Routes
```python
# In app.py
from flask_login import LoginManager, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic here
    pass

@app.route('/dashboard')
@login_required
def dashboard():
    # Protected dashboard
    return render_template('dashboard.html')
```

---

## Testing

### Unit Tests

#### Test Setup (`tests/test_app.py`)
```python
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_flask_app.app import app, init_db
from my_flask_app.db import log_result, get_logs

class DownDetectorTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Website Uptime Checker', response.data)

    def test_api_popular_status(self):
        """Test popular status API endpoint"""
        response = self.app.get('/api/popular_status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('statuses', response.get_json())

    def test_database_operations(self):
        """Test database logging and retrieval"""
        # Test logging
        log_result("https://test.com", "Test status")
        
        # Test retrieval
        logs = get_logs(1)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0][0], "https://test.com")

if __name__ == '__main__':
    unittest.main()
```

#### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_app.py::DownDetectorTestCase::test_home_page_loads

# Run with coverage
pip install pytest-cov
python -m pytest --cov=my_flask_app tests/
```

### Integration Tests

#### Test Website Checking (`tests/test_integration.py`)
```python
import unittest
from unittest.mock import patch, Mock
from my_flask_app.app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('my_flask_app.app.requests.get')
    def test_website_check_success(self, mock_get):
        """Test successful website check"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.app.post('/', data={'url': 'google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'is UP', response.data)

    @patch('my_flask_app.app.requests.get')
    def test_website_check_failure(self, mock_get):
        """Test failed website check"""
        # Mock failed response
        mock_get.side_effect = Exception("Connection failed")

        response = self.app.post('/', data={'url': 'nonexistent.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'is DOWN', response.data)
```

---

## Deployment

### Development Server
```bash
# Standard Flask development server
cd my_flask_app
python app.py

# With environment variables
FLASK_ENV=development FLASK_DEBUG=True python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
cd my_flask_app
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY my_flask_app/ ./my_flask_app/
WORKDIR /app/my_flask_app

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

Build and run:
```bash
docker build -t downdetector .
docker run -p 8000:8000 downdetector
```

#### Render.com Deployment

Create `render.yaml`:
```yaml
services:
  - type: web
    name: downdetector
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "cd my_flask_app && gunicorn -w 4 -b 0.0.0.0:$PORT app:app"
    envVars:
      - key: PYTHON_VERSION
        value: "3.9.7"
```

---

## API Extensions

### Adding Rate Limiting

#### Install Dependencies
```bash
pip install flask-limiter
```

#### Implementation
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/popular_status')
@limiter.limit("10 per minute")
def popular_status():
    # Existing code...
```

### Adding API Keys

#### Create API Key Model
```python
# In db.py
def create_api_keys_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def validate_api_key(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM api_keys WHERE key = ?', (key,))
    result = c.fetchone()
    conn.close()
    return result is not None
```

#### Protect Endpoints
```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/status/<url>')
@require_api_key
def check_single_site(url):
    # Check specific site
    pass
```

### Adding Webhooks

```python
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Receive webhook notifications for monitoring"""
    data = request.get_json()
    
    # Process webhook data
    url = data.get('url')
    status = data.get('status')
    
    if url and status:
        log_result(url, status)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid data'}), 400
```

---

## Performance Optimization

### Database Optimizations

#### Add Indexes
```python
def create_indexes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Index for faster timestamp queries
    c.execute('CREATE INDEX IF NOT EXISTS idx_checked_at ON logs(checked_at)')
    
    # Index for URL searches
    c.execute('CREATE INDEX IF NOT EXISTS idx_url ON logs(url)')
    
    conn.commit()
    conn.close()
```

#### Pagination
```python
def get_logs_paginated(page=1, per_page=10):
    offset = (page - 1) * per_page
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT url, status, checked_at 
        FROM logs 
        ORDER BY id DESC 
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    
    logs = c.fetchall()
    conn.close()
    return logs
```

### Caching

#### Redis Caching
```bash
pip install redis flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/popular_status')
@cache.cached(timeout=30)  # Cache for 30 seconds
def popular_status():
    # Expensive operation cached
    pass
```

### Async Processing

#### Background Tasks with Celery
```bash
pip install celery redis
```

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379')

@celery.task
def check_site_async(url):
    """Check site status in background"""
    # Status checking logic
    pass

@app.route('/api/check_async', methods=['POST'])
def check_async():
    url = request.json.get('url')
    task = check_site_async.delay(url)
    return jsonify({'task_id': task.id})
```

---

## Troubleshooting

### Common Issues

#### 1. Database Lock Errors
**Problem**: `database is locked` error
**Solution**:
```python
# Use connection pooling
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=20)
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_db_connection() as conn:
    c = conn.cursor()
    # Database operations
```

#### 2. Request Timeouts
**Problem**: Slow website checks causing timeouts
**Solution**:
```python
# Reduce timeout for faster feedback
try:
    response = requests.get(url, headers=headers, timeout=5)
except requests.exceptions.Timeout:
    result = f"{url} is DOWN ❌ (Request timeout)"
```

#### 3. Memory Usage
**Problem**: High memory usage with many concurrent requests
**Solution**:
```python
# Limit concurrent checks
import threading
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

def check_sites_concurrent(sites):
    futures = [executor.submit(check_single_site, site) for site in sites]
    return [future.result() for future in futures]
```

### Debug Mode

#### Enable Detailed Logging
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

app.logger.setLevel(logging.DEBUG)
```

#### Flask Debug Toolbar
```bash
pip install flask-debugtoolbar
```

```python
from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['DEBUG_TB_ENABLED'] = True
toolbar = DebugToolbarExtension(app)
```

### Performance Monitoring

#### Add Request Timing
```python
import time
from flask import g

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start_time
    app.logger.info(f'Request took {diff:.3f} seconds')
    return response
```

---

## Contributing

### Code Style Guidelines
- Use 4 spaces for indentation
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions under 50 lines when possible

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature: description"

# Push and create pull request
git push origin feature/new-feature
```

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Functions have docstrings
- [ ] Tests are included
- [ ] No hardcoded values
- [ ] Error handling is implemented
- [ ] Performance impact considered

This developer guide provides a comprehensive foundation for working with the DownDetector application. For specific implementation details, refer to the API Documentation and Function Reference guides.