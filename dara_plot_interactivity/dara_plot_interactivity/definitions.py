import os
import json
import pandas as pd

DATA_ROOT = os.environ.get('DATA_ROOT', './data')

DATA = pd.read_csv(os.path.join(DATA_ROOT, 'sanctions.csv'))

PLOT_FEATURES = [col for col in DATA.columns if col not in ['area', 'year']]
AREA_FEATURE = 'area'
YEAR_FEATURE = 'year'

with open(os.path.join(DATA_ROOT, 'countries.json'), 'r') as f:
    COUNTRIES = json.load(f)
