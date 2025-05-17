import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()


# Load schema
with open('posts.sql') as f:
    c.executescript(f.read())

c.execute("INSERT INTO posts (title, content, author, published_date) VALUES ('My First Post', 'This is the content.', 'Randi', '2025-05-10')")
conn.commit()
conn.close()

