import os
from pathlib import Path

DATAPATH = Path('..') / 'data'
if not os.path.exists(DATAPATH):
    os.mkdir(DATAPATH)

HOUSING_CSV = DATAPATH / 'Ames_Housing_Price_Data.csv'
HOUSING_PICKLE = DATAPATH / 'housing_data.pickle'

if not os.file_exists(HOUSING_CSV):
    raise FileError(f'{HOUSING_CSV} does not exist! Please place in the data directory.')
