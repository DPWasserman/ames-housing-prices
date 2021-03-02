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
                        'TotalLivingArea','UnusedLotSize','HasPool','HouseAge', 'HouseAgeSq',
                        'Toilets','Showers']

 # These are the variables the team has chosen to use based on EDA and experimentation
CHOSEN_VARIABLES = ['LotFrontage','UnusedLotSize','HouseAge','HouseAgeSq','OverallQual','OverallCond',
                    'GrLivArea','TotalLivingArea','Toilets','Showers','UpDownRatio','GarageArea','HasPool']
VARS_TO_DUMMIFY = {'Neighborhood':'Nbhd','LotConfig':'LC','SaleCondition':'SC','BldgType':'BT','BsmtQual':'BQ'}