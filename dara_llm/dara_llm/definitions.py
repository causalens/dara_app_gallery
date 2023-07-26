import pandas as pd
from statsmodels.regression.linear_model import OLSResults

MODEL = OLSResults.load('data/ols_model.pickle')
COEFFICIENTS = pd.DataFrame(
    {
        'Feature': MODEL.params.index,
        'Coefficient': MODEL.params,
        'P-Values': MODEL.pvalues,
    }
).round(2)


DATA = pd.read_csv('data/advertising.csv')

RANDOM_STATE = 100
TRAIN_SIZE = 0.7
TEST_SIZE = 0.3
