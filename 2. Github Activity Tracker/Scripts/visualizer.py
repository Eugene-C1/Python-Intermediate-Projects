import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from datetime import datetime

CSV_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\CSV Output')
CHARTS_DIR = Path(r'C:\Users\cameu\Desktop\Python Projects\2. Github Activity Tracker\Charts')


def plot_hourly_weekly_heatmap(df_commits):
    print("Generating contribution heatmap...")
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    
    df = df_commits

    # Set up the Matplotlib canvas (wide format fits 24 hours perfectly)
    plt.figure(figsize=(14, 6))
    
    # Generate 24-hour clean labels (e.g., 12 AM, 1 AM... 11 PM)
    hour_labels = [f"{h if h <= 12 else h-12} {'AM' if h < 12 else 'PM'}" if h % 2 == 0 else "" for h in range(24)]
    # Tweak labels slightly for 12 PM/AM exceptions
    hour_labels[0] = "12 AM"
    hour_labels[12] = "12 PM"

    # Create the heatmap
    sns.heatmap(
        df,
        cmap='Greens',          # GitHub's signature contribution color
        annot=False,            # Hide numbers inside cells to keep it clean like GitHub
        linewidths=1.5,         # Creates grid borders separating the "tiles"
        linecolor='#FFFFFF',    # White gridlines
        xticklabels=hour_labels,# Use our clean time labels
        cbar_kws={'label': 'Number of Commits'} # Add title to color bar
    )
    
    # Final aesthetic touches
    plt.title('Commit Contribution Punchcard (Day vs Hour)', fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Time of Day', fontsize=12, labelpad=10)
    plt.ylabel('Day of Week', fontsize=12, labelpad=10)
    plt.xticks(rotation=0)      # Keep hour text horizontal
    plt.yticks(rotation=0)      # Keep day text horizontal
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'github_punchcard_heatmap.png', dpi=300)
    plt.show()

def language_pie_chart(df_repos_language):
    df = df_repos_language

    plt.pie(df['Total_Count'], labels=df['Language'], autopct='%1.1f%%')
    plt.title('Language Usage in All Repositories')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'all_repository_language_pie_chart.png', dpi=300)
    plt.show()

def commit_line_chart(df_year_month):
    df = df_year_month

    # Set up the Matplotlib canvas (wide format fits 24 hours perfectly)
    plt.figure(figsize=(14, 6))

    plt.plot(df['Year_Month'], df['Commit_Count'], linestyle='-')
    plt.grid(True, linestyle='--')

    plt.title('Year_Month Commit Activity Line Chart')
    plt.xlabel('Year_Month')
    plt.ylabel('Commit Count')
    plt.xticks(rotation=45) # Tilts your dates so they don't smash into each other

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'year_month_activity_linechart.png', dpi=300)
    plt.show()

def most_stars_bar_chart(df_repos):
    df = df_repos

    # Set up the Matplotlib canvas (wide format fits 24 hours perfectly)
    plt.figure(figsize=(14, 6))

    plt.bar(df['Repo_Name'], df['Stargazers_Count'])
    plt.title('Total Stars per Repository')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'star_count_bar_chart.png', dpi=300)
    plt.show()

def run_all_visualization():
    """Loads master dataset once and run all separate analysis function"""
    print('Starting Data Analysis Phase....\n')

    try:
        df_repos = pd.read_csv(CSV_DIR / 'master_repo_cleanup.csv')
        df_repos_language = pd.read_csv(CSV_DIR / 'summary_repo_language.csv')
        df_hourly_weekly = pd.read_csv(CSV_DIR / 'matrix_hourly_weekly_activity.csv', index_col='Day_of_Week')
        df_year_month = pd.read_csv(CSV_DIR / 'summary_year_month_activity.csv')
    except FileNotFoundError as e:
        print(f"Analysis aborted. Missing master CSV: {e}")
        return
    
    plot_hourly_weekly_heatmap(df_hourly_weekly)
    language_pie_chart(df_repos_language)
    commit_line_chart(df_year_month)
    most_stars_bar_chart(df_repos)

if __name__ == '__main__':
    run_all_visualization()