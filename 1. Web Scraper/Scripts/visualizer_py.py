# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def run_analysis():

    # 3. Define the destination folder and file path
    output_dir = r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Outputs'
    
    # %%
    # Load csv to Dataframe
    df = pd.read_csv(r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Outputs\raw_city_temp.csv')


    # %%
    df2 = df.groupby('City_Name').mean(numeric_only=True).reset_index()
    df2

    # %%
    plt.figure(figsize=(10, 5))

    plt.bar(df2['City_Name'], df2['Temperature'])

    plt.title('Average Temperature by City')
    plt.xlabel('City')
    plt.ylabel('Temperature')

    plt.tight_layout()
    output_file = os.path.join(output_dir, 'avg_city_temp_chart.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📈 Chart successfully saved to: {output_file}")
    plt.show()

    # %%
    plt.figure(figsize=(10, 5))

    plt.bar(df2['City_Name'], df2['Feels_Like'])

    plt.title('Average Feels Like Temperature by City')
    plt.xlabel('City')
    plt.ylabel('Temperature')

    plt.tight_layout()
    output_file = os.path.join(output_dir, 'avg_feels_like_temp_chart.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📈 Chart successfully saved to: {output_file}")
    plt.show()



