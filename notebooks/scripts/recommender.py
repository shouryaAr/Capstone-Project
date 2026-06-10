import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

def get_engine():
    db_path = Path.cwd() / "data" / "db" / "bluestock_mf.db"
    if not db_path.exists():
        db_path = Path.cwd().parent / "data" / "db" / "bluestock_mf.db"
    return create_engine(f"sqlite:///{db_path}")

def recommend_funds(risk_profile="Moderate"):
    engine = get_engine()
    funds = pd.read_sql("SELECT amfi_code, scheme_name, risk_grade, category FROM dim_fund", engine)
    perf = pd.read_sql("SELECT amfi_code, sharpe_ratio, return_3yr_pct FROM fact_performance", engine)

    funds['amfi_code'] = funds['amfi_code'].astype(str).str.strip()
    perf['amfi_code'] = perf['amfi_code'].astype(str).str.strip()

    merged = funds.merge(perf, on='amfi_code')
    matches = merged[merged['risk_grade'].str.lower() == risk_profile.lower()]

    return matches.sort_values(by='sharpe_ratio', ascending=False).head(3)[
        ['scheme_name', 'category', 'risk_grade', 'sharpe_ratio', 'return_3yr_pct']
    ]

if __name__ == "__main__":
    import sys
    profile = sys.argv[1] if len(sys.argv) > 1 else "Moderate"
    print(f"\nTop 3 Funds for Risk Profile: {profile.upper()}")
    print(recommend_funds(profile).to_string(index=False))
