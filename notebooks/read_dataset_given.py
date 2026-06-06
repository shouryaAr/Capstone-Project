import pandas as pd
from pathlib import Path
def read_nav_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading NAV data from {file_path}: {e}")
        return pd.DataFrame()
def data_check(df):
    if df.empty:
        print("Dataframe is empty")
    else:
        print("Shape: ", df.shape)
        print("Data types: ", df.dtypes)
        print("First 5 rows: ", df.head())
if __name__ == "__main__":
    RAW_DIR = Path.cwd() / 'data' / 'raw'
    csv_files = list(RAW_DIR.glob("*.csv"))
    for file in csv_files:
        print(f"Reading NAV data from: {file}")
        nav_df = read_nav_data(file)
        data_check(nav_df)