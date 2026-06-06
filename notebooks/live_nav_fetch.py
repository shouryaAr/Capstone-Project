import requests
import time
from pathlib import Path
import pandas as pd

def fetch_nav(scheme_code, scheme_name, dir_path, max_retries=3):
    session = requests.Session()
    for tries in range(max_retries):
        try:
            response = session.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=(10, 30))
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data['data'])
            df['scheme_code'] = scheme_code
            df['scheme_name'] = scheme_name
            df = df[['scheme_code', 'scheme_name', 'date', 'nav']]
            safe_name = scheme_name.replace(' ', '_').replace('/', '_')
            df.to_csv(f"{dir_path}/{scheme_code}_{safe_name}_raw.csv", index=False)
            return df
        except requests.exceptions.Timeout:
            wait_time = 2 ** tries
            print(f"Timeout error fetching NAV for scheme code {scheme_code}. Retrying ({tries + 1}/{max_retries}) in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error fetching NAV for scheme code {scheme_code}: {e}")
            df = pd.DataFrame()
            return df
    return pd.DataFrame()
if __name__ == "__main__":
    RAW_DIR = Path.cwd() / 'data' / 'raw' / 'fetched_nav'
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    schemes = {
            "125497": "HDFC Top 100 Direct",
            "119551": "SBI Bluechip",
            "120503": "ICICI Bluechip",
            "118632": "Nippon Large Cap",
            "119092": "Axis Bluechip",
            "120841": "Kotak Bluechip"
        }
    for code, name in schemes.items():
        df = fetch_nav(code, name, RAW_DIR)
        print(f"Fetched and saved NAV for scheme code: {code}")
        time.sleep(1)