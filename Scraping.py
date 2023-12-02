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

    #Send HTTP request to the URL
    response = new_func(url)

    #Check if the page exists
    if response.status_code == 200:
        #Parse the HTTP response

        soup = BeautifulSoup(response.text,'html.parser')
    
        if page_type == 'numeric':
        #Extract table elements
            tables = soup.find_all('table')

        #iterate through each table and extract numeric data
            for table in tables:
                #extract text content from the table
                rows = table.find_all('p')

                for row in rows:
                # Extract data from each cell in the row
                    cells = row.find_all(['p','td'])
                    row_data = [cell.get_text(strip=True) for cell in cells]

                #print(row_data)
                    print(f"row data: {row_data}")
    else:
            print("No tables found")
    
    #Save the data in a HDF5 file
            with h5py.File('data.h5', 'w') as hf:
                hf.create_dataset('numeric', data=row_data)
                hf.close()







    

