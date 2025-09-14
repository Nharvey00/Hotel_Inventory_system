# db.py
import mysql.connector

def get_connection():
    """Return a new MySQL connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",              # change if you set a MySQL password
        database="hotel_inventory" # make sure this is your DB name
    )

def get_cursor(dictionary=False):
    """
    Return (cursor, conn). If dictionary=True returns dictionary cursor.
    Caller must close both cursor and conn when done.
    """
    conn = get_connection()
    if dictionary:
        cur = conn.cursor(dictionary=True)
    else:
        cur = conn.cursor()
    return cur, conn
