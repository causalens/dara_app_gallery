"""
Copyright 2023 Impulse Innovations Limited


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import json
import pandas as pd

DATA_ROOT = os.environ.get('DATA_ROOT', './data')

DATA = pd.read_csv(os.path.join(DATA_ROOT, 'gdp.csv'), index_col=0)

PLOT_FEATURES = [col for col in DATA.columns if col not in ['area', 'year']]
AREA_FEATURE = 'area'
YEAR_FEATURE = 'year'

with open(os.path.join(DATA_ROOT, 'countries.json'), 'r') as f:
    COUNTRIES = json.load(f)
