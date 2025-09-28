import tkinter as tk
from tkinter import ttk, messagebox
import items, usage, purchase_orders, users, db

CURRENT_USER = None

# ------------------ Modern Color Scheme ------------------
COLORS = {
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'secondary': '#059669',
    'secondary_hover': '#047857',
    'danger': '#dc2626',
    'danger_hover': '#b91c1c',
    'warning': '#d97706',
    'success': '#16a34a',
    'dark': '#111827',
    'dark_light': '#1f2937',
    'medium': '#374151',
    'light': '#6b7280',
    'lighter': '#9ca3af',
    'lightest': '#f3f4f6',
    'white': '#ffffff',
    'accent': '#8b5cf6',
    'border': '#e2e8f0',
}

# ------------------ Modern Button Component ------------------
class ModernButton:
    def __init__(self, parent, text, command, style='primary', width=120, height=40):
        self.parent = parent
        self.command = command
        
        styles = {
            'primary': {'bg': COLORS['primary'], 'hover': COLORS['primary_hover'], 'fg': COLORS['white']},
            'secondary': {'bg': COLORS['secondary'], 'hover': COLORS['secondary_hover'], 'fg': COLORS['white']},
            'danger': {'bg': COLORS['danger'], 'hover': COLORS['danger_hover'], 'fg': COLORS['white']},
            'warning': {'bg': COLORS['warning'], 'hover': COLORS['warning'], 'fg': COLORS['white']},
        }
        
        self.style_config = styles.get(style, styles['primary'])
        
        self.frame = tk.Frame(parent, bg=self.style_config['bg'], cursor='hand2', 
                             relief='flat', bd=0, highlightthickness=0)
        self.frame.configure(width=width, height=height)
        self.frame.pack_propagate(False)
        
        self.label = tk.Label(
            self.frame, 
            text=text, 
            bg=self.style_config['bg'], 
            fg=self.style_config['fg'],
            font=('Segoe UI', 10, 'bold'),
            cursor='hand2',
            bd=0,
            highlightthickness=0
        )
        self.label.place(relx=0.5, rely=0.5, anchor='center')
        
        self.bind_events()
    
    def bind_events(self):
        widgets = [self.frame, self.label]
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: self.command())
            widget.bind('<Enter>', self.on_enter)
            widget.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.frame.config(bg=self.style_config['hover'])
        self.label.config(bg=self.style_config['hover'])
    
    def on_leave(self, e):
        self.frame.config(bg=self.style_config['bg'])
        self.label.config(bg=self.style_config['bg'])
    
    def pack(self, **kwargs):
        return self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)

