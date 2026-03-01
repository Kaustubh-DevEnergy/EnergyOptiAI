# --- STEP 1: IDENTIFY USER ---
print("Welcome to the Smart Energy & Heat Optimizer (SEHO)")
print("----------------------------------------------------")

user_type = input("Are you a (1) Personal Consumer or (2) Enterprise/Consultant? ")

if user_type == "1":
    print("\n--- PERSONAL CONSUMER MODE ---")
    knows_load = input("Do you already have your hourly load profile? (yes/no): ")
    
    if knows_load.lower() == "no":
        print("No problem! We will create one based on your bills.")
        # This is where we will add Step 3: The Bill Detective
    else:
        print("Great! Please upload your .csv load data.")

elif user_type == "2":
    print("\n--- ENTERPRISE / CONSULTANT MODE ---")
    # Step 2: Expert inputs
    peak_load = input("Enter your annual peak demand in kW: ")
    print(f"Targeting optimization for {peak_load}kW system...")

else:
    print("Invalid input. Please restart and choose 1 or 2.")
