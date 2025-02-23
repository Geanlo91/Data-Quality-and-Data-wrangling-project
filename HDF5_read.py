import requests
import h5py
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
import pandas as pd
import numpy as np


hdf5_file  = 'scraped_data.h5'
 
#Read data from HDF5 and convert to numerical data
def read_data(hdf5_file):
    scraped_data = {}
    with pd.HDFStore(hdf5_file, 'r') as store:
        for key in store.keys():
            scraped_data[key] = store[key]
    return scraped_data

print(read_data(hdf5_file))


 