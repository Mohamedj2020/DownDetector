# ⚡ DownDetector Quick Reference Card

## 🚀 Quick Commands

### Start Application
```bash
cd my_flask_app && python app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
python -m pytest tests/
```

---

## 🔗 API Quick Reference

### Check Website Status
```bash
curl -X POST http://localhost:5000/ -d "url=google.com"
```

### Get Popular Sites Status
```bash
curl http://localhost:5000/api/popular_status
```

### JavaScript API Call
```javascript
fetch('/api/popular_status').then(r => r.json()).then(console.log)
```

---

## 💾 Database Quick Reference

### Log a Result
```python
from db import log_result
log_result("https://example.com", "UP ✅")
```

### Get Recent Logs
```python
from db import get_logs
logs = get_logs(10)  # Last 10 entries
```

### Database Schema
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    checked_at TEXT NOT NULL
);
```

---

## 🛠️ Development Quick Reference

### File Structure
```
my_flask_app/
├── app.py          # Main Flask app
├── db.py           # Database functions
├── templates/
│   └── index.html  # Frontend template
└── logs.db         # SQLite database
```

### Key Functions
- `home()` - Main route handler
- `popular_status()` - API endpoint
- `init_db()` - Database setup
- `log_result()` - Log status check
- `get_logs()` - Retrieve history

### Configuration
```python
# Popular sites list
popular_sites = ["https://www.google.com", ...]

# Database name
DB_NAME = "logs.db"

# Request timeout
timeout=10  # seconds
```

---

## 🐛 Troubleshooting Quick Fix

### Database Lock Error
```python
# Use timeout
conn = sqlite3.connect(DB_NAME, timeout=20)
```

### Import Error
```bash
# Check working directory
cd my_flask_app
python app.py
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Permission Error
```bash
# Fix file permissions
chmod +x app.py
```

---

## 📊 Status Messages

| Emoji | Status | Meaning |
|-------|--------|---------|
| ✅ | UP | HTTP 200 response |
| ⚠️ | WARNING | Non-200 HTTP response |
| ❌ | DOWN | Connection failed |

---

## 🔧 Common Customizations

### Add New Site to Monitor
```python
# In app.py
popular_sites.append("https://your-site.com")
```

### Change Update Interval
```javascript
// In index.html
setInterval(updatePopularBarChart, 10000); // 10 seconds
```

### Modify Request Timeout
```python
# In app.py
response = requests.get(url, timeout=5)  # 5 seconds
```

---

## 📁 Documentation Navigation

| Need | Document |
|------|----------|
| Setup | [Developer Guide](DEVELOPER_GUIDE.md#quick-start) |
| API Reference | [API Documentation](API_DOCUMENTATION.md) |
| Function Details | [Function Reference](FUNCTION_REFERENCE.md) |
| All Docs | [Documentation Index](DOCUMENTATION_INDEX.md) |

---

## 🎯 Common Tasks

### Add Email Notifications
1. Install: `pip install flask-mail`
2. Configure SMTP settings
3. Create email function
4. Integrate with status checks

### Deploy with Docker
1. Create Dockerfile
2. Build: `docker build -t downdetector .`
3. Run: `docker run -p 8000:8000 downdetector`

### Add Rate Limiting
1. Install: `pip install flask-limiter`
2. Initialize limiter
3. Add decorators to routes

### Enable Debug Mode
```python
app.run(debug=True)
```

---

## 💡 Pro Tips

- Use virtual environments: `python -m venv venv`
- Check logs in real-time: `tail -f logs.db`
- Test API with Postman or curl
- Use SQLite browser for database inspection
- Monitor memory usage in production
- Implement caching for better performance

---

*For detailed information, see the [complete documentation index](DOCUMENTATION_INDEX.md).*