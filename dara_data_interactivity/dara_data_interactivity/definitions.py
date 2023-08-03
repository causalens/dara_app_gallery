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
