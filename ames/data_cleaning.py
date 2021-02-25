import numpy as np
import os
import pandas as pd
from pathlib import Path

dataPath = Path('..') / 'data'
if not os.path.exists(dataPath):
    os.mkdir(dataPath)

if not os.file_exists(dataPath / 'Ames_Housing_Price_Data.csv'):
    raise FileError('File does not exist! Please place in the data directory.')

prices = pd.read_csv(dataPath / 'Ames_Housing_Price_Data.csv')
#real_estate = pd.read_csv(dataPath / 'Ames_Real_Estate_Data.csv', low_memory=False)

# Drop index column
prices.drop('Unnamed: 0',axis=1, inplace=True)

# Drop duplicate record(s)
prices = prices.loc[~prices.duplicated(),:]

# Save to a Pickle file for ease of transport
prices.to_pickle(dataPath / 'housing_data.pickle')