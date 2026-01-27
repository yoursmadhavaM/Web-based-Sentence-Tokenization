# Troubleshooting Guide

## Common Issues and Solutions

### Issue: Connection Refused Error

**Error Message:**
```
GET http://localhost:8000/health net::ERR_CONNECTION_REFUSED
POST http://localhost:8000/segment net::ERR_CONNECTION_REFUSED
```

**Cause:** The FastAPI backend server is not running.

**Solution:**

1. **Start the Backend Server:**

   Open a terminal/command prompt and navigate to the project directory:
   ```bash
   cd c:\Users\rvr\Desktop\NLP
   ```

   Then start the server using one of these methods:

   **Method 1: Using the convenience script (Recommended)**
   ```bash
   python run_server.py
   ```

   **Method 2: Using uvicorn directly**
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify Server is Running:**

   You should see output like:
   ```
   ======================================================================
   Starting Sentence Segmentation API Server
   ======================================================================
   
   Server will be available at: http://localhost:8000
   API documentation: http://localhost:8000/docs
   
   Press Ctrl+C to stop the server.
   
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   ```

3. **Test the Server:**

   Open your browser and go to:
   - **API Health Check**: http://localhost:8000/health
   - **API Documentation**: http://localhost:8000/docs
   - **Web Interface**: http://localhost:8000

4. **Keep the Server Running:**

   **Important:** Keep the terminal window open while using the application. The server must remain running for the frontend to work.

   To stop the server, press `Ctrl+C` in the terminal.

---

### Issue: Port 8000 Already in Use

**Error Message:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**

**Option 1: Stop the process using port 8000**

On Windows (PowerShell):
```powershell
netstat -ano | findstr :8000
# Note the PID from the output, then:
taskkill /PID <PID> /F
```

On Linux/Mac:
```bash
lsof -ti:8000 | xargs kill -9
```

**Option 2: Use a different port**

Edit `run_server.py` and change the port:
```python
uvicorn.run(
    "backend.main:app",
    host="0.0.0.0",
    port=8001,  # Change to 8001 or another port
    reload=True,
    log_level="info"
)
```

Then update `frontend/script.js` to use the new port:
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

---

### Issue: spaCy Models Not Found

**Error Message:**
```
OSError: [E050] Can't find model 'en_core_web_sm'
```

**Solution:**

1. **Download the English model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Verify installation:**
   ```bash
   python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully!')"
   ```

3. **For multilingual support (optional):**
   ```bash
   python -m spacy download fr_core_news_sm  # French
   python -m spacy download de_core_news_sm  # German
   python -m spacy download es_core_news_sm  # Spanish
   ```

---

### Issue: Module Import Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   pip list | grep fastapi
   pip list | grep spacy
   ```

3. **If using virtual environment, activate it first:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   
   # Then install dependencies
   pip install -r requirements.txt
   ```

---

### Issue: Frontend Not Loading

**Error Message:**
```
Failed to load resource: net::ERR_FILE_NOT_FOUND
```

**Solution:**

1. **Make sure you're accessing via the backend server:**
   - ✅ Correct: http://localhost:8000
   - ❌ Incorrect: file:///path/to/frontend/index.html

2. **The backend serves the frontend automatically** when you access http://localhost:8000

3. **If you need to serve frontend separately**, use a local server:
   ```bash
   # Python 3
   cd frontend
   python -m http.server 3000
   ```
   Then update `script.js` API_BASE_URL to point to backend on port 8000.

---

### Issue: CORS Errors

**Error Message:**
```
Access to fetch at 'http://localhost:8000/segment' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**

The backend already has CORS enabled. If you still see errors:

1. **Check backend/main.py** - CORS middleware should be configured:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Restart the server** after making changes.

---

### Quick Start Checklist

Before running the application, ensure:

- [ ] Python 3.11+ is installed
- [ ] Dependencies are installed: `pip install -r requirements.txt`
- [ ] spaCy English model is downloaded: `python -m spacy download en_core_web_sm`
- [ ] Backend server is running: `python run_server.py`
- [ ] Server is accessible at http://localhost:8000/health
- [ ] Browser can access http://localhost:8000

---

### Testing the Setup

Run these commands to verify everything is set up correctly:

```bash
# 1. Test Python installation
python --version

# 2. Test dependencies
python -c "import fastapi; import spacy; print('Dependencies OK')"

# 3. Test spaCy model
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model OK')"

# 4. Test backend imports
python -c "from backend.main import app; print('Backend imports OK')"

# 5. Start server
python run_server.py
```

---

### Getting Help

If issues persist:

1. Check the terminal output for detailed error messages
2. Verify all files are in the correct locations
3. Ensure you're in the project root directory when running commands
4. Check that no firewall is blocking port 8000
5. Review the README.md for detailed setup instructions

---

## Quick Fix for Current Issue

**To fix your current connection refused error:**

1. Open a new terminal/command prompt
2. Navigate to project directory:
   ```bash
   cd c:\Users\rvr\Desktop\NLP
   ```
3. Start the server using one of these methods:

   **Method 1: Try different Python commands**
   ```bash
   # Try these in order:
   python run_server.py
   # OR
   python3 run_server.py
   # OR
   py run_server.py
   ```

   **Method 2: Use the Windows batch script**
   ```bash
   START_SERVER.bat
   ```

   **Method 3: Use uvicorn directly**
   ```bash
   py -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Wait for the server to start (you'll see "Uvicorn running on http://0.0.0.0:8000")
5. Keep this terminal open
6. Refresh your browser at http://localhost:8000
7. The application should now work!

**Remember:** The server must stay running while you use the application.

---

## Issue: Python Not Found

**Error Message:**
```
Python was not found; run without arguments to install from the Microsoft Store
```

**Solution:**

### Option 1: Install Python (If Not Installed)

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 or later for Windows

2. **Install Python:**
   - Run the installer
   - **IMPORTANT:** Check the box "Add Python to PATH" during installation
   - Click "Install Now"

3. **Verify Installation:**
   - Open a NEW command prompt (close and reopen)
   - Run: `python --version`
   - Should show: `Python 3.11.x` or similar

### Option 2: Use Python Launcher (Windows)

If Python is installed but `python` command doesn't work, try:

```bash
# Use Python launcher
py run_server.py

# Or specify version
py -3.11 run_server.py
```

### Option 3: Find Python Installation

1. **Check if Python is installed:**
   - Open File Explorer
   - Navigate to: `C:\Users\<YourUsername>\AppData\Local\Programs\Python\`
   - Or: `C:\Python311\` (or similar version)

2. **Use full path:**
   ```bash
   C:\Python311\python.exe run_server.py
   ```

### Option 4: Add Python to PATH Manually

1. **Find Python installation path:**
   - Usually: `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\`
   - Or: `C:\Python311\`

2. **Add to PATH:**
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add Python installation directory
   - Also add: `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\Scripts\`
   - Click OK on all dialogs
   - **Restart command prompt**

### Option 5: Use Virtual Environment

If you have Python installed but commands don't work:

```bash
# Create virtual environment
py -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python run_server.py
```

### Quick Test Commands

Try these to find which Python command works:

```bash
# Test 1
python --version

# Test 2
python3 --version

# Test 3
py --version

# Test 4
where python
where python3
where py
```

**Once you find which command works, use that to run the server!**
