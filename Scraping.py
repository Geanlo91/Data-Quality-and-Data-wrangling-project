import pandas as pd
import requests
from bs4 import BeautifulSoup


#Read CSV file
web_pages = pd.read_csv('web_pages.csv')


#Loop through each URL
for index, row in web_pages.iterrows():
    url = row['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')


    #Extract numeric info
    numeric_data = soup.find('table').get_text()
    print()

