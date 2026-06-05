import sys
import random

# player start data
name = input("What are you called by - ").split()[0].capitalize()
credits = 1000
current_planet = "earth"
print(f"Welcome back Captain {name}!")

cargo_hold = {
    "fuel": 3,
    "glanzend crystals": 0,
    "golden cubes": 0
}

market_prices = {
    "earth": {
        "fuel": 100,
        "glanzend crystals": 175,
        "golden cubes": 400
    },
    "mars": {
        "fuel": 200,
        "glanzend crystals": 50,
        "golden cubes": 300
    },
    "jupiter": {
        "fuel": 350,
        "glanzend crystals": 250,
        "golden cubes": 100
    }
}

planet_list = ["earth", "mars", "jupiter"]

def traveltoplanet(destination_planet):
    global current_planet
    if current_planet == destination_planet:
        print(f"You are already on {destination_planet.capitalize()}!")
        return

    fuel_cost = 0
    if (current_planet == "earth" and destination_planet == "mars" or current_planet == "mars" and destination_planet == "earth"):
        fuel_cost = 2
    elif (current_planet == "mars" and destination_planet == "jupiter" or current_planet == "jupiter" and destination_planet == "mars"):
        fuel_cost = 2
    elif (current_planet == "earth" and destination_planet == "jupiter" or current_planet == "jupiter" and destination_planet == "earth"):
        fuel_cost = 4
 
    if cargo_hold["fuel"] < fuel_cost:
        print(f"❌ NOT ENOUGH FUEL: Traveling to {destination_planet} requires {fuel_cost} Fuel.")
        print(f"You currently only have {cargo_hold['fuel']} Fuel left!")
        return

    cargo_hold["fuel"] -= fuel_cost
    current_planet = destination_planet
    print(f"YOU ARE MOVING THROUGH A WORMHOLE TO {destination_planet.upper()}")
    print(f"Consumed {fuel_cost} fuel. Remaining Fuel: {cargo_hold['fuel']}")

