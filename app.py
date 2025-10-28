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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects ORDER BY date DESC")
    projects = cur.fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)
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
@app.route('/admin/message')
def message():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages ORDER BY date DESC")
    messages = cur.fetchall()
    conn.close()

    return render_template('message.html', messages=messages)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/admin/projects')
def admin_projects():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects ORDER BY date DESC")
    projects = cur.fetchall()
    conn.close()
    return render_template('admin_projects.html', projects=projects)

@app.route('/admin/project/add', methods=['GET', 'POST'])
def add_project():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO projects (title, description, image) VALUES (%s, %s, %s)",
                    (title, description, image))
        conn.commit()
        conn.close()
        flash("Project added successfully!", "success")
        return redirect(url_for('admin_projects'))
    return render_template('add_project.html')

@app.route('/admin/project/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        cur.execute("UPDATE projects SET title=%s, description=%s, image=%s WHERE id=%s",
                    (title, description, image, id))
        conn.commit()
        flash("Project updated!", "info")
        conn.close()
        return redirect(url_for('admin_projects'))
    cur.execute("SELECT * FROM projects WHERE id=%s", (id,))
    project = cur.fetchone()
    conn.close()
    return render_template('edit_project.html', project=project)

@app.route('/admin/project/delete/<int:id>')
def delete_project(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash("Project deleted!", "danger")
    return redirect(url_for('admin_projects'))


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('admin_login'))
app.run(debug=True)

