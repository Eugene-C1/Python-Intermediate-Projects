import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Use Path objects globally to make path handling cleaner and avoid double-backslash mess
BASE_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\JSON Output')

def save_json_data(url, headers, filename, username):
    """Fetches data from GitHub API and saves it safely to a unique JSON file."""
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Ensure the directory exists before writing
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        file_path = BASE_DIR / f"{filename}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    else:
        print(f'API Error for {username} at {url.split(".com")[1]} (Status: {response.status_code})')


def get_github_repo_data(usernames):
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {"Authorization": f"token {access_token}"}

    for username in usernames:
        print(f"Processing user: {username}...")
        
        # 1. Fetch and save user profile & repository list
        user_url = f'https://api.github.com/users/{username}'
        save_json_data(user_url, headers, f"{username}_raw_user_data", username)
        save_json_data(user_url + '/repos', headers, f"{username}_raw_repo_data", username)
        
        # 2. Read back the repository list we just downloaded
        repo_file_path = BASE_DIR / f"{username}_raw_repo_data.json"
        
        try:
            with open(repo_file_path, 'r', encoding='utf-8') as f:
                repo_data = json.load(f)
        except FileNotFoundError:
            print(f'Error: Expected file missing: {repo_file_path}')
            continue # Use 'continue' instead of 'return' so it doesn't skip other users in the list!

        # 3. Loop through individual repositories dynamically
        if isinstance(repo_data, list):
            for repo in repo_data:
                repo_name = repo.get('name')
                repo_base_url = f'https://api.github.com/repos/{username}/{repo_name}'
                
                print(f"  -> Fetching details for repo: {repo_name}")
                
                # FIX: We build a completely UNIQUE filename including the repo_name to prevent overwriting
                save_json_data(repo_base_url + '/commits', headers, f"{username}_{repo_name}_raw_commits_data", username)
                save_json_data(repo_base_url + '/contributors', headers, f"{username}_{repo_name}_raw_contributors_data", username)

    print('\nAll data has been found and successfully stored via JSON.')

if __name__ == '__main__':
    # Quick test array
    get_github_repo_data(['torvalds'])