def buy_menu():
    global credits 

    print("\n🛒 --- LOCAL MARKET BOARD ---")
    print(f"Current Wallet: {credits} Credits")
    print(f"1. Fuel             - {market_prices[current_planet]['fuel']} Credits")
    print(f"2. Glanzend Crystals - {market_prices[current_planet]['glanzend crystals']} Credits")
    print(f"3. Golden Cubes     - {market_prices[current_planet]['golden cubes']} Credits")
    print("4. Cancel Transaction")
    
    choice = input("Select item to buy (1-4): ")
    
    item_name = ""
    if choice == "1":
        item_name = "fuel"
    elif choice == "2":
        item_name = "glanzend crystals"
    elif choice == "3":
        item_name = "golden cubes"
    elif choice == "4":
        print("Exiting market.")
        return 
    else:
        print("Invalid item choice.")
        return

    try:
        qty = int(input(f"How many units of {item_name} do you want? "))
        if qty <= 0:
            print("Quantity must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    total_cost = market_prices[current_planet][item_name] * qty
    
    if credits >= total_cost:
        credits -= total_cost
        cargo_hold[item_name] += qty
        print(f"\n✅ SUCCESS: Bought {qty}x {item_name} for {total_cost} credits.")
        print(f"Remaining Wallet: {credits} Credits")
        print(f"Current Cargo Hold: {cargo_hold}")
    else:
        print(f"\n❌ DENIED: Total cost is {total_cost} credits. You are short by {total_cost - credits} credits!")

def sell_menu():
    global credits

    print("\n💰 --- LOCAL SELLING BOARD ---")
    print(f"Credits Wallet: {credits} credits")
    print(f"1. Fuel             [ Owned: {cargo_hold['fuel']} ]  - Sells for: {market_prices[current_planet]['fuel']} Credits each")
    print(f"2. Glanzend Crystals [ Owned: {cargo_hold['glanzend crystals']} ]  - Sells for: {market_prices[current_planet]['glanzend crystals']} Credits each")
    print(f"3. Golden Cubes     [ Owned: {cargo_hold['golden cubes']} ]  - Sells for: {market_prices[current_planet]['golden cubes']} Credits each")
    print("4. Cancel Transaction")

    choice = input("choose the next action = ")

    item_name = ""
    if choice == "1":
        item_name = "fuel"
    elif choice == "2":
        item_name = "glanzend crystals"
    elif choice == "3":
        item_name = "golden cubes"
    elif choice == "4":
        print("Exiting Market")
        return
    else:
        print("Invalid choice")
        return

    try:
        qty = int(input(f"How many units of {item_name} do you want to sell? "))
        if qty <= 0:
            print("Quantity must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    if cargo_hold[item_name] >= qty:
        total_earnings = market_prices[current_planet][item_name] * qty
        cargo_hold[item_name] -= qty
        credits += total_earnings
        print(f"\n✅ SUCCESS: Sold {qty}x {item_name} for {total_earnings} credits!")
        print(f"New Wallet Balance: {credits} Credits")
    else:
        print(f"\n❌ DENIED: You don't have {qty} units of {item_name}. You only have {cargo_hold[item_name]}!")

def asteroidminer():
    global cargo_hold
    current_depth = 0
    risk_chance = 0.15
    temp_vault = {"glanzend crystals": 0, "golden cubes": 0}

    print("\n🌌 YOU HAVE ENTERED THE DENSE ASTEROID BELT! 🌌")
    print("(No Fuel Used using the latest warp tech)")

    while True:
        print(f"\n🚀 Current Depth: {current_depth}/5 | ⚠️ Crash Risk: {int(risk_chance * 100)}%")
        print(f"📦 Temporary Vault Items: {temp_vault}")
        print("Do you want to go deeper?")
        
        try:
            opt3 = int(input("1. YES (Drill Deeper)\n2. NO (Retreat and Keep Loot)\nChoose between 1 and 2 = "))
        except ValueError:
            print("⚠️ Enter a valid number choice!")
            continue

        if opt3 == 1:
            current_depth += 1
            
            if current_depth > 5:
                print("\n👑 CORE REACHED! You cannot drill any deeper. Automatic extraction initiated!")
                cargo_hold["glanzend crystals"] += temp_vault["glanzend crystals"]
                cargo_hold["golden cubes"] += temp_vault["golden cubes"]
                print(f"✅ SUCCESS: Saved items to your main cargo hold: {temp_vault}")
                return
                
            roll = random.random()
            if roll < risk_chance:
                print("\n💥 BOOM! A massive asteroid smashed through your hull!")
                print("❌ MINING FAILURE: Your temporary vault contents were vaporized!")
                
                cargo_hold["fuel"] = max(0, cargo_hold["fuel"] - 1)
                print(f"⛽ Your fuel line leaked! Lost 1 Fuel. Remaining Fuel: {cargo_hold['fuel']}")
                return
                
            print(f"\n✨ Safe transit! You successfully reached Depth {current_depth}.")
            if current_depth <= 3:
                temp_vault["glanzend crystals"] += 3
                print("💎 Mined 3x Glanzend Crystals!")
            else:
                temp_vault["golden cubes"] += 2
                print("🟨 Rare discovery! Mined 2x Golden Cubes!")
                
            risk_chance += 0.20

        elif opt3 == 2:
            if current_depth == 0:
                print("\nYou left the asteroid belt without drilling anything.")
                return
                
            cargo_hold["glanzend crystals"] += temp_vault["glanzend crystals"]
            cargo_hold["golden cubes"] += temp_vault["golden cubes"]
            
            print("\n🔒 Engaged engine reverse thrusters! Escaping field safely...")
            print(f"✅ SUCCESS: Loaded {temp_vault} safely into your main ship cargo hold.")
            return
            
        else:
            print("❌ Invalid Choice! Enter 1 or 2.")

# main loop
while True:
    print(f"\n📍 CURRENT LOCATION: {current_planet.upper()}")
    print(f"💵 CREDITS: {credits} | ⛽ FUEL: {cargo_hold['fuel']}")
    print("What will you do?")
    print("1. Travel\n2. Buy\n3. Sell\n4. Exit Game")
    
    try:
        opt1 = int(input("choose between 1,2,3,4 = "))
    except ValueError:
        print("WRONG INPUT")
        continue

    if opt1 == 1:
        print("\nchoose which Zone do you want to travel to")
        print("1. Earth\n2. Mars\n3. Jupiter\n4. Asteriod Belt\n5. Go Back")
        while True:
            try:
                opt2 = int(input("choose between 1-5 to travel between Zones = "))
            except ValueError:
                print("WRONG INPUT")
                continue

            if opt2 == 1:
                traveltoplanet("earth")
                break
            elif opt2 == 2:
                traveltoplanet("mars")
                break
            elif opt2 == 3:
                traveltoplanet("jupiter")
                break
            elif opt2 == 4:
                asteroidminer()
                break
            elif opt2 == 5:
                break
            else:
                print("WRONG INPUT")
        
    elif opt1 == 2:
        buy_menu()
    elif opt1 == 3:
        sell_menu()
    elif opt1 == 4:
        print("Exiting ship system. Goodbye Captain!")
        sys.exit()
    else:
        print("WRONG INPUT")
