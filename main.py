import sys
from datetime import datetime
shopItems = {}
#Dictionary of items and their quantities
with open("database.txt", "r") as file:
    for line in file:
        if ":" in line:
            parts = line.strip().split(":")
            name = parts[0].strip()
            quantity = int(parts[1].strip())

            price = float(parts[2].strip()) if len(parts) > 2 else 0.0

            # This creates the nested dictionary
            shopItems[name] = {"quantity": quantity, "price": price}
def save_data():
    with open("database.txt", "w") as file:
        for name, data in shopItems.items():
            file.write(f"{name}: {data['quantity']}: {data['price']}\n")

#------------------------------------------------------------------------------------------------------------------------------

class LogSaver:
    def __init__(self, filename):
        self.filename = "logs.txt"
        self.logs = []
    def adminAdd(self, quantity, name):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {quantity} {name} have been added\n"
        with open(self.filename, "a") as file:
            file.write(message)
                
    def adminRemove(self, quantity, name):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {quantity} {name} have been removed\n"
        with open(self.filename, "a") as file:
            file.write(message)
                
    def userPurchase(self, userBuyQuantity, userBuy, formattedPrice):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}]: {userBuyQuantity} {name} have been purchased for {formattedPrice}\n"
        with open(self.filename, "a") as file:
            file.write(message)
            
logger = LogSaver("logs.txt")
#------------------------------------------------------------------------------------------------------------------------------

def main_menu():
    # Basically loop forever

    while True:
        choice = int(input("Type 1 to add. Type 2 to remove. Type 3 to see inventory. Type 4 to exit. \n"))

        if choice == 1:
            print("\033c", end="")
            reqItem = input("What would you like to add to?\n")
            if reqItem in shopItems:
                reqQuantity = input(f"How many {reqItem}s to add?\n")
                shopItems[reqItem]["quantity"] += int(reqQuantity) 
                print("\033c", end="")
                print(f"Added {reqQuantity} {reqItem}s to inventory.")
                save_data()
                logger.adminAdd(reqQuantity, reqItem)
            else:
                print("Invalid plane name.")

        elif choice == 2:
            print("\033c", end="")
            reqItem = input("What would you like to remove from?\n")
            if reqItem in shopItems:
                reqQuantity = input(f"How many {reqItem}s to remove?\n")
                shopItems[reqItem]["quantity"] -= int(reqQuantity)
                print("\033c", end="")
                print(f"Removed {reqQuantity} {reqItem}s from inventory.")
                save_data()
                logger.adminRemove(reqQuantity, reqItem)

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
#------------------------------------------------------------------------------------------------------------------------------
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
            print("What would you like to buy?")
            userBuy = input()
            if userBuy in shopItems:
                print(f"How many {userBuy}s would you like to buy?")
                userBuyQuantity = int(input())
                if userBuyQuantity <= shopItems[userBuy]["quantity"]:
                    taxedPrice = shopItems[userBuy]["price"] * userBuyQuantity * 1.07
                    formattedPrice = f"${taxedPrice:,.2f}"
                    print("\033c", end="")
                    print(f"You are going to buy {userBuyQuantity} {userBuy}s. The total price is {formattedPrice}.\n")
                    print("Press 1 to confirm. Press 2 to cancel.")
                    userConfirm = int(input())
                    if userConfirm == 1:
                        shopItems[userBuy]["quantity"] -= userBuyQuantity
                        print("\033c", end="")
                        print(f"You have bought {userBuyQuantity} {userBuy}s. Thank you for your purchase!")
                        save_data()
                    if userConfirm == 2:
                        print("\033c", end="")
                        print("Purchase cancelled.")
                else:
                    print("\033c", end="")
                    print(f"Sorry, there are not enough {userBuy}s in stock.")
        if userChoice == 2:
            print("\033c", end="")
            print("Exiting...")
            break
#------------------------------------------------------------------------------------------------------------------------------
# Tells python to run main_menu()
while True:
    print("\033c", end="")
    print ("Welcome to Paul's Plane Shop!")
    print("Press 1 for User Mode. Press 2 for Admin Mode. Press 3 to exit.")
    passChoice = int(input())
    if passChoice == 1:
        print("\033c", end="")
        """
        print ("The User Mode is currently WIP come back later.")
        print ("Press 3 to return to the main menu. Press 4 to exit.")
        returnChoice = int(input())
        if returnChoice == 3:
            pass
        if returnChoice == 4:
            print("\033c", end="")
            print("Exiting...")
            break
            """
        user_menu()
    elif passChoice == 2:
        print("\033c", end="")
        print("Enter Password:")
        password = "yuhui"
        userpass = input()
        while True:
            if userpass == password:
                print("\033c", end="")
                print("Welcome, User")
                main_menu()
                break
            else:
                print("\033c", end="")
                print("Invalid Password, Please try again:")
                userpass = input()
                print("\033c", end="")

    elif passChoice == 3:
         print("\033c", end="")
         print("Exiting...")
         break
    