# ------------------ Card Frame Helper ------------------
def create_card_frame(parent, title="", padding=20):
    shadow_frame = tk.Frame(parent, bg=COLORS['lighter'], bd=0)
    card_frame = tk.Frame(shadow_frame, bg=COLORS['white'], bd=0, relief='flat')
    card_frame.pack(padx=2, pady=2, fill='both', expand=True)
    
    if title:
        title_frame = tk.Frame(card_frame, bg=COLORS['white'], height=50)
        title_frame.pack(fill='x', padx=padding, pady=(padding, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title, bg=COLORS['white'], 
                              fg=COLORS['dark'], font=('Segoe UI', 14, 'bold'))
        title_label.pack(anchor='w', pady=(10, 0))
        
        separator = tk.Frame(card_frame, bg=COLORS['border'], height=1)
        separator.pack(fill='x', padx=padding, pady=(10, 0))
    
    content_frame = tk.Frame(card_frame, bg=COLORS['white'])
    content_frame.pack(fill='both', expand=True, padx=padding, pady=padding)
    
    return shadow_frame, content_frame

def create_modern_entry(parent):
    entry_frame = tk.Frame(parent, bg=COLORS['white'], bd=1, relief='solid',
                          highlightcolor=COLORS['primary'], highlightthickness=1)
    
    entry = tk.Entry(entry_frame, font=('Segoe UI', 10), bg=COLORS['white'], 
                    fg=COLORS['dark'], bd=0, highlightthickness=0)
    entry.pack(padx=12, pady=10, fill='x')
    
    return entry_frame, entry

# ------------------ Apply Modern Theme ------------------
def apply_modern_style(root=None):
    style = ttk.Style()
    try: 
        style.theme_use("clam")
    except: 
        pass
    
    if root:
        root.configure(bg=COLORS['lightest'])
    
    style.configure("TFrame", background=COLORS['lightest'], relief='flat')
    style.configure("TLabel", background=COLORS['lightest'], font=('Segoe UI', 10), 
                   foreground=COLORS['dark'])
    
    # Modern Treeview - Larger and more readable
    style.configure("Modern.Treeview", 
                   font=('Segoe UI', 11), 
                   rowheight=40,  # Increased row height for better readability
                   background=COLORS['white'],
                   foreground=COLORS['dark'], 
                   fieldbackground=COLORS['white'],
                   borderwidth=0,
                   relief='flat')
    style.configure("Modern.Treeview.Heading", 
                   font=('Segoe UI', 12, 'bold'),  # Larger header font
                   background=COLORS['primary'], 
                   foreground=COLORS['white'],
                   borderwidth=1,
                   relief='solid')
    style.map("Modern.Treeview", 
             background=[("selected", COLORS['primary'])], 
             foreground=[("selected", COLORS['white'])])
    
    # Modern Notebook
    style.configure("Modern.TNotebook", 
                   background=COLORS['lightest'],
                   borderwidth=0)
    style.configure("Modern.TNotebook.Tab", 
                   padding=[24, 15], 
                   font=('Segoe UI', 12, 'bold'), 
                   background=COLORS['white'], 
                   foreground=COLORS['light'],
                   borderwidth=1,
                   relief='solid')
    style.map("Modern.TNotebook.Tab", 
             background=[("selected", COLORS['primary'])], 
             foreground=[("selected", COLORS['white'])])
    
    # Modern Combobox
    style.configure("Modern.TCombobox",
                   font=('Segoe UI', 11),
                   fieldbackground=COLORS['white'],
                   background=COLORS['white'],
                   borderwidth=1,
                   relief='solid')

# ------------------ Modern Login Screen ------------------
def show_login(root):
    root.title("Hotel Inventory Management System")
    root.geometry("1200x700")
    root.state('zoomed')
    apply_modern_style(root)
    
    main_container = tk.Frame(root, bg=COLORS['lightest'])
    main_container.pack(fill='both', expand=True)
    
    # Left panel - Branding
    left_panel = tk.Frame(main_container, bg=COLORS['primary'], width=500)
    left_panel.pack(side='left', fill='y')
    left_panel.pack_propagate(False)
    
    right_panel = tk.Frame(main_container, bg=COLORS['lightest'])
    right_panel.pack(side='right', fill='both', expand=True)
    
    brand_frame = tk.Frame(left_panel, bg=COLORS['primary'])
    brand_frame.pack(expand=True, fill='both', padx=40, pady=40)
    
    tk.Label(brand_frame, text="🏨", font=('Segoe UI', 80), 
            bg=COLORS['primary'], fg=COLORS['white']).pack(pady=(50, 20))
    
    tk.Label(brand_frame, text="Hotel Inventory", 
            font=('Segoe UI', 28, 'bold'), 
            bg=COLORS['primary'], fg=COLORS['white']).pack(pady=(0, 10))
    
    tk.Label(brand_frame, text="Management System", 
            font=('Segoe UI', 18), 
            bg=COLORS['primary'], fg=COLORS['white']).pack(pady=(0, 30))
    
    tk.Label(brand_frame, text="Streamline your hotel operations\nwith our comprehensive inventory solution", 
            font=('Segoe UI', 12), 
            bg=COLORS['primary'], fg=COLORS['white'],
            justify='center').pack(pady=20)
    
    # Right panel - Login form
    login_container = tk.Frame(right_panel, bg=COLORS['lightest'])
    login_container.pack(expand=True)
    
    login_card, login_content = create_card_frame(login_container, "Sign In", padding=40)
    login_card.pack(expand=True, padx=100, pady=100, fill='both')
    
    tk.Label(login_content, text="Welcome back!", 
            font=('Segoe UI', 20, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).pack(pady=(0, 10))
    
    tk.Label(login_content, text="Please sign in to your account", 
            font=('Segoe UI', 12), 
            bg=COLORS['white'], fg=COLORS['light']).pack(pady=(0, 30))
    
    tk.Label(login_content, text="Username", 
            font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
    
    username_frame, username_entry = create_modern_entry(login_content)
    username_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(login_content, text="Password", 
            font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
    
    password_frame, password_entry = create_modern_entry(login_content)
    password_entry.config(show="*")
    password_frame.pack(fill='x', pady=(0, 30))
    
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
    
    login_btn = ModernButton(login_content, "Sign In", attempt_login, 
                            style='primary', width=150, height=45)
    login_btn.pack(pady=20)
    
    root.bind('<Return>', lambda e: attempt_login())
    username_entry.focus()

# ------------------ Logout Function ------------------
def logout(root):
    if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
        global CURRENT_USER
        CURRENT_USER = None
        for w in root.winfo_children(): 
            w.destroy()
        show_login(root)

# ------------------ Modern Dashboard ------------------
def show_dashboard(root):
    root.title("🏨 Hotel Inventory Management System")
    root.state("zoomed")
    apply_modern_style(root)
    
    main_container = tk.Frame(root, bg=COLORS['lightest'])
    main_container.pack(fill='both', expand=True)
    
    # Top header bar
    header_frame = tk.Frame(main_container, bg=COLORS['white'], height=80, bd=0)
    header_frame.pack(fill='x', pady=(0, 2))
    header_frame.pack_propagate(False)
    
    header_content = tk.Frame(header_frame, bg=COLORS['white'])
    header_content.pack(fill='both', expand=True, padx=30, pady=20)
    
    logo_frame = tk.Frame(header_content, bg=COLORS['white'])
    logo_frame.pack(side='left')
    
    tk.Label(logo_frame, text="🏨", font=('Segoe UI', 28), 
            bg=COLORS['white']).pack(side='left', padx=(0, 15))
    tk.Label(logo_frame, text="Hotel Inventory", 
            font=('Segoe UI', 20, 'bold'), 
            bg=COLORS['white'], fg=COLORS['primary']).pack(side='left')
    
    user_frame = tk.Frame(header_content, bg=COLORS['white'])
    user_frame.pack(side='right')
    
    user_info = f"👤 {CURRENT_USER.get('username')} ({CURRENT_USER.get('role','')})"
    tk.Label(user_frame, text=user_info,
            font=('Segoe UI', 12), bg=COLORS['white'], 
            fg=COLORS['dark']).pack(side='left', padx=(0, 25))
    
    logout_btn = ModernButton(user_frame, "Logout", lambda: logout(root), 
                             style='danger', width=110, height=40)
    logout_btn.pack(side='right')
    
    content_frame = tk.Frame(main_container, bg=COLORS['lightest'])
    content_frame.pack(fill='both', expand=True, padx=25, pady=20)
    
    nb = ttk.Notebook(content_frame, style="Modern.TNotebook")
    nb.pack(fill="both", expand=True)
    
    # ------------------ Items Tab ------------------
    items_tab = tk.Frame(nb, bg=COLORS['lightest'])
    nb.add(items_tab, text="📦 Inventory Items")
    
    items_container = tk.Frame(items_tab, bg=COLORS['lightest'])
    items_container.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Statistics cards
    stats_frame = tk.Frame(items_container, bg=COLORS['lightest'])
    stats_frame.pack(fill='x', pady=(0, 25))
    
    def create_stat_card(parent, title, value, icon, color):
        card_frame = tk.Frame(parent, bg=color, bd=0, relief='flat', height=90)
        card_frame.pack(side='left', fill='x', padx=(0, 20), expand=True)
        card_frame.pack_propagate(False)
        
        content = tk.Frame(card_frame, bg=color)
        content.pack(fill='both', expand=True, padx=25, pady=20)
        
        tk.Label(content, text=icon, font=('Segoe UI', 28), 
                bg=color, fg=COLORS['white']).pack(side='left', padx=(0, 20))
        
        text_frame = tk.Frame(content, bg=color)
        text_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(text_frame, text=str(value), font=('Segoe UI', 20, 'bold'), 
                bg=color, fg=COLORS['white']).pack(anchor='w')
        tk.Label(text_frame, text=title, font=('Segoe UI', 11), 
                bg=color, fg=COLORS['white']).pack(anchor='w')
    
    # Items table card
    items_card, items_content = create_card_frame(items_container, "Inventory Overview")
    items_card.pack(fill='both', expand=True)
    
    item_cols = ("ID", "Name", "Category", "Quantity", "Unit Price", "Reorder Level")
    item_tree = ttk.Treeview(items_content, columns=item_cols, show="headings", 
                            style="Modern.Treeview", height=18)
    
    # Configure columns properly
    item_tree.column("ID", width=80, anchor="center")
    item_tree.column("Name", width=220, anchor="w")
    item_tree.column("Category", width=160, anchor="center")
    item_tree.column("Quantity", width=120, anchor="center")
    item_tree.column("Unit Price", width=140, anchor="center")
    item_tree.column("Reorder Level", width=140, anchor="center")
    
    for col in item_cols:
        item_tree.heading(col, text=col)
    
    vsb = ttk.Scrollbar(items_content, orient="vertical", command=item_tree.yview)
    item_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    item_tree.pack(fill="both", expand=True)
    
    def tag_rows(tree):
        for i, row in enumerate(tree.get_children()):
            tree.item(row, tags=("evenrow",) if i % 2 == 0 else ("oddrow",))
        tree.tag_configure("evenrow", background=COLORS['white'])
        tree.tag_configure("oddrow", background=COLORS['lightest'])
    
    def refresh_items():
        for r in item_tree.get_children(): 
            item_tree.delete(r)
        
        try:
            item_data = items.read_items()
            for row in item_data:
                item_tree.insert("", "end", values=(
                    row['item_id'], row['name'], row['category'],
                    row['quantity'], f"${float(row['unit_price']):.2f}", row['reorder_level']
                ))
            tag_rows(item_tree)
            update_statistics(item_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")
    
    def update_statistics(item_data):
        for widget in stats_frame.winfo_children():
            widget.destroy()
        
        try:
            total_items = len(item_data)
            low_stock = sum(1 for item in item_data if item['quantity'] <= item['reorder_level'])
            total_value = sum(item['quantity'] * float(item['unit_price']) for item in item_data)
            
            cur, conn = db.get_cursor()
            cur.execute("SELECT COUNT(*) FROM purchase_orders WHERE status = 'Pending'")
            pending_orders = cur.fetchone()[0]
            cur.close(); conn.close()
            
            create_stat_card(stats_frame, "Total Items", total_items, "📦", COLORS['primary'])
            create_stat_card(stats_frame, "Low Stock", low_stock, "⚠️", COLORS['warning'])
            create_stat_card(stats_frame, "Total Value", f"${total_value:,.2f}", "💰", COLORS['secondary'])
            create_stat_card(stats_frame, "Pending Orders", pending_orders, "📋", COLORS['accent'])
            
        except Exception as e:
            print(f"Stats error: {e}")
            create_stat_card(stats_frame, "Total Items", 0, "📦", COLORS['primary'])
            create_stat_card(stats_frame, "Low Stock", 0, "⚠️", COLORS['warning'])
            create_stat_card(stats_frame, "Total Value", "$0.00", "💰", COLORS['secondary'])
            create_stat_card(stats_frame, "Pending Orders", 0, "📋", COLORS['accent'])
    
    # ------------------ Enhanced Usage Tab ------------------
    usage_tab = tk.Frame(nb, bg=COLORS['lightest'])
    nb.add(usage_tab, text="📝 Usage Tracking")
    
    usage_container = tk.Frame(usage_tab, bg=COLORS['lightest'])
    usage_container.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Compact usage form card
    usage_form_card, usage_form_content = create_card_frame(usage_container, "📝 Record New Usage")
    usage_form_card.pack(fill='x', pady=(0, 25))
    usage_form_card.configure(height=180)  # Fixed height for form
    
    form_grid = tk.Frame(usage_form_content, bg=COLORS['white'])
    form_grid.pack(fill='x', pady=15)
    
    # Horizontal layout for form
    tk.Label(form_grid, text="Item:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=0, column=0, sticky='w', padx=(0, 15), pady=8)
    usage_item_cb = ttk.Combobox(form_grid, state="readonly", width=30, style="Modern.TCombobox")
    usage_item_cb.grid(row=0, column=1, pady=8, sticky='ew', padx=(0, 30))
    
    tk.Label(form_grid, text="Quantity:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=0, column=2, sticky='w', padx=(0, 15), pady=8)
    usage_qty_frame, usage_qty = create_modern_entry(form_grid)
    usage_qty_frame.grid(row=0, column=3, pady=8, sticky='ew', padx=(0, 30))
    
    tk.Label(form_grid, text="Purpose:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=1, column=0, sticky='w', padx=(0, 15), pady=8)
    usage_purpose_frame, usage_purpose = create_modern_entry(form_grid)
    usage_purpose_frame.grid(row=1, column=1, columnspan=2, pady=8, sticky='ew', padx=(0, 30))
    
    form_grid.columnconfigure(1, weight=1)
    form_grid.columnconfigure(3, weight=1)
    
    def do_log_usage():
        try:
            name = usage_item_cb.get()
            if not name:
                messagebox.showwarning("Warning", "Please select an item")
                return
            item_id = next(i['item_id'] for i in items.read_items() if i['name']==name)
            qty_val = int(usage_qty.get())
            purpose_val = usage_purpose.get().strip() or None
            usage.log_usage(item_id, CURRENT_USER['user_id'], qty_val, purpose_val)
            messagebox.showinfo("✅ Success", "Usage recorded successfully")
            usage_item_cb.set(''); usage_qty.delete(0,'end'); usage_purpose.delete(0,'end')
            refresh_items(); refresh_usage()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
    
    record_btn = ModernButton(form_grid, "Record Usage", do_log_usage, 
                             style='secondary', width=150, height=45)
    record_btn.grid(row=1, column=3, pady=15, sticky='e')
    
    # Large usage history table
    usage_history_card, usage_history_content = create_card_frame(usage_container, "📊 Usage History")
    usage_history_card.pack(fill='both', expand=True)
    
    usage_cols = ("Usage ID", "Item Name", "User", "Quantity", "Date Used", "Purpose")
    usage_tree = ttk.Treeview(usage_history_content, columns=usage_cols, show="headings", 
                             style="Modern.Treeview", height=18)  # Increased height
    
    for col in usage_cols:
        usage_tree.heading(col, text=col)
        if col == "Item Name":
            usage_tree.column(col, width=200, anchor="w")
        elif col == "Purpose":
            usage_tree.column(col, width=250, anchor="w")
        elif col == "Date Used":
            usage_tree.column(col, width=180, anchor="center")
        else:
            usage_tree.column(col, width=120, anchor="center")
    
    vsb2 = ttk.Scrollbar(usage_history_content, orient="vertical", command=usage_tree.yview)
    usage_tree.configure(yscrollcommand=vsb2.set)
    vsb2.pack(side="right", fill="y")
    usage_tree.pack(fill="both", expand=True)
    
    def tag_usage_rows(tree):
        for i, row in enumerate(tree.get_children()):
            tree.item(row, tags=("evenrow",) if i % 2 == 0 else ("oddrow",))
        tree.tag_configure("evenrow", background=COLORS['white'])
        tree.tag_configure("oddrow", background=COLORS['lightest'])
    
    def refresh_usage():
        for r in usage_tree.get_children(): 
            usage_tree.delete(r)
        
        try:
            cur, conn = db.get_cursor(dictionary=True)
            cur.execute("""
                SELECT u.usage_id, i.name AS item_name, us.username AS user_name, 
                       u.quantity_used, u.date_used, u.purpose
                FROM `usage` u
                JOIN items i ON u.item_id=i.item_id
                JOIN users us ON u.user_id=us.user_id
                ORDER BY u.usage_id DESC LIMIT 500
            """)
            rows = cur.fetchall()
            cur.close(); conn.close()
            
            for u in rows:
                usage_tree.insert("", "end", values=(
                    u['usage_id'], u['item_name'], u['user_name'],
                    u['quantity_used'], u['date_used'], u['purpose'] or 'N/A'
                ))
            tag_usage_rows(usage_tree)
            usage_item_cb['values'] = [i['name'] for i in items.read_items()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load usage history: {str(e)}")
    
    # ------------------ Enhanced Purchase Orders Tab ------------------
    po_tab = tk.Frame(nb, bg=COLORS['lightest'])
    nb.add(po_tab, text="📑 Purchase Orders")
    
    po_container = tk.Frame(po_tab, bg=COLORS['lightest'])
    po_container.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Compact PO form card
    po_form_card, po_form_content = create_card_frame(po_container, "📑 Create Purchase Order")
    po_form_card.pack(fill='x', pady=(0, 25))
    po_form_card.configure(height=200)  # Fixed height for form
    
    po_form_grid = tk.Frame(po_form_content, bg=COLORS['white'])
    po_form_grid.pack(fill='x', pady=15)
    
    # Horizontal layout for PO form
    tk.Label(po_form_grid, text="Item:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=0, column=0, sticky='w', padx=(0, 15), pady=8)
    po_item_cb = ttk.Combobox(po_form_grid, state="readonly", width=25, style="Modern.TCombobox")
    po_item_cb.grid(row=0, column=1, pady=8, sticky='ew', padx=(0, 20))
    
    tk.Label(po_form_grid, text="Supplier:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=0, column=2, sticky='w', padx=(0, 15), pady=8)
    po_supplier_frame, po_supplier_e = create_modern_entry(po_form_grid)
    po_supplier_frame.grid(row=0, column=3, pady=8, sticky='ew', padx=(0, 20))
    
    tk.Label(po_form_grid, text="Quantity:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=1, column=0, sticky='w', padx=(0, 15), pady=8)
    po_qty_frame, po_qty_e = create_modern_entry(po_form_grid)
    po_qty_frame.grid(row=1, column=1, pady=8, sticky='ew', padx=(0, 20))
    
    tk.Label(po_form_grid, text="Unit Price:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=1, column=2, sticky='w', padx=(0, 15), pady=8)
    po_price_frame, po_price_e = create_modern_entry(po_form_grid)
    po_price_e.config(state="readonly", bg=COLORS['lightest'])
    po_price_frame.grid(row=1, column=3, pady=8, sticky='ew', padx=(0, 20))
    
    tk.Label(po_form_grid, text="Total Price:", font=('Segoe UI', 11, 'bold'), 
            bg=COLORS['white'], fg=COLORS['dark']).grid(row=2, column=0, sticky='w', padx=(0, 15), pady=8)
    po_total_frame, po_total_e = create_modern_entry(po_form_grid)
    po_total_e.config(state="readonly", bg=COLORS['lightest'])
    po_total_frame.grid(row=2, column=1, pady=8, sticky='ew', padx=(0, 20))
    
    po_form_grid.columnconfigure(1, weight=1)
    po_form_grid.columnconfigure(3, weight=1)
    
    def update_po_prices(event=None):
        name = po_item_cb.get()
        qty_text = po_qty_e.get()
        if not name or not qty_text.isdigit():
            po_price_e.config(state="normal"); po_price_e.delete(0,'end'); po_price_e.config(state="readonly")
            po_total_e.config(state="normal"); po_total_e.delete(0,'end'); po_total_e.config(state="readonly")
            return
        
        try:
            item = next(i for i in items.read_items() if i['name']==name)
            unit_price = float(item['unit_price'])
            total_price = unit_price * int(qty_text)
            po_price_e.config(state="normal"); po_price_e.delete(0,'end'); 
            po_price_e.insert(0, f"${unit_price:.2f}"); po_price_e.config(state="readonly")
            po_total_e.config(state="normal"); po_total_e.delete(0,'end'); 
            po_total_e.insert(0, f"${total_price:.2f}"); po_total_e.config(state="readonly")
        except:
            pass
    
    po_item_cb.bind("<<ComboboxSelected>>", update_po_prices)
    po_qty_e.bind("<KeyRelease>", update_po_prices)
    
    def do_create_po():
        try:
            item_name = po_item_cb.get()
            if not item_name:
                messagebox.showwarning("Warning", "Please select an item")
                return
            item = next(i for i in items.read_items() if i['name']==item_name)
            supplier = po_supplier_e.get().strip()
            if not supplier:
                messagebox.showwarning("Warning", "Please enter supplier name")
                return
            qty = int(po_qty_e.get())
            price = float(item['unit_price'])
            purchase_orders.create_order(item['item_id'], supplier, qty, price, CURRENT_USER['user_id'])
            messagebox.showinfo("✅ Success", "Purchase order created successfully!")
            po_item_cb.set(''); po_supplier_e.delete(0,'end'); po_qty_e.delete(0,'end')
            po_price_e.config(state="normal"); po_price_e.delete(0,'end'); po_price_e.config(state="readonly")
            po_total_e.config(state="normal"); po_total_e.delete(0,'end'); po_total_e.config(state="readonly")
            refresh_po(); refresh_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    create_po_btn = ModernButton(po_form_grid, "Create Order", do_create_po, 
                                style='primary', width=150, height=45)
    create_po_btn.grid(row=2, column=3, pady=15, sticky='e')
    
    # Large Purchase Orders table with approve button
    po_history_card, po_history_content = create_card_frame(po_container, "📋 Purchase Orders Management")
    po_history_card.pack(fill='both', expand=True)
    
    # Action button at top right
    po_action_frame = tk.Frame(po_history_content, bg=COLORS['white'])
    po_action_frame.pack(fill='x', pady=(0, 15))
    
    def approve_selected_order():
        sel = po_tree.selection()
        if not sel:
            messagebox.showinfo("Selection Required", "Please select an order to approve.")
            return
        
        order_values = po_tree.item(sel[0])['values']
        order_id = order_values[0]
        status = order_values[7]  # Status column
        
        # Check if already approved
        if "Approved" in status or "Delivered" in status:
            messagebox.showinfo("Info", "This order has already been approved.")
            return
        
        try:
            purchase_orders.approve_order(order_id)
            messagebox.showinfo("✅ Success", "Order approved and stock updated successfully!")
            refresh_po(); refresh_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    approve_po_btn = ModernButton(po_action_frame, "✅ Approve Selected Order", approve_selected_order, 
                                 style='secondary', width=220, height=45)
    approve_po_btn.pack(side='right')
    
    po_cols = ("Order ID", "Item Name", "Supplier", "Quantity", "Unit Price", "Total Price", "Date", "Status", "User")
    po_tree = ttk.Treeview(po_history_content, columns=po_cols, show="headings", 
                          style="Modern.Treeview", height=16)  # Increased height
    
    # Configure PO columns for better visibility
    po_tree.column("Order ID", width=100, anchor="center")
    po_tree.column("Item Name", width=200, anchor="w")
    po_tree.column("Supplier", width=150, anchor="w")
    po_tree.column("Quantity", width=100, anchor="center")
    po_tree.column("Unit Price", width=120, anchor="center")
    po_tree.column("Total Price", width=130, anchor="center")
    po_tree.column("Date", width=180, anchor="center")
    po_tree.column("Status", width=120, anchor="center")
    po_tree.column("User", width=120, anchor="center")
    
    for col in po_cols:
        po_tree.heading(col, text=col)
    
    vsb3 = ttk.Scrollbar(po_history_content, orient="vertical", command=po_tree.yview)
    po_tree.configure(yscrollcommand=vsb3.set)
    vsb3.pack(side="right", fill="y")
    po_tree.pack(fill="both", expand=True)
    
    def tag_po_rows(tree):
        for i, row in enumerate(tree.get_children()):
            tree.item(row, tags=("evenrow",) if i % 2 == 0 else ("oddrow",))
        tree.tag_configure("evenrow", background=COLORS['white'])
        tree.tag_configure("oddrow", background=COLORS['lightest'])
    
    def refresh_po():
        for r in po_tree.get_children(): 
            po_tree.delete(r)
        
        try:
            cur, conn = db.get_cursor(dictionary=True)
            cur.execute("""
                SELECT po.order_id, i.name AS item_name, po.supplier_name, po.quantity, po.unit_price,
                       (po.quantity * po.unit_price) AS total_price, po.order_date, po.status, u.username AS user_name
                FROM purchase_orders po
                JOIN items i ON po.item_id=i.item_id
                JOIN users u ON po.user_id=u.user_id
                ORDER BY po.order_id DESC LIMIT 500
            """)
            rows = cur.fetchall()
            cur.close(); conn.close()
            
            for p in rows:
                status_display = f"🟡 {p['status']}" if p['status'] == 'Pending' else f"🟢 {p['status']}"
                po_tree.insert("", "end", values=(
                    p['order_id'], p['item_name'], p['supplier_name'], p['quantity'],
                    f"${float(p['unit_price']):.2f}", f"${float(p['total_price']):.2f}", 
                    p['order_date'], status_display, p['user_name']
                ))
            tag_po_rows(po_tree)
            po_item_cb['values'] = [i['name'] for i in items.read_items()]
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load purchase orders: {str(e)}")
    
    # Load initial data
    refresh_items()  
    refresh_usage()  
    refresh_po()     
    
    # Attach refresh functions to root for external access
    root.refresh_items = refresh_items
    root.refresh_usage = refresh_usage  
    root.refresh_po = refresh_po

# ------------------ Application Entry Point ------------------
if __name__ == "__main__":
    root = tk.Tk()
    show_login(root)
    root.mainloop()
