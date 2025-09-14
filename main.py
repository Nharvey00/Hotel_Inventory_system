# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import items, usage, purchase_orders, users, db

CURRENT_USER = None

# ------------------ Global Style ------------------
def apply_style(root=None):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg="#f4f6f9")

    style.configure("TFrame", background="#f4f6f9")
    style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#dfe6ee")
    style.map("Treeview", background=[("selected", "#4a90e2")], foreground=[("selected", "white")])
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat", background="#4a90e2", foreground="white")
    style.map("TButton",
              background=[("active", "#357ab8")],
              foreground=[("active", "white")])

    style.configure("TNotebook.Tab", padding=[14, 8], font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", "#4a90e2")], foreground=[("selected", "white")])

# ------------------ Login Screen ------------------
def show_login(root):
    root.title("Hotel Inventory - Login")
    root.geometry("420x280")
    apply_style(root)

    login_frame = ttk.Frame(root, padding=32)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_lbl = ttk.Label(login_frame, text="🏨 Hotel Inventory", font=("Segoe UI", 18, "bold"))
    title_lbl.grid(row=0, column=0, columnspan=2, pady=(0,16))

    ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=8, padx=4)
    username_entry = ttk.Entry(login_frame, width=28, font=("Segoe UI", 10))
    username_entry.grid(row=1, column=1, pady=8)

    ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=8, padx=4)
    password_entry = ttk.Entry(login_frame, show="*", width=28, font=("Segoe UI", 10))
    password_entry.grid(row=2, column=1, pady=8)

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get()
        user = users.authenticate(username, password)
        if user:
            global CURRENT_USER
            CURRENT_USER = user
            for widget in root.winfo_children():
                widget.destroy()
            show_dashboard(root)
        else:
            messagebox.showerror("Login Failed", "❌ Invalid username or password")

    login_btn = ttk.Button(login_frame, text="Login", command=attempt_login)
    login_btn.grid(row=3, column=0, columnspan=2, pady=16, ipadx=10)

