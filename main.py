import sys
import re
import time
from datetime import datetime

def show_loader():
    bar_length = 30
    print("\033c", end="")
    print("=" * 42)
    print("        ✈   Paul's Plane Shop   ✈")
    print("=" * 42)
    print("\n  Loading inventory...\n")
    for i in range(bar_length + 1):
        filled = "█" * i
        empty = "░" * (bar_length - i)
        percent = int((i / bar_length) * 100)
        print(f"  [{filled}{empty}] {percent}%", end="\r")
        time.sleep(0.04)
    print(f"  [{'█' * bar_length}] 100%")
    time.sleep(0.3)

show_loader()



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

