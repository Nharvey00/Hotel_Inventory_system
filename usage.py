# usage.py
import db
import items
from datetime import datetime

def log_usage(item_id, user_id, quantity_used, purpose=None):
    """
    Log usage and subtract from items.quantity.
    This opens its own connection and then calls items.adjust_quantity to change stock.
    """
    cur, conn = db.get_cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO `usage` (item_id, user_id, quantity_used, date_used, purpose) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (item_id, user_id, quantity_used, now, purpose))
    conn.commit()
    cur.close()
    conn.close()

    # subtract from items (negative delta)
    items.adjust_quantity(item_id, -abs(quantity_used))
