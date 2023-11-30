import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


#Read CSV file
web_pages = pd.read_csv('web_pages.csv')


#Loop through each URL
for index, row in web_pages.iterrows():
    url = row['url']
    page_type = row['type']
    compliance = row['compliance']

    #Check if the page is compliant
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        response =requests.get(url,timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve web page.Error: {e}")
        continue


    soup = BeautifulSoup(response.text,'html.parser')

    if page_type == 'table':
        #Extract table elements
        tables = soup.find_all('table')

        #iterate through each table and extract numeric data
        for table in tables:
                #extract text content from the table
            table_text = table.get_text()

                #search for numeric data within the table text
            match = re.search(r'(\d{1,3}(,\d{3})*(\.\d+)?)',table_text)

            if match:
                    #Print the numeric patterns found
                print(f"Numeric data found on the page{url}:\n{match}\n")

            else:
                print(f"No numeric data found on the page{url}\n")
    else:
        print(f"Page type {page_type} not supported")
else:
    print(f"Page not found: {url}")





    

