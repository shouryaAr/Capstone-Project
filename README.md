# Bluestock Mutual Fund Analytics Platform

![Python](https://img.shields.io/badge/Python-3-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458)
![Plotly](https://img.shields.io/badge/Plotly-Visualizations-3F4F75)

🌐 **Live Web Application:** [bluestock-capstone-project-sa.streamlit.app](https://bluestock-capstone-project-sa.streamlit.app/)

## 📌 Project Overview
The **Bluestock Mutual Fund Analytics Platform** is an end-to-end data engineering and quantitative analytics capstone project. It ingests, cleans, and models large-scale mutual fund data—including daily NAV pricing, investor demographic data, and transactional SIP logs—to deliver actionable business intelligence and risk metrics.

## ✨ Key Features
* **ETL & Data Engineering:** Robust data pipelines built with Python and Pandas, loading sanitized data into a relational SQLite database using SQLAlchemy.
* **Advanced Risk Modeling:** Computes institutional-grade metrics including 95% Historical Value at Risk (VaR), Conditional VaR (Expected Shortfall), and 90-day Rolling Sharpe ratios.
* **Investor Behavioral Analytics:** Tracks SIP mandate continuity, segments users by vintage cohorts, and flags at-risk retail accounts to predict churn.
* **Algorithmic Recommender System:** A standalone Python engine that matches mutual funds to mock investor profiles based on risk tolerance and historical performance.
* **Interactive Web Dashboard:** A 4-page dynamic Streamlit application featuring global multi-table filtering, dual-axis financial charts, and asset class heatmaps.

## 📂 Repository Structure
```text
bluestock_mf_capstone/
│
├── data/                   
│   ├── raw/                # Unprocessed CSV extracts
│   ├── processed/          # Cleaned CSVs
│   └── db/                 # SQLite relational database
│
├── notebooks/              # Jupyter Notebooks for ETL, EDA, and Modeling
│   ├── 01_data_ingestion.ipynb
│   ├── 02_schema_design.ipynb
│   ├── 03_eda_visualizations.ipynb
│   ├── 04_feature_engineering.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── dashboard/              
│   └── bluestock_dashboard.py  # Streamlit interactive UI application
│
├── scripts/                
│   └── recommender.py          # Standalone Fund Recommendation Engine
│
├── reports/                # Final deliverables, presentation, and exported visuals
│   ├── Final_Report.pdf
│   ├── Presentation.pptx
│   └── imgs/
│
├── requirements.txt        # Python dependencies
├── run_pipeline.py         # Master CLI execution script
└── README.md               # Project documentation
```

## 🏗️ Database Architecture
The data model utilizes a Star Schema design for optimized analytical querying:
* **Dimension Tables:** `dim_fund` (Fund Metadata), `dim_date` (Calendar tracking).
* **Fact Tables:** `fact_nav` (Daily Pricing), `fact_transactions` (Investor SIPs/Lumpsums), `fact_performance` (Long-term metrics), `fact_aum` (Assets Under Management).

> ⚠️ **Note on Version Control:** *The `bluestock_mf.db` file has been included in this repository strictly as a static, read-only seed file to enable the ephemeral deployment on Streamlit Community Cloud. In a true production environment, this database would be hosted on a dedicated cloud RDBMS (e.g., AWS RDS or PostgreSQL) and excluded from version control.*

## 🚀 Setup & Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/bluestock_mf_capstone.git
cd bluestock_mf_capstone
```

**2. Create a virtual environment (optional but recommended):**
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# On Windows use: .venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

## ⚙️ Usage

**Option 1: View the Live Deployment**
Access the fully deployed application immediately without local configuration at:
[https://bluestock-capstone-project-sa.streamlit.app/](https://bluestock-capstone-project-sa.streamlit.app/)

**Option 2: Use the Master Pipeline (CLI Menu)**
Run the master script to easily access the dashboard or recommender engine locally:
```bash
python run_pipeline.py
```

**Option 3: Launch the Dashboard Manually**
Spin up the interactive Streamlit server locally:
```bash
streamlit run dashboard/bluestock_dashboard.py
```

**Option 4: Run the Recommender Engine Manually**
Execute the recommender script via the command line by passing a risk profile (`Low`, `Moderate`, or `High`):
```bash
python scripts/recommender.py High
```

## 📊 Strategic Insights Discovered
1. **Tail Risk Divergence:** Sector-specific equity schemes show significantly steeper 95% CVaR drop-offs compared to large-cap index funds, indicating higher vulnerability during market corrections.
2. **SIP Mandate Lapses:** Behavioral analysis flagged 1,360 "at-risk" retail accounts exhibiting transactional lapses exceeding 35 days, providing a clear target list for automated retention interventions.
3. **Sector Density Vulnerabilities:** Herfindahl-Hirschman Index (HHI) analysis identified several equity portfolios with aggressive sector concentrations (HHI > 2500), reducing their broad-market diversification benefits.

---
*Created as part of the Bluestock Fintech Data Science Capstone Project - v1.0*