import datetime
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import h5py

def sanitize_url(url):
    #Replace slashes and other special characters with underscores
    return url.replace("https://", "").replace("/", "_").replace(":", "_")

# Read CSV file
web_pages = pd.read_csv('web_pages.csv')

#Open the HDF5 file
with h5py.File('Scraped data.h5', 'a') as hf:

# Loop through each URL in the CSV file and reapce
    for index, row in web_pages.iterrows():
        url = row['url']
        page_type = row['type']
        compliance = row['compliance']

        # Send HTTP request to the URL
        response = requests.get(url)

        # Check if the page exists
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract numeric data from the entire HTML content
            html_content = soup.prettify()
            matches = re.finditer(r'(\b[\w\s]+\b)\s*:\s*(\d+)', html_content)
            numeric_data_with_headers = [(match.group(1), match.group(2)) for match in matches]
            print(f"Numeric data with headers found on the page {url}: {numeric_data_with_headers}")

            if numeric_data_with_headers:
                #check if a group for the URL already exists
                if url in hf:
                    url_group = hf[url]
                else:
                    url_group = hf.create_group(url)

                url_group.attrs['page_type'] = page_type
                url_group.attrs['compliance'] = compliance
                Scraping_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                #save each key-value pair as a separate dataset
                for i, (key, value) in enumerate(numeric_data_with_headers):
                    dataset_name = f'{key}_{i}'
                    #check if the dataset already exists
                    if dataset_name not in url_group:
                        url_group.create_dataset(dataset_name, data=value)
                    else:
                        continue

                    ds = url_group.create_dataset(dataset_name, data=value)
                    ds.attrs['Scraped_date'] = Scraping_date
            else:
                print(f"No numeric data with headers found on the page {url}")

        else:
            print(f"Page not found: {url}")




        

