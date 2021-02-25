import numpy as np
import pandas as pd

from ames import config

prices = pd.read_csv(config.HOUSING_CSV)
#real_estate = pd.read_csv(dataPath / 'Ames_Real_Estate_Data.csv', low_memory=False)

# Drop index column
prices.drop('Unnamed: 0',axis=1, inplace=True)

# Drop duplicate record(s)
prices = prices.loc[~prices.duplicated(),:]

# TODO: Additional cleaning


# Save to a Pickle file for ease of transport
prices.to_pickle(config.HOUSING_PICKLE)