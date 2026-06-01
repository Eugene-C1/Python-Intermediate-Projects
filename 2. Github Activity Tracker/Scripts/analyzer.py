import pandas as pd

import pandas as pd
from pathlib import Path

CSV_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\CSV Output')

def run_all_analysis():
    """Loads master dataset once and run all separate analysis function"""
    print('Starting Data Analysis Phase....\n')

    try:
        df_commits = pd.read_csv(CSV_DIR / 'master_commits_cleanup.csv')
        df_controbutors = pd.read_csv(CSV_DIR / 'master_contributors_cleanup.csv')
    except FileNotFoundError as e:
        print(f"Analysis aborted. Missing master CSV: {e}")
        return

    # Call each analysis function
    


    print("\nAll analysis summaries saved to CSV Output folder.")

if __name__ == '__main__':
    run_all_analysis()