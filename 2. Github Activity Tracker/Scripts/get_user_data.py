import os
import requests
from dotenv import load_dotenv
import sys
import json

def get_user_data(url, headers, username, content):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f'Error: User "{username}" not found. (Status: {response.status_code})')

    with open(f'C:\\Users\\cameu\Desktop\\Python Projects\\2. Github Activity Tracker\\Output\\{username}_raw_{content}.json', 'w') as f:
        json.dump(data, f, indent=4)
    
def main(usernames):
    # Load access token from .env file
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')

    for username in usernames:
        url = f'https://api.github.com/users/{username}'  # Added the / here
        headers = {"Authorization": f"token {access_token}"}

        get_user_data(url, headers, username, 'user_data')
        get_user_data(url + '/repos', headers, username, 'repo_data')
        
    print('Data has been found and stored via json')
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: Please provide a GitHub username')
        print('Usage: uv run main.py <username>')
        sys.exit(1)

    usernames = sys.argv[1:]
    main(usernames)
