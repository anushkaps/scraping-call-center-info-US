import requests
import json
import pandas as pd
from tqdm import tqdm

# Overpass API endpoint
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# Define query to fetch neighborhoods
QUERY_TEMPLATE = """
[out:json];
area[name="{state}"]->.state;r̥
area[name="{city}"](area.state)->.city;
node["place"="neighbourhood"](area.city);
out;
"""

# Load cities from file
def load_cities(filename):
    cities = []
    with open(filename, "r") as file:
        for line in file:
            state, city = line.strip().split(',')
            cities.append({"state": state, "city": city})
    return cities

states_cities = load_cities("cities.txt")

def fetch_neighborhoods(state, city):
    """Fetch neighborhoods for a specific state and city."""
    query = QUERY_TEMPLATE.format(state=state, city=city)
    response = requests.get(OVERPASS_API_URL, params={"data": query})
    if response.status_code == 200:
        data = response.json()
        neighborhoods = []
        for element in data.get("elements", []):
            neighborhoods.append({
                "state": state,
                "city": city,
                "name": element.get("tags", {}).get("name", "Unknown"),
                "lat": element.get("lat"),
                "lon": element.get("lon")
            })
        return neighborhoods
    else:
        print(f"Failed to fetch data for {city}, {state}. Status: {response.status_code}")
        return []

# Main script to loop through cities and fetch datar̥r̥
all_neighborhoods = []
for location in tqdm(states_cities, desc="Fetching neighborhoods"):
    state = location["state"]
    city = location["city"]
    neighborhoods = fetch_neighborhoods(state, city)
    all_neighborhoods.extend(neighborhoods)

# Save data to JSON and CSV
with open("us_neighborhoods.json", "w") as file:
    json.dump(all_neighborhoods, file, indent=2)

df = pd.DataFrame(all_neighborhoods)
df.to_csv("us_neighborhoods.csv", index=False)

print(f"Fetched {len(all_neighborhoods)} neighborhoods. Data saved to 'us_neighborhoods.json' and 'us_neighborhoods.csv'.")
