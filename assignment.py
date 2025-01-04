import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

start_time = time.time()

# Initialize the base URL and headers
BASE_URL = "https://www.yellowpages.com/search"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Load neighborhoods, cities, and states from the CSV file
locations_df = pd.read_csv("us_neighborhoods.csv")

# Function to fetch listing URLs from search results
def get_listing_urls(search_terms, location, page):
    params = {
        "search_terms": search_terms,
        "geo_location_terms": location,
        "page": page,
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Check if there are results, indicating this is a valid page
        if not soup.find_all("div", class_="result"):
            return []

        results = soup.find_all("div", class_="result")
        urls = []
        for result in results:
            link = result.find("a", href=True)
            if link:
                href = link["href"]
                # Use urljoin to handle both relative and absolute URLs
                full_url = urljoin(BASE_URL, href)
                urls.append(full_url)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {BASE_URL}: {e}")
        return []

# Function to scrape data from each listing
def scrape_listing(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        data = {}

        # Scrape details
        data["Company Name"] = (
            soup.find("h1", class_="business-name").text.strip()
            if soup.find("h1", class_="business-name")
            else None
        )
        data["C-level Name"] = None
        data["Phone Number"] = (
            soup.find("p", class_="phone").text.strip()
            if soup.find("p", class_="phone")
            else None
        )
        data["Email"] = None

        # Extract the address
        details_section = soup.find("section", id="details-card")
        address = None
        if details_section:
            p_tags = details_section.find_all("p")
            for i, tag in enumerate(p_tags):
                if "phone" in tag.get("class", []):
                    address = p_tags[i + 1].get_text(strip=True) if i + 1 < len(p_tags) else None
                    break
        data["Address"] = address

        # Scrape website URL
        data["Website URL"] = (
            soup.find("a", class_="other-links")["href"].strip()
            if soup.find("a", class_="other-links")
            else None
        )

        # Scrape social links
        social_links = soup.find_all("a", class_="general-social-links")
        for link in social_links:
            href = link.get("href", "")
            if "linkedin" in href:
                data["LinkedIn Profile"] = href
            elif "facebook" in href:
                data["Facebook URL"] = href

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Main script to loop through locations and scrape data
results = []
search_terms = "call center"
output_file = "call_centers_progress.csv"
batch_size = 100

# Loop through all neighborhoods, cities, and states in the CSV
for _, loc in locations_df.iterrows():
    location = f"{loc['name']}, {loc['city']}, {loc['state']}"
    page = 1

    while True:  # Keep scraping until no more results are found
        print(f"Scraping {location}, Page {page}")
        listing_urls = get_listing_urls(search_terms, location, page)
        if not listing_urls:
            break
        for url in listing_urls:
            data = scrape_listing(url)
            if data:
                results.append(data)
                if len(results) % batch_size == 0:  # Save progress every batch_size rows
                    df = pd.DataFrame(results)
                    df.to_csv(output_file, index=False)
                    print(f"Saved {len(results)} rows to {output_file}")
        page += 1
        time.sleep(2)  # Add delay to avoid getting blocked

# Final save for remaining results
if results:
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Final save: {len(results)} rows saved to {output_file}")

# Record the end time
end_time = time.time()

# Calculate the time taken
elapsed_time = end_time - start_time
print(f"Total time taken: {elapsed_time:.2f} seconds")
print(f"Data saved to {output_file}")
