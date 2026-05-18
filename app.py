import sys
import re
import time
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATA INITIALIZATION ---
shopItems = {}

if not os.path.exists("database.txt"):
    with open("database.txt", "w") as f:
        f.write("Boeing 747: 10: 120000000.00\nAirbus A320: 15: 90000000.00\n")

with open("database.txt", "r") as file:
    for line in file:
        if ":" in line:
            parts = line.strip().split(":")
            name = parts[0].strip()
            quantity = int(parts[1].strip())
            price = float(parts[2].strip())
            shopItems[name] = {"quantity": quantity, "price": price}

def save_data():
    with open("database.txt", "w") as file:
        for name, data in shopItems.items():
            file.write(f"{name}: {data['quantity']}: {data['price']}\n")

# --- LOGGING SYSTEM ---
class LogSaver:
    def __init__(self, filename):
        self.filename = filename

    def writeLog(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safeMessage = message.replace("\033c", "").replace("$", "")
        with open(self.filename, "a") as file:
            file.write(f"[{timestamp}]: {safeMessage}\n")

    def adminAdd(self, reqQuantity, reqItem):
        self.writeLog(f"Admin ADDED {reqQuantity} {reqItem}s to inventory")

    def adminRemove(self, reqQuantity, reqItem):
        self.writeLog(f"Admin REMOVED {reqQuantity} {reqItem}s from inventory")

    def userPurchase(self, userBuyQuantity, userBuy, taxedPrice):
        formatted = f"{taxedPrice:,.2f}"
        self.writeLog(f"User PURCHASED {userBuyQuantity} {userBuy}s for {formatted} USD")

logger = LogSaver("logs.txt")

# --- MAIN GUI APPLICATION ---
class PlaneShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paul's Plane Shop - Inventory Management")
        self.root.geometry("650x500")

        header = tk.Label(root, text="✈ Paul's Plane Shop System", font=("Helvetica", 16, "bold"))
        header.pack(pady=10)

        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(pady=10, fill="x", padx=20)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Quantity", "Price"), show="headings", height=8)
        self.tree.heading("Quantity", text="Quantity Available")
        self.tree.heading("Price", text="Unit Price (USD)")
        self.tree.pack(side="left", fill="x", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=15, fill="both", expand=True, padx=20)

        self.setup_admin_tab()
        self.setup_user_tab()
        self.update_inventory_display()

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def update_inventory_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        plane_list = list(shopItems.keys())
        self.admin_combo['values'] = plane_list
        self.user_combo['values'] = plane_list

        for name, data in shopItems.items():
            formatted_price = f"${data['price']:,.2f}"
            self.tree.insert("", "end", iid=name, text=name, values=(data['quantity'], formatted_price))

    def setup_admin_tab(self):
        admin_frame = tk.Frame(self.notebook)
        self.notebook.add(admin_frame, text=" Admin Controls ")

        tk.Label(admin_frame, text="Select Plane:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.admin_combo = ttk.Combobox(admin_frame, state="readonly", width=25)
        self.admin_combo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(admin_frame, text="Quantity Amount:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.admin_qty_entry = tk.Entry(admin_frame, width=27)
        self.admin_qty_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(admin_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Add To Stock", bg="#4caf50", fg="white", padx=10, command=self.admin_add).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Remove From Stock", bg="#f44336", fg="white", padx=10, command=self.admin_remove).pack(side="left", padx=10)

    def setup_user_tab(self):
        user_frame = tk.Frame(self.notebook)
        self.notebook.add(user_frame, text=" User Storefront ")

        tk.Label(user_frame, text="Choose Plane to Buy:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.user_combo = ttk.Combobox(user_frame, state="readonly", width=25)
        self.user_combo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(user_frame, text="Purchase Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.user_qty_entry = tk.Entry(user_frame, width=27)
        self.user_qty_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(user_frame, text="Purchase Items", bg="#2196f3", fg="black", padx=20, command=self.user_purchase).grid(row=2, column=0, columnspan=2, pady=15)

    def get_inputs(self, combo, entry):
        item = combo.get()
        if not item:
            messagebox.showerror("Error", "Please select a valid plane.")
            return None, None
        try:
            qty = int(entry.get())
            if qty <= 0:
                raise ValueError()
            return item, qty
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid, positive whole number.")
            return None, None

    def admin_add(self):
        item, qty = self.get_inputs(self.admin_combo, self.admin_qty_entry)
        if item and qty:
            shopItems[item]["quantity"] += qty
            save_data()
            logger.adminAdd(qty, item)
            self.update_inventory_display()
            self.admin_qty_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added {qty} units to {item}!")

    def admin_remove(self):
        item, qty = self.get_inputs(self.admin_combo, self.admin_qty_entry)
        if item and qty:
            if qty > shopItems[item]["quantity"]:
                messagebox.showerror("Error", f"Cannot remove {qty} units. Only {shopItems[item]['quantity']} exist.")
                return
            shopItems[item]["quantity"] -= qty
            save_data()
            logger.adminRemove(qty, item)
            self.update_inventory_display()
            self.admin_qty_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Removed {qty} units from {item}!")

    def user_purchase(self):
        item, qty = self.get_inputs(self.user_combo, self.user_qty_entry)
        if item and qty:
            available = shopItems[item]["quantity"]
            if qty > available:
                messagebox.showerror("Shortage", f"We cannot fulfill this request. Only {available} items are left.")
                return

            raw_cost = shopItems[item]["price"] * qty
            taxed_price = raw_cost * 1.07
            formatted_total = f"${taxed_price:,.2f}"

            confirm = messagebox.askyesno(
                "Confirm Purchase", 
                f"You are buying {qty} {item}(s).\nTotal Price (incl. 7% Tax): {formatted_total}\n\nProceed?"
            )

            if confirm:
                shopItems[item]["quantity"] -= qty
                save_data()
                logger.userPurchase(qty, item, taxed_price)
                self.update_inventory_display()
                self.user_qty_entry.delete(0, tk.END)
                messagebox.showinfo("Receipt", f"Purchase completed successfully for {formatted_total}!")

    def on_exit(self):
        save_data()
        self.root.destroy()

# --- SEQUENTIAL RUNNER (MAC SAFE) ---
def run_application():
    # 1. Create Splash Window
    splash = tk.Tk()
    splash.title("Paul's Plane Shop")
    splash.geometry("400x220")
    splash.resizable(False, False)
    splash.configure(bg="#1a1a2e")
    splash.overrideredirect(True)

    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w // 2) - 200
    y = (screen_h // 2) - 110
    splash.geometry(f"400x220+{x}+{y}")

    tk.Label(splash, text="✈  Paul's Plane Shop", font=("Helvetica", 20, "bold"),
             bg="#1a1a2e", fg="#e0e0e0").pack(pady=35)
    tk.Label(splash, text="Loading inventory...", font=("Helvetica", 11),
             bg="#1a1a2e", fg="#a0a0c0").pack()

    bar_frame = tk.Frame(splash, bg="#1a1a2e")
    bar_frame.pack(pady=20)
    canvas = tk.Canvas(bar_frame, width=300, height=16, bg="#2e2e4e", highlightthickness=0)
    canvas.pack()
    bar = canvas.create_rectangle(0, 0, 0, 16, fill="#5c7cfa", outline="")

    def animate(step=0):
        width = int((step / 30) * 300)
        canvas.coords(bar, 0, 0, width, 16)
        if step < 30:
            splash.after(50, animate, step + 1)
        else:
            # Clear splash and launch main app frame sequentially
            splash.destroy()
            launch_main_app()

    animate()
    splash.mainloop()

def launch_main_app():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    app = PlaneShopApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_application()
