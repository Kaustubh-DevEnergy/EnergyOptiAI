import streamlit as st
import pandas as pd
import numpy as np
import pypsa
import atlite
from sklearn.linear_model import LinearRegression
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="EnergySelectionAI", page_icon="⚡", layout="wide")

BUILDING_STANDARDS = {
    "Altbau (Unrenovated)": 200,
    "Bestand (Modernized)": 100,
    "KfW 55 (New Build)": 55,
    "KfW 40 (Passive/High Efficiency)": 40
}

# --- 2. SIDEBAR INPUTS ---
if st.sidebar.button("(Clear Cache)", key="clear_cache_btn"):
    st.session_state.clear()
    st.rerun()

st.sidebar.header("📍 1. Geographic Location")
lat = st.sidebar.number_input("Latitude", value=48.7667, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=11.4250, format="%.4f")

st.sidebar.header("🏠 2. Building Infrastructure")
house_type = st.sidebar.selectbox("Building Age", list(BUILDING_STANDARDS.keys()))
living_area = st.sidebar.number_input("Living Area (m²)", min_value=1, value=120)
roof_space = st.sidebar.number_input("Roof for PV (m²)", min_value=0, value=40)

st.sidebar.header("👤 3. Human Lifestyle")
num_people = st.sidebar.slider("Residents", 1, 6, 3)
has_ev = st.sidebar.checkbox("Electric Vehicle (EV)?")
cook_at_home = st.sidebar.checkbox("Daily Home Cooking?", value=True)

st.sidebar.header("🔋 4. Energy Storage")
battery_capacity = st.sidebar.slider("Battery Size (kWh)", 0, 20, 5)

# --- 3. PRELIMINARY ESTIMATES ---
st.title("⚡ EnergySelectionAI")
st.markdown("#### Spatially-Explicit Residential Energy Optimizer")
st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=13)

thermal_demand = BUILDING_STANDARDS[house_type] * living_area
pv_capacity = (int(roof_space / 1.7) * 0.4) if roof_space > 0 else 0.1
base_load_est = 1200 + (num_people * 500)

col1, col2, col3 = st.columns(3)
col1.metric("Annual Heat Demand", f"{thermal_demand:,} kWh_th")
col2.metric("Potential PV Capacity", f"{pv_capacity:.2f} kWp")
col3.metric("Est. Base Load", f"{base_load_est:,} kWh_el")

# --- 4. DATA PROCESSING (Atlite & Scikit-Learn) ---
if st.button("🚀 Generate Energy Forecast", use_container_width=True):
    with st.spinner("🌍 Fetching GIS Weather Data & Modeling Systems..."):
        try:
            # 4.1 Weather Retrieval (Atlite)
            cutout_filename = "weather_prod.nc"
            if not os.path.exists(cutout_filename):
                cutout = atlite.Cutout(path=cutout_filename, module="era5",
                                      bounds=[lon-0.5, lat-0.5, lon+0.5, lat+0.5], 
                                      time="2023-05-01")
                cutout.prepare(features=["influx", "temperature"])
            else:
                cutout = atlite.Cutout(path=cutout_filename)

            # 4.2 Solar Profile Processing
            pv_raw = cutout.pv(panel="CSi", orientation={'slope': 30, 'azimuth': 180}, capacity_factor=True)
            pv_profile = pv_raw.mean(dim=["x", "y"]).values.flatten()[:24]
            # Night-time mask (Safety alignment)
            sun_mask = np.zeros(24)
            sun_mask[6:20] = 1.0 
            pv_profile = pv_profile * sun_mask

            # 4.3 Heat Pump COP Modeling (Linear Regression)
            temp_raw = cutout.temperature().mean(dim=["x", "y"])
            avg_temp_c = float(temp_raw.mean()) - 273.15
            if avg_temp_c < -5: avg_temp_c = 14.0 # Baseline for Spring
            
            X_train = np.array([[-15], [-5], [2], [10], [20]])
            y_train = np.array([1.8, 2.4, 3.1, 4.0, 5.2])
            cop_model = LinearRegression().fit(X_train, y_train)
            safe_cop = float(cop_model.predict([[avg_temp_c]]))

            # 4.4 Load Profile Generation
            # Base load + Thermal load distributed hourly
            hourly_base = (num_people * 0.12) + (thermal_demand / safe_cop / 8760)
            daily_load = np.full(24, hourly_base)
            
            if cook_at_home:
                daily_load[7:9] += 0.8  # Breakfast
                daily_load[18:20] += 2.0 # Dinner
            if has_ev:
                daily_load[1:6] += 2.5 # Night charging

            st.session_state.update({
                'forecast_ready': True, 
                'pv_profile': pv_profile, 
                'cop': safe_cop, 
                'pv_cap': pv_capacity, 
                'daily_load': daily_load
            })
            st.success("☀️ Forecast Ready!")

        except Exception as e:
            st.error(f"Logic Error during data processing: {e}")

