import sqlite3

conn = sqlite3.connect('jobs.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT,
    qualifications TEXT,
    requirements TEXT,
    apply_email TEXT
)
''')

conn.commit()
conn.close()
print("Initialized jobs.db")
