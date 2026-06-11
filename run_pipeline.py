"""
Bluestock Mutual Fund Analytics - Master Execution Pipeline
This script provides a clean CLI interface to launch the dashboard and run the recommender.
"""
import os
import sys
import subprocess
from pathlib import Path

def get_project_root():
    """Safely derive the project root path."""
    return Path(__file__).parent.resolve()

def launch_dashboard():
    root = get_project_root()
    dashboard_path = root / "dashboard" / "bluestock_dashboard.py"
    print(f"Launching Interactive Dashboard at: {dashboard_path}...")
    subprocess.run(["streamlit", "run", str(dashboard_path)])

def run_recommender(risk_profile):
    root = get_project_root()
    recommender_path = root / "scripts" / "recommender.py"
    
    if not recommender_path.exists():
        print(f"[-] Error: recommender.py script could not be located under {root}.")
        return

    print(f"Running Recommender Engine for profile: {risk_profile}...\n")
    subprocess.run([sys.executable, str(recommender_path), risk_profile])

if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("📊 BLUESTOCK MF ANALYTICS MASTER PIPELINE")
        print("="*40)
        print("1. Launch Interactive Streamlit Dashboard")
        print("2. Run Fund Recommender Engine (Low Risk)")
        print("3. Run Fund Recommender Engine (Moderate Risk)")
        print("4. Run Fund Recommender Engine (High Risk)")
        print("5. Exit Pipeline")
        print("="*40)
        
        choice = input("\nEnter your selection (1-5): ").strip()
        
        if choice == '1':
            launch_dashboard()
        elif choice == '2':
            run_recommender("Low")
        elif choice == '3':
            run_recommender("Moderate")
        elif choice == '4':
            run_recommender("High")
        elif choice == '5':
            print("\nExiting pipeline. Happy investing!")
            break
        else:
            print("\n[-] Invalid selection. Please enter a number between 1 and 5.")