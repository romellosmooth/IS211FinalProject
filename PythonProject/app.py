from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '173451'  # Needed for sessions

# Database Connection
def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = 'Randi'
        published_date = request.form['published_date']  # User can still provide this

        db = get_db()
        db.execute("INSERT INTO posts (title, content, author, published_date) VALUES (?, ?, ?, ?)",
                   (title, content, author, published_date))
        db.commit()
        return redirect(url_for('dashboard'))

    # Render the form when the request method is GET
    return render_template('add_post.html', current_date=current_date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':  # Simple login logic
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY published_date DESC').fetchall()
    return render_template('index.html', posts=posts)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db()
    posts = db.execute('SELECT id, title FROM posts ORDER BY published_date DESC').fetchall()
    return render_template("dashboard.html", posts=posts, page_class="dashboard-page")


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        new_author = request.form['author']
        new_published = request.form['published_date']

        db.execute(
            'UPDATE posts SET title = ?, content = ?, author = ?, published_date = ? WHERE id = ?',
            (new_title, new_content, new_author, new_published, post_id)
        )
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