# --- 5. SYSTEM OPTIMIZATION (PyPSA) ---
if 'forecast_ready' in st.session_state:
    n = pypsa.Network()
    snapshots = pd.date_range("2023-05-01 00:00", periods=24, freq="H")
    n.set_snapshots(snapshots)
    n.add("Bus", "Home_Bus")

    # Mapping Data to Series
    pv_series = pd.Series(st.session_state['pv_profile'], index=snapshots)
    load_series = pd.Series(st.session_state['daily_load'], index=snapshots)

    # 5.1 Supply & Grid
    n.add("Generator", "Solar_PV", bus="Home_Bus", 
          p_nom=st.session_state['pv_cap'], 
          p_max_pu=pv_series)
    
    n.add("Generator", "Utility_Grid", bus="Home_Bus", 
          p_nom=100, 
          marginal_cost=0.40) # €/kWh cost

    # 5.2 Storage
    if battery_capacity > 0:
        n.add("Store", "Home_Battery", bus="Home_Bus", 
              e_nom=battery_capacity, 
              e_initial=battery_capacity * 0.5, 
              e_cyclic=True,
              marginal_cost=0.01) # Prefers battery over grid

    # 5.3 Demand
    n.add("Load", "Household_Demand", bus="Home_Bus", p_set=load_series)

    # Solve
    n.optimize(solver_name='highs')

    # --- 6. RESULTS DASHBOARD ---
    st.divider()
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.subheader("Hourly Dispatch Strategy")
        res_plot = pd.DataFrame(index=snapshots)
        res_plot["Solar (Direct)"] = n.generators_t.p["Solar_PV"]
        res_plot["Grid Purchase"] = n.generators_t.p["Utility_Grid"]
        res_plot["Household Demand"] = load_series
        if battery_capacity > 0:
            res_plot["Battery Help"] = n.stores_t.p["Home_Battery"].clip(lower=0)
        
        st.area_chart(res_plot)
        
        if battery_capacity > 0:
            st.subheader("Battery State of Charge (%)")
            soc = (n.stores_t.e["Home_Battery"] / battery_capacity) * 100
            st.line_chart(soc)

    with c_right:
        st.subheader("System Performance")
        sol_gen = n.generators_t.p["Solar_PV"].sum()
        total_load = load_series.sum()
        self_suff = (sol_gen / total_load * 100) if total_load > 0 else 0
        
        st.metric("Self-Sufficiency Rate", f"{self_suff:.1f}%")
        st.metric("Calculated COP", f"{st.session_state['cop']:.2f}")
        
        # Financials
        annual_load = total_load * 365
        savings = (annual_load * (self_suff / 100)) * 0.40
        st.divider()
        st.metric("Annual Savings", f"€{savings:,.2f}")
        st.caption("Based on €0.40/kWh grid price")
        
        co2 = (annual_load * (self_suff / 100)) * 0.4
        st.metric("CO2 Mitigation", f"{co2:.1f} kg/year")
