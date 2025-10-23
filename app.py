from flask import Flask, render_template, request, redirect, session, url_for, flash
import pymysql
app = Flask(__name__)
app.secret_key = "secret123"
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="x",   
        database="test_db_1",
        cursorclass=pymysql.cursors.DictCursor
    )
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                    (name, email, subject, message))
        conn.commit()
        conn.close()
        flash("Your message has been sent!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cur.fetchone()
        conn.close()
        if admin:
            session['admin'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('admin_login.html')
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages ORDER BY date DESC")
    messages = cur.fetchall()
    conn.close()

    return render_template('dashboard.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('admin_login'))
app.run(debug=True)

