import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re   

hdf5_file = "scraped_data.h5"
df = pd.DataFrame()


def sanitize_name(name):
    # Replace non-alphanumeric characters with underscores
    sanitized = re.sub(r'\W+', '_', name)
    # Ensure that the name doesn't start with a digit
    if sanitized[0].isdigit():
        sanitized = '_' + sanitized
    return sanitized
 
#define function which collects first row of each URL for each date
def aggregate_first_rows(hdf5_file, target_urls):
    # Sanitize the target URLs
    sanitized_urls = [sanitize_name(url) for url in target_urls]

    # Initialize dictionaries for aggregated data and column names
    aggregated_data = {url: [] for url in sanitized_urls}
    column_names = {url: None for url in sanitized_urls}

    with pd.HDFStore(hdf5_file, 'r') as store:
        for key in store.keys():
            # Remove the leading slash and sanitize the key
            sanitized_key = sanitize_name(key[1:])

            for sanitized_url in sanitized_urls:
                if sanitized_url in sanitized_key:
                    data = store[key]
                    metadata = store.get_storer(key).attrs.metadata
                    url = metadata.get('url', '')

                    first_row = data.head(1)
                    if column_names[sanitized_url] is None:
                        column_names[sanitized_url] = first_row.columns
                    aggregated_data[sanitized_url].append(first_row)
                    break  # Break the loop once a match is found

    # Combine all first rows into separate DataFrames for each sanitized URL
    for sanitized_url in sanitized_urls:
        if aggregated_data[sanitized_url]:
            aggregated_data[sanitized_url] = pd.concat(aggregated_data[sanitized_url])[column_names[sanitized_url]]
        else:
            aggregated_data[sanitized_url] = pd.DataFrame(columns=column_names[sanitized_url])
        print(f"Aggregated data from {sanitized_url}")
        print(aggregated_data[sanitized_url])

    return aggregated_data

# Example usage
target_urls = ['https_www_bitdegree_org_cryptocurrency_prices_xrp_xrp_price_price_history', 'https_www_skysports_com_la_liga_table', 'https_www_absa_co_za_indices_share_information_']
aggregated_tables = aggregate_first_rows(hdf5_file, target_urls)


def visualize_data(aggreggated_tables):
    for url, table in aggreggated_tables.items():
        if not table.empty:
            print(f"Visualizing data from {url}")
            plt.figure()
            
            #Plot specificcolumns for each URL and adjust legends
            if url == "https_www_bitdegree_org_cryptocurrency_prices_xrp_xrp_price_price_history":
                #remove the $ sign from the price columns, convert to float and plot
                table['High'] = table['High'].str.replace('$', '').astype(float)
                table.plot(x='Scrape Date', y='High',kind = 'line')
                plt.legend(['High price $'], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                plt.tick_params(axis='x', rotation=60)
                plt.title('XRP High Price')

            elif url == "https_www_skysports_com_la_liga_table":
                table.plot(x='Scrape Date', y=['Pl','GD'],kind = 'bar')
                plt.legend(['Played','Goal Diff'], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                plt.tick_params(axis='x', rotation=60)
                plt.title('Real Madrid played vs Goal Diff')

            elif url == "https_www_absa_co_za_indices_share_information_":
                table.plot(x='Scrape Date', y=['High', 'Low'],kind = 'line')
                plt.legend(['High', 'Low'], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                plt.tick_params(axis='x', rotation=60)
                plt.title('JSE 4SI High and Low Prices')

            plt.show()

visualize_data(aggregated_tables)