# --- SETTINGS (2026 Germany) ---
ELEC_PRICE = 0.348  # €/kWh
GAS_PRICE = 0.096   # €/kWh
COP_AVG = 3.5       # Heat Pump Efficiency

def run_assessment():
    print("--- EquipmentSelectionAI: Step 1 & 2 ---")
    user_type = input("Are you a (1) Homeowner or (2) Consultant? ")

    if user_type == "1":
        # Step 2: Homeowner Path
        bill_eur = float(input("Avg. monthly electricity bill in EUR? "))
        annual_elec = (bill_eur / ELEC_PRICE) * 12
        
        has_gas = input("Do you heat with Gas? (y/n): ")
        if has_gas.lower() == 'y':
            annual_gas = float(input("Annual Gas consumption (kWh): "))
            # MECHANICAL LOGIC: Convert Gas to Heat Pump Electricity
            hp_elec_demand = (annual_gas * 0.9) / COP_AVG
            print(f"\n[AI Insight] Your total future electric load: {annual_elec + hp_elec_demand:.0f} kWh/year")
            print(f"[AI Insight] Savings by switching to Heat Pump: €{ (annual_gas * GAS_PRICE) - (hp_elec_demand * ELEC_PRICE) :.2f} /year")

    elif user_type == "2":
        # Step 2: Expert Path
        peak_kw = float(input("Enter peak load demand (kW): "))
        print(f"Optimizing industrial sizing for {peak_kw}kW peak...")

if __name__ == "__main__":
    run_assessment()
