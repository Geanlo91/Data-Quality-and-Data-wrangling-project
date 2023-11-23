import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


#Read CSV file
web_pages = pd.read_csv('web_pages.csv')


#Loop through each URL
for index, row in web_pages.iterrows():
    urls = row['url']
    for url in urls:
        response = requests.get(urls)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')


        #Extract table info with heading 'Index Performance'
            tables = soup.find_all('table')

        #iterate through each table and extract numeric data
            for table in tables:
                #extract text content from the table
                table_text = table.get_text()

        #Print the numeric patterns found
                print(f"Numeric data found on the page{url}:\n{table_text}\n")
        else:
            print(f"Failed to retrieve the web page{url}.Status code:{response.status_code}")





    

