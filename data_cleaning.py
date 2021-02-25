import pandas as pd
import numpy as np
from pathlib import Path

dataPath = Path('data')

prices = pd.read_csv(dataPath / 'Ames_Housing_Price_Data.csv')
#real_estate = pd.read_csv(dataPath / 'Ames_Real_Estate_Data.csv', low_memory=False)

# Drop index column
prices.drop('Unnamed: 0',axis=1, inplace=True)

# Drop duplicate record(s)
prices = prices.loc[~prices.duplicated(),:]

# Save to a Pickle file for ease of transport
prices.to_pickle(dataPath / 'housing_data.pickle')