# ⚡ EnergySelectionAI
### *Spatially-Explicit Residential Energy Optimizer & Digital Twin*

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PyPSA](https://img.shields.io/badge/PyPSA-Optimization-blue?style=for-the-badge)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

---

### ⚠️ Project Status: Under Development
> **Note:** This project is a work in progress. I am constantly updating the logic and adding new features as I find new inspiration and engineering ideas to integrate. Thank you for visiting!

---

## 🌟 Overview
**EnergySelectionAI** is a full-stack energy modeling application designed to bridge the gap between GIS weather data and residential energy strategy. By leveraging the power of **Atlite** for climate data and **PyPSA** for mathematical optimization, the tool calculates the most cost-effective way to manage a home's energy "microgrid."

It focuses on **Sector Coupling**: the intelligent synchronization of solar generation, battery storage, electric vehicle (EV) charging, and heat pump thermal demand.

---

## 🚀 Key Features
* **🌍 GIS-Integrated Weather Engine:** Automatically retrieves and processes ERA5 (Copernicus) satellite data based on specific GPS coordinates.
* **🤖 ML-Driven Performance:** Uses **Scikit-Learn (Linear Regression)** to predict real-time Heat Pump COP based on ambient temperature curves.
* **⚖️ Linear Programming Optimizer:** Utilizes the **HiGHS solver** via **PyPSA** to determine the optimal hourly dispatch of energy for a 24-hour horizon.
* **🏠 Dynamic Load Modeling:** Simulates household demand based on German building standards (e.g., **KfW 40/55**), resident count, and lifestyle habits.
* **📊 Automated Financials:** Calculates Self-Sufficiency Rates (SSR), annual cost savings in Euros, and CO2 mitigation metrics.

---

## 🛠️ Technical Stack
| Category | Tools |
| :--- | :--- |
| **Language** | Python 3.x |
| **Data Science** | Pandas, NumPy, Xarray (NetCDF processing) |
| **Energy Modeling** | PyPSA, Atlite |
| **Machine Learning** | Scikit-Learn |
| **Frontend** | Streamlit |
| **Optimization** | HiGHS Solver |

---

## 📂 Project Structure
* `app.py`: The main Streamlit application containing the UI and the optimization logic.
* `requirements.txt`: List of dependencies required to run the environment.
* `.gitignore`: Configured to exclude heavy weather data files (`.nc`) and local caches.

---

## 📈 Roadmap (Upcoming Ideas)
- [ ] **Smart EV Integration:** Moving from static charging to "Solar-Following" EV charging logic.
- [ ] **8760-Hour Simulation:** Expanding from a 24-hour snapshot to a full-year seasonal analysis.
- [ ] **ROI Module:** Adding a detailed investment vs. payback period calculator.
- [ ] **PostgreSQL Backend:** Transitioning session data to a time-series database.

---

## 🤝 Contact & Visit
If you have any questions about the engineering logic or would like to discuss the project:

* **Author:** Kaustubh Jagtap
* **Location:** Ingolstadt, Germany 🇩🇪
* **Focus:** *Developed with a passion for the German Energiewende.*
