# purchase_orders.py
import db
import items
from datetime import datetime

def create_order(item_id, supplier_name, quantity, unit_price, user_id=None):
    """
    Create a purchase order. Status defaults to 'Pending'.
    """
    cur, conn = db.get_cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO purchase_orders
             (item_id, supplier_name, quantity, unit_price, order_date, status, user_id)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (item_id, supplier_name, quantity, unit_price, now, 'Pending', user_id))
    conn.commit()
    cur.close()
    conn.close()

def approve_order(order_id, delivered_qty=None):
    """
    Approve (or mark delivered) an order and update item quantity accordingly.
    delivered_qty if provided will be used, otherwise order.quantity is used.
    """
    cur, conn = db.get_cursor(dictionary=True)
    cur.execute("SELECT * FROM purchase_orders WHERE order_id=%s", (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()

    if not order:
        raise ValueError("Order not found")

    if order['status'].lower() == 'approved' or order['status'].lower() == 'delivered':
        # already processed
        return

    qty_to_add = delivered_qty if delivered_qty is not None else order['quantity']

    # mark order as approved/delivered
    cur2, conn2 = db.get_cursor()
    cur2.execute("UPDATE purchase_orders SET status=%s WHERE order_id=%s", ('Approved', order_id))
    conn2.commit()
    cur2.close()
    conn2.close()

    # increase stock
    items.adjust_quantity(order['item_id'], qty_to_add)
