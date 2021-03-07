import numpy as np
import pandas as pd

import sys
sys.path.append('../ames')
import config

def clean(housing_location, save_to_disk=True, output_location=config.HOUSING_PICKLE):

    housing = pd.read_csv(housing_location)

    # Drop index column
    if 'Unnamed: 0' in housing.columns:
        housing.drop('Unnamed: 0',axis=1, inplace=True)

    # Drop duplicate record(s)
    housing = housing.loc[~housing.duplicated(),:]

    # Impute NAs with zeros (Continuous Variable)
    continuous_var = ['BsmtFinSF1','BsmtFinSF2','BsmtFullBath','BsmtHalfBath',
                    'BsmtUnfSF','GarageArea','GarageCars',
                    'LotFrontage','MasVnrArea','TotalBsmtSF']
    for var in continuous_var:
        housing[var].fillna(0, inplace=True)

    # Impute NAs with None (Qualitative Variable)
    housing['BsmtQual'].fillna('None', inplace=True)

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

    housing['HasPool'] = np.where(housing['PoolArea']>0, 1, 0)
    housing['HasBsmt'] = np.where(housing['BsmtQual']=='None', 0, 1)

    housing['Toilets'] = housing['HalfBath'] + housing['FullBath'] + housing['BsmtFullBath'] + housing['BsmtHalfBath']
    housing['Showers'] = housing['FullBath'] + housing['BsmtFullBath']

    housing['DecadeBuilt'] = housing['YearBuilt'].apply(lambda x: (x//10 * 10))
    housing['DecadeRemodel'] = housing['YearBuilt'].apply(lambda x: (x//10 * 10))
    
    maxYear = max(housing['YearBuilt'])
    housing['HouseAge'] = maxYear - housing['YearBuilt'] + 1
    housing['HouseAgeSq'] = housing['HouseAge'] ** 2
    housing['HouseAgeLog'] = np.log(housing['HouseAge'])

    housing['UpDownRatio'] = housing['2ndFlrSF']/housing['1stFlrSF'] # Ratio of area upstairs to area downstairs

    if save_to_disk:
        # Save to a Pickle file for ease of transport
        housing.to_pickle(output_location)

    return housing

def dummify(housing, dict_of_dummy_var, drop_first=False):
    """
    Purpose: Dummify categorical variables
    Inputs: housing = DataFrame
            dict_of_dummy_var = Dict with name of categorical variable as key and prefix as value
            drop_first = Boolean to determine whether to drop the first categorical dummy
    Output: DataFrame which should be joined with another dataframe to get all the features
    """
    X = pd.DataFrame()

    if not dict_of_dummy_var:
        return X

    for var, prefix in dict_of_dummy_var.items():
        dummy_df = pd.get_dummies(housing[var], prefix=prefix, drop_first=drop_first)
        X = pd.concat([X, dummy_df], axis=1)

    return X