# ------------------ Dashboard ------------------
def show_dashboard(root):
    root.title("🏨 Hotel Inventory System")
    root.state("zoomed")
    apply_style(root)

    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill="x")
    user_label = ttk.Label(top_frame, text=f"👤 {CURRENT_USER.get('username')} ({CURRENT_USER.get('role','')})",
                           font=("Segoe UI", 11, "bold"))
    user_label.pack(side="left")
    ttk.Button(top_frame, text="Logout", command=lambda: logout(root)).pack(side="right", padx=6)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Items Tab ---
    items_tab = ttk.Frame(nb)
    nb.add(items_tab, text="📦 Items")
    item_cols = ("item_id", "name", "category", "quantity", "unit_price", "reorder_level")
    item_tree = ttk.Treeview(items_tab, columns=item_cols, show="headings")
    for c in item_cols:
        item_tree.heading(c, text=c.title())
        item_tree.column(c, anchor="center", width=140)
    item_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_items():
        for r in item_tree.get_children():
            item_tree.delete(r)
        rows = items.read_items()
        for row in rows:
            item_tree.insert("", "end", values=(row['item_id'], row['name'], row['category'],
                                                row['quantity'], float(row['unit_price']), row['reorder_level']))
    refresh_items()

    # --- Usage Tab ---
    usage_tab = ttk.Frame(nb)
    nb.add(usage_tab, text="📝 Usage")

    usage_frame = ttk.LabelFrame(usage_tab, text="Record Usage", padding=12)
    usage_frame.pack(anchor="nw", fill="x", padx=10, pady=10)

    ttk.Label(usage_frame, text="Item ID:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    usage_item = ttk.Entry(usage_frame, width=24); usage_item.grid(row=0, column=1, padx=6, pady=6)

    ttk.Label(usage_frame, text="Quantity:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
    usage_qty = ttk.Entry(usage_frame, width=24); usage_qty.grid(row=1, column=1, padx=6, pady=6)

    ttk.Label(usage_frame, text="Purpose:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
    usage_purpose = ttk.Entry(usage_frame, width=36); usage_purpose.grid(row=2, column=1, padx=6, pady=6)

    def do_log_usage():
        try:
            item_id_val = int(usage_item.get())
            qty_val = int(usage_qty.get())
            purpose_val = usage_purpose.get().strip() or None
            usage.log_usage(item_id_val, CURRENT_USER['user_id'], qty_val, purpose_val)
            messagebox.showinfo("✅ Success", "Usage recorded")
            usage_item.delete(0, 'end'); usage_qty.delete(0, 'end'); usage_purpose.delete(0, 'end')
            refresh_items()
            refresh_usage()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(usage_frame, text="Record Usage", command=do_log_usage).grid(row=3, column=1, sticky="w", pady=10)

    usage_log_frame = ttk.Frame(usage_tab, padding=8)
    usage_log_frame.pack(fill="both", expand=True, padx=10, pady=8)
    usage_cols = ("usage_id", "item_id", "user_id", "quantity_used", "date_used", "purpose")
    usage_tree = ttk.Treeview(usage_log_frame, columns=usage_cols, show="headings")
    for c in usage_cols:
        usage_tree.heading(c, text=c.title())
        usage_tree.column(c, width=120, anchor="center")
    usage_tree.pack(fill="both", expand=True)

    def refresh_usage():
        for r in usage_tree.get_children():
            usage_tree.delete(r)
        cur, conn = db.get_cursor(dictionary=True)
        cur.execute("SELECT usage_id, item_id, user_id, quantity_used, date_used, purpose FROM `usage` ORDER BY usage_id DESC LIMIT 200")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for u in rows:
            usage_tree.insert("", "end", values=(u['usage_id'], u['item_id'], u['user_id'],
                                                 u['quantity_used'], u['date_used'], u['purpose']))
    refresh_usage()

    # --- Purchase Orders Tab ---
    po_tab = ttk.Frame(nb)
    nb.add(po_tab, text="📑 Purchase Orders")

    po_frame = ttk.LabelFrame(po_tab, text="Create Purchase Order", padding=12)
    po_frame.pack(anchor="nw", fill="x", padx=10, pady=10)

    ttk.Label(po_frame, text="Item ID:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    po_item_e = ttk.Entry(po_frame, width=24); po_item_e.grid(row=0, column=1, padx=6, pady=6)

    ttk.Label(po_frame, text="Supplier:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
    po_supplier_e = ttk.Entry(po_frame, width=30); po_supplier_e.grid(row=1, column=1, padx=6, pady=6)

    ttk.Label(po_frame, text="Quantity:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
    po_qty_e = ttk.Entry(po_frame, width=24); po_qty_e.grid(row=2, column=1, padx=6, pady=6)

    ttk.Label(po_frame, text="Unit Price:").grid(row=3, column=0, sticky="w", padx=6, pady=6)
    po_price_e = ttk.Entry(po_frame, width=24); po_price_e.grid(row=3, column=1, padx=6, pady=6)

    def do_create_po():
        try:
            iid = int(po_item_e.get())
            qty = int(po_qty_e.get())
            price = float(po_price_e.get())
            supplier = po_supplier_e.get().strip() or None
            purchase_orders.create_order(iid, supplier, qty, price, CURRENT_USER['user_id'])
            messagebox.showinfo("✅ Success", "Purchase order created (Pending)")
            po_item_e.delete(0,'end'); po_qty_e.delete(0,'end'); po_price_e.delete(0,'end'); po_supplier_e.delete(0,'end')
            refresh_po()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(po_frame, text="Create Order", command=do_create_po).grid(row=4, column=1, sticky="w", pady=10)

    po_list_frame = ttk.Frame(po_tab, padding=8)
    po_list_frame.pack(fill="both", expand=True, padx=10, pady=8)
    po_cols = ("order_id", "item_id", "supplier_name", "quantity", "unit_price", "order_date", "status", "user_id")
    po_tree = ttk.Treeview(po_list_frame, columns=po_cols, show="headings")
    for c in po_cols:
        po_tree.heading(c, text=c.title())
        po_tree.column(c, width=120, anchor="center")
    po_tree.pack(fill="both", expand=True)

    def refresh_po():
        for r in po_tree.get_children():
            po_tree.delete(r)
        cur, conn = db.get_cursor(dictionary=True)
        cur.execute("SELECT order_id, item_id, supplier_name, quantity, unit_price, order_date, status, user_id FROM purchase_orders ORDER BY order_id DESC LIMIT 200")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for p in rows:
            po_tree.insert("", "end", values=(p['order_id'], p['item_id'], p['supplier_name'],
                                              p['quantity'], float(p['unit_price']), p['order_date'], p['status'], p.get('user_id')))
    refresh_po()

    def approve_selected_order():
        sel = po_tree.selection()
        if not sel:
            messagebox.showinfo("Choose", "Select an order to approve.")
            return
        order_id = po_tree.item(sel[0])['values'][0]
        try:
            purchase_orders.approve_order(order_id)
            messagebox.showinfo("✅ Success", "Order approved and stock updated.")
            refresh_po()
            refresh_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(po_tab, text="Approve Selected Order", command=approve_selected_order).pack(anchor="ne", padx=12, pady=8)

    root.refresh_items = refresh_items
    root.refresh_usage = refresh_usage
    root.refresh_po = refresh_po

def logout(root):
    for w in root.winfo_children():
        w.destroy()
    show_login(root)

# ------------------ Run ------------------
if __name__ == "__main__":
    root = tk.Tk()
    show_login(root)
    root.mainloop()
