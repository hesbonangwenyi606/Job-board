# Job Board (Flask + SQLite)

A simple job board web application built with Flask and SQLite.

## Features
- List job postings
- Create, edit, delete job postings
- Search jobs by title or company
- Initialize database with sample jobs

## Quick start (locally)
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database (creates `jobs.db` with sample data):
   ```bash
   python init_db.py
   ```
4. Run the app:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   ```
   or
   ```bash
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## Files in this project
- `app.py` — main Flask application
- `init_db.py` — script to initialize the SQLite database with sample jobs
- `jobs.db` — (created after running init_db.py)
- `templates/` — HTML templates (Bootstrap via CDN)
- `static/` — static files (CSS)
- `requirements.txt` — Python dependencies

## Notes
- This is a minimal, self-contained example intended for learning and local use.
- No authentication or file uploads included.
# Job-board
