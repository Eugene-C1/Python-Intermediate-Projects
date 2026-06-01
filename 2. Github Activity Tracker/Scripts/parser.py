import json
import pandas as pd
from pathlib import Path

# Define your directory structures
JSON_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\JSON Output')
CSV_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\CSV Output')

def compile_json_to_clean_csv():
    # Ensure output directory exists
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    
    commit_rows = []
    contributor_rows = []
    
    # 1. Scan the folder for commit files
    # Filename format: {username}_{repo_name}_raw_commits_data.json
    for file_path in JSON_DIR.glob('*_raw_commits_data.json'):
        # Extract the metadata hidden in the filename itself
        parts = file_path.stem.split('_')
        username = parts[0]
        # In case the repo name has underscores, stitch them back together
        repo_name = "_".join(parts[1:-3]) 
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                commits = json.load(f)
                
            if isinstance(commits, list):
                for commit in commits:
                    # SELECT ONLY CLEANUP-READY DATA POINTS
                    row = {
                        'Username': username,
                        'Repo_Name': repo_name,
                        'SHA': commit.get('sha'),
                        'Author_Login': commit.get('author', {}).get('login') if commit.get('author') else 'Unknown',
                        'Commit_Message': commit.get('commit', {}).get('message', '').strip().replace('\n', ' '),
                        'Date': commit.get('commit', {}).get('author', {}).get('date')
                    }
                    commit_rows.append(row)
        except Exception as e:
            print(f"Skipping corrupt file {file_path.name}: {e}")

    # 2. Scan the folder for contributor files
    # Filename format: {username}_{repo_name}_raw_contributors_data.json
    for file_path in JSON_DIR.glob('*_raw_contributors_data.json'):
        parts = file_path.stem.split('_')
        username = parts[0]
        repo_name = "_".join(parts[1:-3])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contributors = json.load(f)
                
            if isinstance(contributors, list):
                for contributor in contributors:
                    row = {
                        'Username': username,
                        'Repo_Name': repo_name,
                        'Contributor_Login': contributor.get('login'),
                        'Contributions_Count': contributor.get('contributions'),
                        'Type': contributor.get('type')
                    }
                    contributor_rows.append(row)
        except Exception as e:
            print(f"Skipping corrupt file {file_path.name}: {e}")

    # 3. Save everything into massive master CSV files
    if commit_rows:
        df_commits = pd.DataFrame(commit_rows)
        
        # Safe deduplication check
        if 'SHA' in df_commits.columns:
            df_commits.drop_duplicates(subset=['SHA'], inplace=True)
            
        df_commits.to_csv(CSV_DIR / 'master_commits_cleanup.csv', index=False, encoding='utf-8')
        print(f"Compiled {len(commit_rows)} commits into master_commits_cleanup.csv")
        
    if contributor_rows:
        df_contributors = pd.DataFrame(contributor_rows)
        df_contributors.to_csv(CSV_DIR / 'master_contributors_cleanup.csv', index=False, encoding='utf-8')
        print(f"Compiled {len(contributor_rows)} contributors into master_contributors_cleanup.csv")

if __name__ == '__main__':
    compile_json_to_clean_csv()