from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

import sys
sys.path.append('../ames')
import config
from data_prep import dummify

def lr_results(housing, regress_vars,dummy_dict):
    X = housing[regress_vars].copy()
    dummy_df = dummify(housing, dummy_dict, drop_first=True)
    X = pd.concat([X,dummy_df], axis=1)
    y = np.log(housing['SalePrice'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    reg = LinearRegression()
    folds = KFold(n_splits=10,shuffle=True, random_state=42)
    train_scores = cross_val_score(reg, X_train, y_train, scoring="neg_root_mean_squared_error", cv=folds)
    test_scores = cross_val_score(reg, X_test, y_test, scoring="neg_root_mean_squared_error", cv=folds)
    return -np.mean(train_scores), -np.mean(test_scores)