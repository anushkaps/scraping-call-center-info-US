# Business Scraper: Yellow Pages

This project is a Python-based scraper that collects business data from **Yellow Pages** for call centers across neighborhoods in the United States. It fetches essential details like business name, phone number, address, website, and social media links, while handling pagination and location data for efficient scraping.

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [Challenges Faced](#challenges-faced)
- [File Structure](#file-structure)
- [Running the Code](#running-the-code)
- [License](#license)

## Project Overview

The objective of this project was to scrape business listings from Yellow Pages, starting with "call center" listings. However, the project was complicated by the lack of complete location data from Yellow Pages, so I supplemented this with neighborhood and city data obtained from external sources like Britannica and OpenStreetMap.

## Getting Started

To get started with this project, you’ll need Python and a few libraries to be installed. Please follow the steps below to set up your environment and run the scraper.

### Prerequisites

You will need the following libraries:
- `requests` – To send HTTP requests to websites.
- `beautifulsoup4` – For parsing HTML and extracting data.
- `pandas` – For managing data and saving it to CSV.
- `urllib` – To handle URL joining and manipulation.

Install them using pip:

```bash
pip install requests beautifulsoup4 pandas
```

## How It Works

### Step 1: Location Data

Since Yellow Pages doesn’t provide all the locations for business listings, the scraper first collects data about **cities** and **neighborhoods** in the United States. 

1. **Collecting Cities:** I scrape a list of all cities from **Britannica** and save the data into a file called `cities.txt`.
2. **Neighborhood Data:** Using OpenStreetMap's API, I fetch neighborhood data for each city, including the state, city name, neighborhood name, and geographic coordinates (latitude and longitude). This data is stored in a CSV file called `us_neighborhoods.csv`.

### Step 2: Scraping Yellow Pages

Once the locations are gathered, the scraper fetches business listings from Yellow Pages.

1. **Get Listing URLs:** The script searches Yellow Pages for call centers by querying with city, state, and neighborhood as search terms. It handles pagination by continuing to search for results on subsequent pages until 100 listings are found or no more pages are available.
   
2. **Extracting Data:** For each listing, the scraper extracts the following:
   - Business Name
   - Phone Number
   - Address
   - Email
   - Website URL
   - Social Media links (e.g., LinkedIn, Facebook)
   
3. **Saving Data:** The extracted data is stored in a CSV file, `call_centers_progress.csv`, with each run appending to this file after every 100 rows. I yet haven't saved all the data since there are almost 15,000 neighborhoods and its inefficient to add a file of that size to github.

### Step 3: Main Script (`assignment.py`)

The script that handles the bulk of the work is `assignment.py`. This script:

1. Loads **location data** from `us_neighborhoods.csv`.
2. Sends search requests to Yellow Pages for **call center** listings based on each neighborhood.
3. Scrapes necessary business details from each listing.
4. Manages pagination to ensure all available results are fetched.
5. Saves the results to a CSV file after each successful scrape, updating every 100 rows for better progress tracking.

### Key Functions

- `get_listing_urls(search_terms, location, page)`: Fetches listing URLs from Yellow Pages based on search terms and location.
- `scrape_listing(url)`: Extracts business details (name, phone, address, website, etc.) from each listing URL.
- `save_to_csv(results)`: Saves the collected results to a CSV file.

## Challenges Faced

1. **Missing Location Data in Yellow Pages:** Yellow Pages did not offer a comprehensive list of neighborhoods. I had to collect location data manually from Britannica and OpenStreetMap, ensuring I had a list of cities and neighborhoods in the U.S.
   
2. **Inconsistent Data from External Sources:** Initially, I tried scraping Wikipedia for cities and neighborhoods, but the inconsistent page structure made scraping unreliable. Switching to Britannica and OpenStreetMap's API solved this issue by providing more structured data.
   
3. **Handling Pagination:** Yellow Pages lists multiple pages for some search results. I had to ensure that the scraper efficiently navigated through all the pages, collecting a total of 100 unique rows per location.

4. **Rate Limiting:** Yellow Pages did not impose any rate limiting, which meant I didn’t need to worry about throttling requests, allowing for faster scraping.

## File Structure

```plaintext
/
├── fetch_neighborhoods.py             # Script to collect neighborhoods using OpenStreetMap
├── us_neighborhoods.csv               # CSV with city, state, neighborhood, lat, lon data
├── assignment.py                      # Main script for scraping Yellow Pages
├── cities.txt                         # File containing a list of all cities in the U.S.
└── call_centers_progress.csv         # CSV where business data is saved
```

## Running the Code

To run the scraper, you need to follow these steps:

1. First, run `fetch_neighborhoods.py` to generate the `us_neighborhoods.csv`(which I have already uploaded) file with neighborhood data.

```bash
python fetch_neighborhoods.py
```

2. After that, execute `assignment.py` to begin scraping Yellow Pages for call center listings. The script will automatically go through each neighborhood and scrape data.

```bash
python assignment.py
```

The results will be saved in the `call_centers_first_100.csv` file. The scraper will stop after 100 rows are collected, ensuring you get a manageable data set.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
