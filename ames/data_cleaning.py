import numpy as np
import pandas as pd

from ames import config

housing = pd.read_csv(config.HOUSING_CSV)
#real_estate = pd.read_csv(dataPath / 'Ames_Real_Estate_Data.csv', low_memory=False)

# Drop index column
housing.drop('Unnamed: 0',axis=1, inplace=True)

# Drop duplicate record(s)
housing = housing.loc[~housing.duplicated(),:]

# Impute NAs with zeros
housing['TotalBsmtSF'].fillna(0, inplace=True)
housing['BsmtUnfSF'].fillna(0, inplace=True)
housing['GarageArea'].fillna(0,inplace=True)

# TODO: Additional cleaning


# Save to a Pickle file for ease of transport
housing.to_pickle(config.HOUSING_PICKLE)