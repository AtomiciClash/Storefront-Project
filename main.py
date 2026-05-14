import sys
import re
import time
import threading
import os
from datetime import datetime

def show_splash():
    try:
        import tkinter as tk
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
                splash.after(400, splash.destroy)

        animate()
        splash.mainloop()
    except Exception:
        pass

os.environ.setdefault("DISPLAY", ":0")
splash_thread = threading.Thread(target=show_splash, daemon=True)
splash_thread.start()
splash_thread.join(timeout=3)



shopItems = {}
# Dictionary of items and their quantities


# ------------------------------------------------------------------------------------------------------------------------------
with open("database.txt", "r") as file:
    for line in file:
        if ":" in line:
            parts = line.strip().split(":")
            name = parts[0].strip()
            quantity = int(parts[1].strip())

            price = float(parts[2].strip())

            shopItems[name] = {"quantity": quantity, "price": price}


# ------------------------------------------------------------------------------------------------------------------------------
def save_data():
    with open("database.txt", "w") as file:
        for name, data in shopItems.items():
            file.write(f"{name}: {data['quantity']}: {data['price']}\n")


# ------------------------------------------------------------------------------------------------------------------------------
class TryBlocks:
    def __init__(self):
        pass

    def integerTry(self):
        while True:
            try:
                return int(input())
            except ValueError:
                print("\033c", end="")
                print("Error: Please enter a valid number.")

    def strTry(self):
        while True:
            try:
                return str(input())
            except ValueError:
                print("\033c", end="")
                print("Error: Please enter a valid plane.")


tryBlocks = TryBlocks()
# ------------------------------------------------------------------------------------------------------------------------------


class LogSaver:
    def __init__(self, filename):
        self.filename = filename

    def writeLog(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safeMessage = message.replace("\033c", "").replace("$", "")
        with open(self.filename, "a") as file:
            file.write(f"[{timestamp}]: {safeMessage}" + "\n")
            file.flush()

    def adminAdd(self, reqQuantity, reqItem):
        logEntry = f"Admin ADDED {reqQuantity} {reqItem}s to inventory"
        self.writeLog(logEntry)

    def adminRemove(self, reqQuantity, reqItem):
        logEntry = f"Admin REMOVED {reqQuantity} {reqItem}s from inventory"
        self.writeLog(logEntry)

    def userPurchase(self, userBuyQuantity, userBuy, taxedPrice):
        taxedPrice = f"{(taxedPrice):,.2f}"
        logEntry = f"User PURCHASED {userBuyQuantity} {userBuy}s for {taxedPrice} USD"
        self.writeLog(logEntry)


logger = LogSaver("logs.txt")
# ------------------------------------------------------------------------------------------------------------------------------


def main_menu():
    while True:
        print(
            "Type 1 to add. Type 2 to remove. Type 3 to see inventory. Type 4 to exit."
        )
        choice = tryBlocks.integerTry()
        if choice == 1:
            print("\033c", end="")
            print("What would you like to add to?")
            reqItem = tryBlocks.strTry()
            if reqItem in shopItems:
                print(f"How many {reqItem}s would you like to add?")
                reqQuantity = tryBlocks.integerTry()
                shopItems[reqItem]["quantity"] += int(reqQuantity)

                print(f"Added {reqQuantity} {reqItem}s to inventory.")
                save_data()
                logger.adminAdd(reqQuantity, reqItem)
                input("\nPress Enter to return to the menu...")
            else:
                print("Invalid plane name.")

        elif choice == 2:
            print("\033c", end="")
            print("What would you like to remove from?")
            reqItem = tryBlocks.strTry()
            if reqItem in shopItems:
                print(f"How many {reqItem}s would you like to remove?")
                reqQuantity = tryBlocks.integerTry()
                shopItems[reqItem]["quantity"] -= int(reqQuantity)

                print(f"Removed {reqQuantity} {reqItem}s from inventory.")
                save_data()
                logger.adminRemove(reqQuantity, reqItem)
                input("\nPress Enter to return to the menu...")

        elif choice == 3:
            print("\033c", end="")
            print("Current Inventory:\n------------------------")
            for name, data in shopItems.items():
                formattedPrice = f"${data['price']:,.2f}"
                print(f"{name}: {data['quantity']} units | Price: {formattedPrice}")
            print("------------------------")

        elif choice == 4:
            print("Exiting...")
            save_data()
            sys.exit()

        else:
            print("Select something from the menu chud")


# ------------------------------------------------------------------------------------------------------------------------------
def user_menu():
    print("\033c", end="")
    print("Welcome to the User Menu")

    while True:
        print("\033c", end="")
        print("Current Inventory:\n------------------------")
        for name, data in shopItems.items():
            formattedPrice = f"${data['price']:,.2f}"
            print(f"{name}: {data['quantity']} units | Price: {formattedPrice}")
        print("------------------------")
        print("Press 1 to buy. Press 2 to exit.")
        userChoice = int(input())
        if userChoice == 1:
            print("\033c", end="")
            for name, data in shopItems.items():
                formattedPrice = f"${data['price']:,.2f}"
                print(f"{name}: {data['quantity']} units | Price: {formattedPrice}")
            print("------------------------")

            print("What would you like to buy?")
            userBuy = tryBlocks.strTry()
            if userBuy in shopItems:
                print(f"How many {userBuy}s would you like to buy?")
                userBuyQuantity = tryBlocks.integerTry()
                if userBuyQuantity <= shopItems[userBuy]["quantity"]:
                    taxedPrice = shopItems[userBuy]["price"] * userBuyQuantity * 1.07
                    formattedPrice = f"${taxedPrice:,.2f}"
                    print("\033c", end="")
                    print(
                        f"You are going to buy {userBuyQuantity} {userBuy}s. The total price is {formattedPrice}."
                    )
                    print("Press 1 to confirm. Press 2 to cancel.")
                    userConfirm = tryBlocks.integerTry()
                    if userConfirm == 1:
                        shopItems[userBuy]["quantity"] -= userBuyQuantity
                        print(
                            f"You have bought {userBuyQuantity} {userBuy}s. Thank you for your purchase!"
                        )
                        save_data()
                        logger.userPurchase(userBuyQuantity, userBuy, taxedPrice)
                        input("\nPress Enter to return to the menu...")
                    elif userConfirm == 2:
                        print("\033c", end="")
                        print("Purchase cancelled.")
                else:
                    print("\033c", end="")
                    print(f"Sorry, there are not enough {userBuy}s in stock.")
            else:
                print("\033c", end="")
                print("Invalid plane name.")
        elif userChoice == 2:
            print("\033c", end="")
            print("Exiting...")
            break


# ------------------------------------------------------------------------------------------------------------------------------

while True:
    print("\033c", end="")
    print("Welcome to Paul's Plane Shop!")
    print("Press 1 for User Mode. Press 2 for Admin Mode. Press 3 to exit.")
    passChoice = tryBlocks.integerTry()
    if passChoice == 1:
        print("\033c", end="")
        user_menu()
    elif passChoice == 2:
        print("\033c", end="")
        print("Enter Password:")
        password = "yuhui"
        userpass = tryBlocks.strTry()
        if userpass == password:
            print("\033c", end="")
            print("Welcome, User")
            main_menu()
            break
        else:
            print("\033c", end="")
            print("Invalid Password, Please try again:")
            userpass = tryBlocks.strTry()
            print("\033c", end="")

    elif passChoice == 3:
        print("\033c", end="")
        print("Exiting...")
        break

