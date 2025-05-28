# Extend Flask backend to support search functionality
from flask import Flask, request, jsonify, render_template
import sqlite3


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('Job-Browse-Page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/addJob')
def addJob():
    return render_template('addJob.html')
@app.route('/account')
def account():
    return render_template('account.html')

def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    job_type TEXT NOT NULL,
                    description TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    query = request.args.get('q', '').strip()
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    if query:
        c.execute('''SELECT * FROM jobs WHERE 
                        title LIKE ? OR 
                        location LIKE ? OR 
                        job_type LIKE ? OR 
                        description LIKE ?''',
                  tuple([f"%{query}%"] * 7))
    else:
        c.execute('SELECT * FROM jobs')
    jobs = [dict(id=row[0], title=row[1], location=row[2],
                 job_type=row[3], description=row[4])
            for row in c.fetchall()]
    conn.close()
    return jsonify(jobs)

@app.route('/api/jobs', methods=['POST'])
def add_job():
    data = request.get_json()
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''INSERT INTO jobs (title, location, job_type, description)
                 VALUES (?, ?, ?, ? )''',
              (data['title'], data['location'],
               data['job_type'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201




if __name__ == '__main__':
    init_db()
    app.run(debug=True)

