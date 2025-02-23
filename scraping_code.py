import pandas as pd
import requests 
import datetime
from datetime import datetime 
import logging
import re

#Logging setup
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')    

# Read URLs from CSV
csv_file = 'web_pages.csv'  # Replace with your CSV file path
urls = pd.read_csv(csv_file)

#Function to sanitize group names
def sanitize_name(name):
    #Replacenon_alphanumeric characters with underscores
    sanitized = re.sub(r'\W+', '_', name)
    #Ensure that group name doesn't start with digit
    if sanitized[0].isdigit():
        sanitized = '_' + sanitized
    return sanitized


# Function to scrape data
def scrape_data(urls):
    scraped_tables = {}

    # Iterate over rows in the CSV file
    for _, row in urls.iterrows():  
        url = row['URL']

        # Get the first column name from CSV file
        first_column_name = row['start_column_name']
        try:
            response = requests.get(url)
            tables_list = pd.read_html(response.text)
            for table in tables_list:

                # Check if the first column of the table matches the desired name
                if table.columns[0] == first_column_name:
                    scraped_tables[url] = table
                    logging.info(f"\nScraped table from: {url} \nfirst column: '{first_column_name} \nscrapped date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Print the first few rows of the table
                    print(table.head())  
                #add regex backup if no table found
                else:
                    logging.error(f"No tables found in {url}")
                    print(f"No tables found in {url}")
                      
        except ValueError:
            logging.error(f"No tables found in {url}")
            print(f"No tables found in {url}")
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")
    return scraped_tables

#Saving scraped data to HDF5 file
def save_to_hdf5(scraped_tables, hdf5_file, scrape_date):
    with pd.HDFStore(hdf5_file, 'a') as store:
        for url, (url, table) in enumerate(scraped_tables.items(), start=1):
            if isinstance(table, pd.DataFrame):
                # Sanitize the group name with scrape date
                group_name = f"{sanitize_name(url + '_' + scrape_date)}"

                #insert scrape date as first column 
                table.insert(0, 'Scrape Date', scrape_date)
                
                store.put(group_name, table)

                # Save URL and date as attributes
                store.get_storer(group_name).attrs.metadata = {f"url_{url}": url, 'date': scrape_date}
                logging.info(f"Saved table from: {url} scrapped date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                logging.error(f"Skipped saving non-DataFrame data from {url}")
                print(f"Skipped saving non-DataFrame data from {url}")
           

# HDF5 file name
hdf5_file = 'scraped_data.h5'
 
#scraping loop
number_of_times = 1
for _ in range(number_of_times):
    scrape_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    scraped_data = scrape_data(urls)

    # Save to HDF5 and visualize after processing all URLs
    save_to_hdf5(scraped_data, hdf5_file, scrape_date)
    print(f"Saved scraped data to {hdf5_file}")
    

