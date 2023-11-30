import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


#Read CSV file
web_pages = pd.read_csv('web_pages.csv')


#Loop through each URL
def new_func(url):
    return requests.get(url,headers={'User-Agent':'Mozilla/5.0'})

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
    
    if page_type == '':
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





    

