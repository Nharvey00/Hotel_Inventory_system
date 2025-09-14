# items.py
import db

def create_item(name, category, quantity, unit_price, reorder_level):
    cur, conn = db.get_cursor()
    sql = "INSERT INTO items (name, category, quantity, unit_price, reorder_level) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (name, category, quantity, unit_price, reorder_level))
    conn.commit()
    cur.close()
    conn.close()

def read_items():
    """Return list of dicts: item_id, name, category, quantity, unit_price, reorder_level"""
    cur, conn = db.get_cursor(dictionary=True)
    cur.execute("SELECT item_id, name, category, quantity, unit_price, reorder_level FROM items ORDER BY item_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_item(item_id):
    cur, conn = db.get_cursor(dictionary=True)
    cur.execute("SELECT item_id, name, category, quantity, unit_price, reorder_level FROM items WHERE item_id=%s", (item_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def update_item(item_id, name, category, quantity, unit_price, reorder_level):
    cur, conn = db.get_cursor()
    sql = "UPDATE items SET name=%s, category=%s, quantity=%s, unit_price=%s, reorder_level=%s WHERE item_id=%s"
    cur.execute(sql, (name, category, quantity, unit_price, reorder_level, item_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_item(item_id):
    cur, conn = db.get_cursor()
    cur.execute("DELETE FROM items WHERE item_id=%s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()

def adjust_quantity(item_id, delta):
    """
    Adjust item quantity by delta (positive to add, negative to subtract).
    Uses independent connection (keeps interfaces simple).
    """
    cur, conn = db.get_cursor()
    sql = "UPDATE items SET quantity = quantity + %s WHERE item_id=%s"
    cur.execute(sql, (delta, item_id))
    conn.commit()
    cur.close()
    conn.close()
