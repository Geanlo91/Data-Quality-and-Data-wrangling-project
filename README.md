# Data-Quality-and-Data-wrangling-project

This project involves scraping data from multiple URLs saved in a CSV file, cleaning and converting the data to numerical values and tables, and saving it to an HDF5 file. It also includes visualizing the scraped data using different plots

## Prerequisites

- Python 3.x
- pandas
- requests
- h5py
- matplotlib

## Getting Started

1. Clone the repository or download the code files.
2. Install the required dependencies using the following command:
    ```
    pip install pandas requests h5py matplotlib
    ```
3. Update the `web_pages.csv` file with the URLs you want to scrape.
4. Run the `scraping.py` file.

## Usage

The `scraping.py` file contains the following functions:

- `scrape_data(urls)`: Scrapes data from the provided URLs and returns a dictionary of scraped tables.
- `clean_and_convert_to_numeric(df)`: Cleans and converts the data in a DataFrame to numeric format.
- `save_to_hdf5(scraped_tables, hdf5_file, scrape_date)`: Saves the scraped tables to an HDF5 file.
- `visualize_data(scraped_tables)`: Visualizes the scraped tables using line plots and bar plots.

The code includes an example of scraping for multiple days. You can adjust the `number_of_days` variable to specify the desired number of days.

## Output

The scraped data is saved to an HDF5 file named `scraped_data2.h5`. Each table is stored as a separate dataset in the HDF5 file, with a unique name based on the URL and scrape date.

## License

This project is licensed under the [MIT License](LICENSE).