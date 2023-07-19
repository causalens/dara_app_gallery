import os
import pandas as pd

from dara.core import DataVariable

DATA_ROOT = os.environ.get('DATA_ROOT', './data')

data = pd.read_csv(os.path.join(DATA_ROOT, '401k.csv'), index_col=0)
data['Income Bracket'] = pd.qcut(data['Income'], 4, labels=['Below Q1', 'Above Q1', 'Above Q2', 'Above Q3'])

DATA = DataVariable(data)
FEATURES = [*data.columns]
CATEGORICAL_FEATURES = [*data.select_dtypes(include=['object', 'category']).columns]

GREEN = '#4f9a5c'
RED = '#c25450'
