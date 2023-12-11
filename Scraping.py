import datetime
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import h5py

# Read CSV file
web_pages = pd.read_csv('web_pages.csv')

# Loop through each URL
def new_func(url):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

for index, row in web_pages.iterrows():
    url = row['url']
    page_type = row['type']
    compliance = row['compliance']

    # Send HTTP request to the URL
    response = new_func(url)

    # Check if the page exists
    if response.status_code == 200:
        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract numeric data from the entire HTML content
        html_content = soup.prettify()

        # Adjust the regex pattern based on your HTML structure
        matches = re.finditer(r'(\b[\w\s]+\b)\s*:\s*(\d+)', html_content)

        numeric_data_with_headers = [(match.group(1), match.group(2)) for match in matches]

        if numeric_data_with_headers:
            df = pd.DataFrame(numeric_data_with_headers, columns=['header', 'value'])
            print(f"Numeric data with headers found on the page {url}: {numeric_data_with_headers}")

            # Save to HDF5 file
            create_new_file = True
            hdf5_file_path = 'Scraped data.h5'
            with h5py.File(hdf5_file_path, 'a' if not create_new_file else 'w') as hf:

                # Create a group for the URL and replacing the forward slashes with underscores
                url_group = hf.create_group(url)

                #store metadata for each url
                url_group.attrs['page_type'] = page_type
                url_group.attrs['compliance'] = compliance
                url_group.attrs['Scraping_date'] =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Create a dataset for the numeric data with headers for each URL
                url_group.create_dataset('headers',data=df['header'].to_numpy())
                url_group.create_dataset('values',data=df['value'].to_numpy())
            

        else:
            print(f"No numeric data with headers found on the page {url}")

    else:
        print(f"Page not found: {url}")



        

