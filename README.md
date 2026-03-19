⚡ EnergySelectionAI
Spatially-Explicit Residential Energy Optimizer & Digital Twin
⚠️ Project Status: Under Development > Thank you for taking the time to visit! This project is a work in progress. I am constantly updating the logic and adding new features as I find new inspiration and engineering ideas to integrate.

🌟 Overview
EnergySelectionAI is a full-stack energy modeling application designed to bridge the gap between GIS weather data and residential energy strategy. By leveraging the power of Atlite for climate data and PyPSA for mathematical optimization, the tool calculates the most cost-effective way to manage a home's energy "microgrid."

It focuses on Sector Coupling: the intelligent synchronization of solar generation, battery storage, electric vehicle (EV) charging, and heat pump thermal demand.

🚀 Key Features
GIS-Integrated Weather Engine: Automatically retrieves and processes ERA5 (Copernicus) satellite data based on specific GPS coordinates.

ML-Driven Performance: Uses Scikit-Learn (Linear Regression) to predict real-time Heat Pump COP based on ambient temperature curves.

Linear Programming Optimizer: Utilizes the HiGHS solver via PyPSA to determine the optimal hourly dispatch of energy for a 24-hour horizon.

Dynamic Load Modeling: Simulates household demand based on building standards (e.g., KfW 40/55), resident count, and lifestyle habits (cooking/EV charging).

Automated Financials: Calculates Self-Sufficiency Rates (SSR), annual cost savings in Euros, and CO2 mitigation metrics.

🛠️ Technical Stack
Language: Python 3.x

Data Science: Pandas, NumPy, Xarray (for NetCDF weather files)

Energy Modeling: PyPSA (Python for Power System Analysis), Atlite

Machine Learning: Scikit-Learn

Frontend: Streamlit

Optimization Solver: HiGHS

📂 Project Structure
app.py: The main Streamlit application containing the UI and the optimization logic.

requirements.txt: List of dependencies required to run the environment.

.gitignore: Configured to exclude heavy weather data files (.nc) and local caches.

📈 Roadmap (Upcoming Ideas)
[ ] Smart EV Integration: Moving from static charging to "Solar-Following" EV charging logic.

[ ] 8760-Hour Simulation: Expanding from a 24-hour snapshot to a full-year seasonal analysis.

[ ] ROI Module: Adding a detailed investment vs. payback period calculator.

[ ] PostgreSQL Backend: Transitioning session data to a time-series database for historical performance tracking.

🤝 Contact & Visit
If you have any questions about the engineering logic or would like to discuss the project:

Author: Kaustubh Jagtap

Location: Ingolstadt

Developed with a passion for the German Energiewende.
