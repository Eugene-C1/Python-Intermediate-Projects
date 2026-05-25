# Import dependencies
import os
from dotenv import load_dotenv
import requests
import json


def get_city_lan_lat(cities):
    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv('API_KEY')

    # Initializing variable
    lats = []
    lons = []
    
    # Looping throug the list of cities
    for i in cities:
        # Send GET Request (Getting the lat and lon of Manila)
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={i}&limit=5&appid={api_key}'
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert response to JSON
            data = response.json()
            lats.append(data[0]['lat'])
            lons.append(data[0]['lon'])
        else:
            print(f'Error: {response.status_code}')

    # Adding the api result to a combined list
    combined_data = []
    for city, lon, lat in zip(cities, lons, lats):
        combined_data.append({
            'city' : city,
            'lot' : lon,
            'lat' : lat
        })

    
    json_output = json.dumps(combined_data, indent=4)
    cleaned_data = json.loads(json_output)
    #print(json_output)

    # Writing city location into a json file.
    with open(r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Requirements\raw_city_loc.json', 'w', encoding="utf-8") as file:
        json.dump(cleaned_data, file, indent=4)
    
def main():
    # Read config json
    with open(r'C:\Users\cameu\Desktop\Python Projects\1. Web Scraper\Requirements\config.json', 'r') as f:
        config = json.load(f)

    # Load the list of city in the json config
    cities = config['cities']

    # Gets latitude and longtitude of the city from weatherapi
    get_city_lan_lat(cities)


if __name__ == "__main__":

    main()