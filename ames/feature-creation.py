import pandas as pd

from ames import config

housing = pd.read_pickle(config.HOUSING_PICKLE)

housing['TotalLivingArea'] = housing['GrLivArea'] + housing['TotalBsmtSF'] - housing['BsmtUnfSF']
housing['UnusedLotSize'] = housing['LotArea'] - housing['1stFlrSF']

housing['HasPool'] = (housing['PoolArea']>0)
