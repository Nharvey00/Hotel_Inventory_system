# users.py
import db

def authenticate(username, password):
    """
    Return user dict if credentials match, otherwise None.
    Assumes users table has columns: user_id, username, password, role
    (password currently compared in plaintext — replace with hashing if desired)
    """
    cur, conn = db.get_cursor(dictionary=True)
    cur.execute("SELECT user_id, username, password, role FROM users WHERE username=%s LIMIT 1", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and user.get('password') == password:
        return user
    return None

def create_user(username, password, role='staff'):
    cur, conn = db.get_cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    conn.commit()
    cur.close()
    conn.close()
