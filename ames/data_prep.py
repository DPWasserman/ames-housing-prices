import numpy as np
import pandas as pd

import sys
sys.path.append('../ames')
import config

def clean(housing_location, save_to_disk=True, output_location=config.HOUSING_PICKLE):

    housing = pd.read_csv(housing_location)

    # Drop index column
    housing.drop('Unnamed: 0',axis=1, inplace=True)

    # Drop duplicate record(s)
    housing = housing.loc[~housing.duplicated(),:]

    # Impute NAs with zeros
    housing['TotalBsmtSF'].fillna(0, inplace=True)
    housing['BsmtUnfSF'].fillna(0, inplace=True)
    housing['GarageArea'].fillna(0,inplace=True)

    # TODO: Additional cleaning

    if save_to_disk:
        # Save to a Pickle file for ease of transport
        housing.to_pickle(output_location)

    return housing


def add_features(housing, save_to_disk=True, output_location=config.HOUSING_PICKLE):
    """
    This function will add features to the housing dataframe.
    Input: housing (pandas dataframe)
    Output: pandas dataframe
    """

    housing['TotalLivingArea'] = housing['GrLivArea'] + housing['TotalBsmtSF'] - housing['BsmtUnfSF']
    housing['UnusedLotSize'] = housing['LotArea'] - housing['1stFlrSF']

    housing['HasPool'] = (housing['PoolArea']>0)
    
    housing['Toilets'] = housing['HalfBath'] + housing['FullBath']
    housing['Showers'] = housing['FullBath']
    housing['DecadeBuilt'] = housing['YearBuilt'].apply(lambda x: int(str(x)[:3]+'0'))
    

    if save_to_disk:
        # Save to a Pickle file for ease of transport
        housing.to_pickle(output_location)

    return housing