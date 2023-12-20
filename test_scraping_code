import pandas as pd
import matplotlib.pyplot as plt

# Test case 1: Empty table
table1 = pd.DataFrame()
scraped_tables1 = {'url1': table1}
visualize_data(scraped_tables1)  # No plots should be generated

# Test case 2: Table with fewer than 2 columns
table2 = pd.DataFrame({'A': [1, 2, 3]})
scraped_tables2 = {'url2': table2}
visualize_data(scraped_tables2)  # No plots should be generated

# Test case 3: Table with fewer than 2 rows
table3 = pd.DataFrame({'A': [1], 'B': [2]})
scraped_tables3 = {'url3': table3}
visualize_data(scraped_tables3)  # No plots should be generated

# Test case 4: Table with numeric columns
table4 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
scraped_tables4 = {'url4': table4}
visualize_data(scraped_tables4)  # Box plot should be generated

# Test case 5: Table with categorical and numeric columns
table5 = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [1, 2, 3]})
scraped_tables5 = {'url5': table5}
visualize_data(scraped_tables5)  # Line plot should be generated

# Test case 6: Table that is not a DataFrame
table6 = 'Not a DataFrame'
scraped_tables6 = {'url6': table6}
visualize_data(scraped_tables6)  # Error message should be printed