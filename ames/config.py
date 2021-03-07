import os
from pathlib import Path

DATAPATH = Path('..') / 'data'
if not os.path.exists(DATAPATH):
    os.mkdir(DATAPATH)

HOUSING_CSV = DATAPATH / 'Ames_Housing_Price_Data.csv'
HOUSING_PICKLE = DATAPATH / 'housing_data.pickle'

if not os.path.exists(HOUSING_CSV):
    raise OSError(f'{HOUSING_CSV} does not exist! Please place in the data directory.')

# These are continuous variables in the dataset or created as features
CONTINUOUS_VARIABLES = ['1stFlrSF','2ndFlrSF', '3SsnPorch', 'BedroomAbvGr', 
                        'BsmtFinSF1', 'BsmtFinSF2', 'BsmtFullBath', 'BsmtHalfBath', 
                        'BsmtUnfSF', 'EnclosedPorch', 'Fireplaces', 'FullBath', 
                        'GarageArea', 'GarageCars', 'GarageYrBlt', 'GrLivArea', 
                        'HalfBath', 'KitchenAbvGr', 'LotArea', 'LotFrontage', 
                        'LowQualFinSF', 'MasVnrArea', 'MiscVal', 'MoSold', 'MSSubClass', 
                        'OpenPorchSF', 'OverallCond', 'OverallQual', 'PoolArea', 
                        'ScreenPorch', 'TotalBsmtSF', 'TotRmsAbvGrd', 'WoodDeckSF', 
                        'YearBuilt', 'YearRemodAdd', 'YrSold','DecadeBuilt', 'DecadeRemodel',
                        'TotalLivingArea','UnusedLotSize','HasBsmt', 'HasPool','HouseAge', 'HouseAgeSq',
                        'Toilets','Showers']

 # These are the variables the team has chosen to use based on EDA and experimentation
CHOSEN_VARIABLES = ['YrSold', 'LotFrontage','UnusedLotSize','HouseAgeSq','OverallQual','OverallCond',
                    'TotalLivingArea','Toilets','Showers','UpDownRatio','GarageArea','HasPool','HasBsmt']
VARS_TO_DUMMIFY = {'Neighborhood':'Nbhd','LotConfig':'LC','SaleCondition':'SC','BldgType':'BT','BsmtQual':'BQ'}

LASSO_VARS_FROM_CHOSEN = ['BQ_Ex','BQ_Gd', 'BT_1Fam', 'GarageArea', 'LotFrontage', 'Nbhd_Blmngtn',
                    'Nbhd_ClearCr', 'Nbhd_Crawfor', 'Nbhd_Gilbert', 'Nbhd_GrnHill', 'Nbhd_NoRidge',
                    'Nbhd_NridgHt', 'Nbhd_Somerst', 'Nbhd_StoneBr', 'OverallCond', 'OverallQual',
                    'SC_Partial', 'Showers', 'Toilets', 'TotalLivingArea', 'UnusedLotSize']
                    # Using an alpha of 4.028090452261307e-05 (Found via Alpha CV starting from Chosen Variables)

LASSO_VARS_FROM_ALL =['1stFlrSF', 'BQ_Ex', 'BT_1Fam', 'Fireplaces', 'GarageArea',
                      'GarageCars', 'GrLivArea', 'LotArea', 'Nbhd_ClearCr', 'Nbhd_Crawfor',
                      'Nbhd_GrnHill', 'Nbhd_NridgHt', 'Nbhd_Somerst', 'Nbhd_StoneBr',
                      'OverallCond', 'OverallQual', 'ScreenPorch', 'Showers', 'Toilets', 
                      'TotalBsmtSF', 'TotalLivingArea', 'WoodDeckSF', 'YearBuilt', 'YearRemodAdd']
                      # Using an alpha of 4.6308040201005025e-05 (Found via Alpha CV starting from all continous variables)