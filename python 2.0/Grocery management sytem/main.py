import tkinter as tk
from tkinter import messagebox, ttk
import json

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')

        self.items = {}
        self.file_path = "grocery_data.json"

        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        # Frame for entry fields
        entry_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20, borderwidth=2, relief="flat")
        entry_frame.pack(padx=15, pady=10, fill="x")

        # Labels and Entry fields
        tk.Label(entry_frame, text="Item Name:", bg='#ffffff', font=("Helvetica", 12)).grid(row=0, column=0, padx=10,
                                                                                            pady=5, sticky="w")
        tk.Label(entry_frame, text="Quantity:", bg='#ffffff', font=("Helvetica", 12)).grid(row=1, column=0, padx=10,
                                                                                           pady=5, sticky="w")
        tk.Label(entry_frame, text="Price:", bg='#ffffff', font=("Helvetica", 12)).grid(row=2, column=0, padx=10,
                                                                                        pady=5, sticky="w")

        self.item_name = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.item_name.grid(row=0, column=1, padx=10, pady=5)
        self.quantity = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.quantity.grid(row=1, column=1, padx=10, pady=5)
        self.price = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.price.grid(row=2, column=1, padx=10, pady=5)

        # Frame for buttons and search input
        button_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=10)
        button_frame.pack(padx=15, pady=10, fill="x")

        # Buttons with modern design
        btn_config = {"font": ("Helvetica", 12), "padx": 10, "pady": 5, "width": 14, "bd": 0, "relief": "flat"}
        tk.Button(button_frame, text="Add Item", command=self.add_item, bg='#4CAF50', fg='#ffffff', **btn_config).grid(
            row=0, column=0)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg='#f44336', fg='#ffffff',
                  **btn_config).grid(row=0, column=1)
        tk.Button(button_frame, text="Update Item", command=self.update_item, bg='#2196F3', fg='#ffffff',
                  **btn_config).grid(row=0, column=2)
        tk.Button(button_frame, text="Show Items", command=self.show_items, bg='#FF5722', fg='#ffffff',
                  **btn_config).grid(row=0, column=3)

        # Search entry and button
        tk.Label(button_frame, text="Search:", bg='#ffffff', font=("Helvetica", 12)).grid(row=1, column=0, padx=10,
                                                                                          pady=5, sticky="w")
        self.search_entry = tk.Entry(button_frame, width=30, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Search", command=self.search_item, bg='#FFC107', fg='#ffffff', **btn_config).grid(
            row=1, column=2, padx=5, pady=5)

        tk.Button(button_frame, text="Save", command=self.save_items, bg='#8BC34A', fg='#ffffff', **btn_config).grid(
            row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Load", command=self.load_items, bg='#3F51B5', fg='#ffffff', **btn_config).grid(
            row=2, column=1, padx=5, pady=5)

        # Frame for Treeview
        tree_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        tree_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Treeview for displaying items
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Quantity", "Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Bind Treeview selection event to on_treeview_select
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Scrollbars
        self.v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.v_scroll.set)

        self.h_scroll = tk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=self.h_scroll.set)

        # Expandable rows and columns
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def add_item(self):
        name = self.item_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if name and quantity and price:
            self.items[name] = (quantity, price)
            self.clear_entries()
            self.show_items()
            messagebox.showinfo("Info", f"Item '{name}' added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            if item_name in self.items:
                del self.items[item_name]
                self.clear_entries()
                self.show_items()
                messagebox.showinfo("Info", f"Item '{item_name}' deleted successfully!")
            else:
                messagebox.showwarning("Warning", "Item not found!")
        else:
            messagebox.showwarning("Warning", "Please select an item to delete!")

    def update_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            new_quantity = self.quantity.get()
            new_price = self.price.get()
            if new_quantity and new_price:
                if item_name in self.items:
                    self.items[item_name] = (new_quantity, new_price)
                    self.clear_entries()
                    self.show_items()
                    messagebox.showinfo("Info", f"Item '{item_name}' updated successfully!")
                else:
                    messagebox.showwarning("Warning", "Item not found!")
            else:
                messagebox.showwarning("Warning", "Please enter new quantity and price!")
        else:
            messagebox.showwarning("Warning", "Please select an item to update!")

    def show_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, (quantity, price) in self.items.items():
            self.tree.insert("", "end", values=(name, quantity, price))

    def search_item(self):
        search_term = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())

        for name, (quantity, price) in self.items.items():
            if search_term in name.lower():
                self.tree.insert("", "end", values=(name, quantity, price))

    def save_items(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.items, f)
        messagebox.showinfo("Info", "Items saved successfully!")

    def load_items(self):
        try:
            with open(self.file_path, 'r') as f:
                self.items = json.load(f)
            self.show_items()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved data found.")

    def clear_entries(self):
        self.item_name.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.price.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            quantity, price = self.items.get(item_name, ('', ''))
            self.item_name.delete(0, tk.END)
            self.item_name.insert(0, item_name)
            self.quantity.delete(0, tk.END)
            self.quantity.insert(0, quantity)
            self.price.delete(0, tk.END)
            self.price.insert(0, price)

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryApp(root)
    root.resizable(0,0)
    root.mainloop()
