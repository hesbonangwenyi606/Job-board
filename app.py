from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'jobs.db'

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # replace in production

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    conn = get_db_connection()
    if q:
        cur = conn.execute("SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ? ORDER BY created_at DESC",
                           (f'%{q}%', f'%{q}%'))
    else:
        cur = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = cur.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs, q=q)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    conn = get_db_connection()
    job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    if job is None:
        flash('Job not found', 'warning')
        return redirect(url_for('index'))
    return render_template('job_detail.html', job=job)

@app.route('/new', methods=('GET', 'POST'))
def new_job():
    if request.method == 'POST':
        title = request.form['title'].strip()
        company = request.form['company'].strip()
        location = request.form['location'].strip()
        description = request.form['description'].strip()
        apply_email = request.form['apply_email'].strip()
        if not title or not company:
            flash('Title and company are required.', 'danger')
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO jobs (title, company, location, description, apply_email) VALUES (?, ?, ?, ?, ?)",
                (title, company, location, description, apply_email)
            )
            conn.commit()
            conn.close()
            flash('Job created.', 'success')
            return redirect(url_for('index'))
    return render_template('new_job.html')

@app.route('/edit/<int:job_id>', methods=('GET', 'POST'))
def edit_job(job_id):
    conn = get_db_connection()
    job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if job is None:
        conn.close()
        flash('Job not found', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title'].strip()
        company = request.form['company'].strip()
        location = request.form['location'].strip()
        description = request.form['description'].strip()
        apply_email = request.form['apply_email'].strip()
        if not title or not company:
            flash('Title and company are required.', 'danger')
        else:
            conn.execute(
                "UPDATE jobs SET title=?, company=?, location=?, description=?, apply_email=? WHERE id=?",
                (title, company, location, description, apply_email, job_id)
            )
            conn.commit()
            conn.close()
            flash('Job updated.', 'success')
            return redirect(url_for('job_detail', job_id=job_id))
    conn.close()
    return render_template('edit_job.html', job=job)

@app.route('/delete/<int:job_id>', methods=('POST',))
def delete_job(job_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    flash('Job deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/init-db')
def init_db_route():
    # convenience route to init DB from browser (idempotent)
    init_db()
    flash('Database initialized (or already exists).', 'info')
    return redirect(url_for('index'))

def init_db():
    if DB_PATH.exists():
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT,
        description TEXT,
        apply_email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    sample = [
        ('Backend Developer', 'Acme Corp', 'Nairobi, Kenya', 'Work on our payments platform.', 'jobs@acme.example'),
        ('Frontend Developer', 'Greenwheels', 'Remote', 'Build UI components.', 'talent@greenwheels.example'),
        ('Data Analyst', 'HealthTech', 'Nairobi, Kenya', 'Analyze clinical data.', 'hr@healthtech.example'),
    ]
    cur.executemany("INSERT INTO jobs (title, company, location, description, apply_email) VALUES (?, ?, ?, ?, ?)", sample)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # initialize DB if missing
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
