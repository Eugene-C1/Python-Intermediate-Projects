import pandas as pd

import pandas as pd
from pathlib import Path

CSV_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\CSV Output')


def language_breakdown(df_repos):
    """Calculate total language usage"""
    print('Analyzing total language usage per repository...')

    summary = df_repos.groupby('Language').size().reset_index(name='Total_Count')
    summary = summary.sort_values(by='Total_Count', ascending=False)

    summary.to_csv(CSV_DIR / 'summary_repo_language.csv', index=False)

def analyze_repo_health(df_repos, df_commits):
    """Calculate a health score of a repo"""

    print('Calculating Repository Health Metrics...')

    # Get recent activity count
    activity = df_commits.groupby('Repo_Name').size().reset_index(name='Recent_Commits')

    # Merge activity with main repo data
    health_df = pd.merge(df_repos, activity, on='Repo_Name', how='left').fillna(0)

    # Normalize data (scaling 0 - 1)
    # Ensures 1000 stars doesn't outvote 10 commits
    def normalize(column):
        if column.max() == column.min(): return 0
        return (column - column.min()) / (column.max() - column.min())

    health_df['n_commits'] = normalize(health_df['Recent_Commits'])
    health_df['n_stars'] = normalize(health_df['Stargazers_Count'])
    health_df['n_forks'] = normalize(health_df['Forks_Count'])

    # If a repo has the most issues, it's health score for this part is 0
    health_df['n_issues'] = 1 - normalize(health_df['Open_Issues_Count'])

    # Calculate the final score
    health_df['Health_Score'] = (
        (health_df['n_commits'] * 0.40) +
        (health_df['n_stars'] * 0.20) +
        (health_df['n_forks'] * 0.20) + 
        (health_df['n_issues'] * 0.20)
    ) * 100

    # rank and sort
    health_df = health_df.sort_values(by='Health_Score', ascending=False)

    # Identify Top and Neglected
    health_df['Status'] = 'Active'
    health_df.loc[health_df['Health_Score'] < 20, 'Status'] = 'Neglected'
    health_df.loc[health_df['Health_Score'] > 20, 'Status'] = 'Impactful'

    output_cols = ['Repo_Name', 'Health_Score', 'Status', 'Recent_Commits', 'Stargazers_Count']
    health_df[output_cols].to_csv(CSV_DIR / 'summary_repo_health.csv', index=False)

def analyze_hourly_weekly_activity(df_commits):
    print("Analyzing hourly/weekly contribution patterns...")

    df = df_commits
    # 1. Convert Date column to actual datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Extract Hour (0-23) and Day Name
    df['Hour'] = df['Date'].dt.hour
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    # 3. Aggregate data to get a count of commits for every Day/Hour combination
    counts = df.groupby(['Day_of_Week', 'Hour']).size().reset_index(name='Commit_Count')
    
    # 4. Pivot the data into a 2D Grid (Rows = Days, Columns = Hours)
    pivot_df = counts.pivot(index='Day_of_Week', columns='Hour', values='Commit_Count').fillna(0)
    
    # 5. Ensure all 24 hours exist, even if some hours had 0 commits
    for hour in range(24):
        if hour not in pivot_df.columns:
            pivot_df[hour] = 0.0
            
    # Sort columns explicitly 0 through 23
    pivot_df = pivot_df.reindex(columns=range(24))
    
    # 6. Ensure days are ordered logically from Monday to Sunday
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex(days_order)
    
    # Save the 2D matrix directly
    pivot_df.to_csv(CSV_DIR / 'matrix_hourly_weekly_activity.csv')
    print("Saved activity matrix to matrix_hourly_weekly_activity.csv")

def analyze_commit_history(df_commits):
    df = df_commits

    df['Date'] = pd.to_datetime(df['Date'])

    df['Year_Month'] = df['Date'].dt.to_period('M')
    df = df.groupby('Year_Month').size().reset_index(name='Commit_Count')

    # Save the 2D matrix directly
    df.to_csv(CSV_DIR / 'summary_year_month_activity.csv', index=False)
    print("Saved activity matrix to year_month_activity_activity.csv")

def run_all_analysis():
    """Loads master dataset once and run all separate analysis function"""
    print('Starting Data Analysis Phase....\n')

    try:
        df_commits = pd.read_csv(CSV_DIR / 'master_commits_cleanup.csv')
        df_controbutors = pd.read_csv(CSV_DIR / 'master_contributors_cleanup.csv')
        df_repos = pd.read_csv(CSV_DIR / 'master_repo_cleanup.csv')
    except FileNotFoundError as e:
        print(f"Analysis aborted. Missing master CSV: {e}")
        return

    # Call each analysis function
    language_breakdown(df_repos)
    analyze_repo_health(df_repos, df_commits)
    analyze_hourly_weekly_activity(df_commits)
    analyze_commit_history(df_commits)


    print("\nAll analysis summaries saved to CSV Output folder.")

if __name__ == '__main__':
    run_all_analysis()