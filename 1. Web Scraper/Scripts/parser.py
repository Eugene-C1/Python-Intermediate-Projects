# Import dependencies
import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd 

# Output to csv
def output_csv(weather_records):
    if weather_records:
        df = pd.DataFrame(weather_records)
        output_path = r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Outputs\raw_city_temp.csv'
        df.to_csv(output_path, index=False)
        print(f"\n All data successfully saved to: {output_path}")
    else:
        print("\nNo data was retrieved. CSV file not created.")


# Get raw data
def get_raw_data(city_loc, api_key):
    weather_records = []

    for city in city_loc:
        # Changed the endpoint from '3.0/onecall' to '2.5/weather'
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={city["lat"]}&lon={city["lon"]}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            record = {
                "City_Name": data.get("name", "Unknown"),
                "Country Code": data["sys"]["country"],
                "Temperature": data["main"]["temp"],
                "Feels_Like": data["main"]["feels_like"],
                "Humidity": data["main"]["humidity"],
                "Wind_Speed": data["wind"]["speed"],
                "Description": data["weather"][0]["description"] if data["weather"] else "N/A"
            }
            weather_records.append(record)
            print(f"Successfully processed: {record['City_Name']}")
        else:
            print(f'Error {response.status_code}: {response.text}')

    
    output_csv(weather_records)

def main():
    with open(r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Requirements\raw_city_loc.json', 'r') as f:
        city_loc = json.load(f)

    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv('API_KEY')

    get_raw_data(city_loc, api_key)

if __name__ == '__main__':
    main()