import pandas as pd
from sklearn.model_selection import train_test_split

from ames import config

housing_df = pd.read_pickle(config.HOUSING_PICKLE)

X = housing_df.drop('SalePrice')
y = housing_df.loc[:, 'SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20, random_state=42)
