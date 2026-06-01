from dotenv import load_dotenv
import sys

import github_client
import parser
import analyzer
import visualizer

def main(usernames):
    github_client.get_github_repo_data(usernames)

    parser.compile_json_to_clean_csv()
    analyzer.run_all_analysis()
    visualizer.run_all_visualization()

if __name__ == '__main__':
    # Get username from CLI args
    if len(sys.argv) < 2:
        print('Error: Please provide a GitHub username')
        print('Usage: uv run main.py <username>')
        sys.exit(1)

    usernames = sys.argv[1:]
    main(usernames)