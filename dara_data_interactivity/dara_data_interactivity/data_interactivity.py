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
from typing import List
from bokeh.palettes import Blues

import numpy as np
import pandas as pd

from dara.core import py_component, UpdateVariable, Variable, DataVariable
from dara.core.definitions import ComponentInstance
from dara.components import Bokeh, Stack, Table, Select, Grid, Spacer, Card, Text, Heading

from dara_data_interactivity.definitions import DATA, FEATURES, CATEGORICAL_FEATURES, GREEN, RED
from dara_data_interactivity.plotting_utils import plot_distribution


class DataInteractivityPage:
    def __init__(self) -> None:
        self.selected_rows = Variable([])
        self.graph_view = Variable('Total Wealth')

    def __call__(self) -> ComponentInstance:
        """
        Constructs the layout of the page.

        The page displays a Table of the data with customized formatting along with distribution plots
        and descriptive statistics of the selected Table rows.

        :return: ComponentInstance
        """
        return Stack(
            Heading('Explore Your Dataset', level=3),
            Text(
                'Click on an individual row to see where this datapoint lies in the total data distribution. \
                Or click on multiple datapoints to view the distribution amongst these individuals.',
                italic=True
            ),
            Stack(
                Table(
                    data=DATA,
                    columns=self.table_columns,
                    onclick_row=UpdateVariable(
                        resolver=lambda ctx: ctx.inputs.new, variable=self.selected_rows),
                    multi_select=False,
                ),
                height='40%'
            ),
            Stack(
                self.plot_selected_rows(self.selected_rows, self.graph_view, DATA),
                self.descriptive_stats(self.selected_rows),
                direction='horizontal'    
            ),
        )

    @property
    def table_columns(self) -> List[dict]:
        """ Applies formatting to the columns within the Table """
        columns = []
        for feature in FEATURES:
            col = {
                'col_id': feature,
                'label': feature,
                'filter': Table.TableFilter.NUMERIC  # allowing to filter by numeric searches
            }

            # color coding income brackets lighter (lower income) -> darker (higher income)
            if feature == 'Income Bracket':
                col['formatter'] = {
                    'type': Table.TableFormatterType.BADGE,
                    'badges': {
                        'Below Q1': {'color': Blues[5][1], 'label': 'Below Q1'},
                        'Above Q1': {'color': Blues[5][2], 'label': 'Above Q1'},
                        'Above Q2': {'color': Blues[5][3], 'label': 'Above Q2'},
                        'Above Q3': {'color': Blues[5][4], 'label': 'Above Q3'},
                    }
                }
                col['filter'] = Table.TableFilter.TEXT
            # giving Y/N features green and red badges respectively
            elif feature in CATEGORICAL_FEATURES:
                col['formatter'] = {
                    'type': Table.TableFormatterType.BADGE,
                    'badges': {
                        'Y': {'color': GREEN, 'label': 'Yes'},
                        'N': {'color': RED, 'label': 'No'},
                    }
                }
                # updating Y/N features to filter by text since they are not numeric
                col['filter'] = Table.TableFilter.TEXT
            # marking entries in Total Wealth red if individual is in any kind of debt
            elif feature in ['Total Wealth', 'Net Financial Assets']:
                col['formatter'] = {
                    'type': Table.TableFormatterType.THRESHOLD,
                    'thresholds': [
                        {
                            'color': RED,
                            'bounds': (-10000000000000, -0.01)
                        }
                    ]
                }

            # pinning some columns to the left so they are always visible
            if feature == 'Eligible for 401K' or feature == 'Income Bracket':
                col['sticky'] = 'left'

            columns.append(col)
        return columns

    @py_component
    def plot_selected_rows(self, rows: List[dict], view: str, data: pd.DataFrame) -> ComponentInstance:
        """
        Plots a distribution plot of the selected variable.

        If one individual from the table is selected it will plot the whole data and highlight the individual
        in a different color. If multiple individuals are selected it will plot the collective distributions of
        the individuals chosen.

        :param rows: the information from the row(s) selected in the Table
        :param view: the feature chosen of which to view the distribution
        :param data: DataFrame hosting the data in question
        :return: ComponentInstance
        """
        if rows == []:
            # display nothing if rows haven't been selected
            return Stack()

        if len(rows) == 1:
            graph = plot_distribution(data, view, rows[0])
            help_text = 'Bars that are orange indicate that the selected data point lives within this range.'
        else:
            graph = plot_distribution(pd.DataFrame(rows), view)
            help_text = ''
        return Stack(
            Stack(
                Text('Variable:'),
                Select(value=self.graph_view, items=FEATURES),
                direction='horizontal',
                height='7%'
            ),
            Bokeh(graph),
            Text(help_text, italic=True),
            height='100%'
        )

    @py_component
    def descriptive_stats(self, rows: List[dict]) -> ComponentInstance:
        """
        Displays a Table with the descriptive statistics of the selected row(s).

        :param rows: the information from the row(s) selected in the Table
        :return: ComponentInstance
        """
        if rows == []:
            # display nothing if rows haven't been selected
            return Stack()

        table_data = pd.DataFrame(rows)
        numerical_stats = table_data.describe(include=np.number).reset_index()
        categorical_stats = table_data.describe(include=['O']).reset_index()

        return Stack(
            Table(
                data=DataVariable(categorical_stats),
                columns=[*categorical_stats.columns],
            ),
            Table(
                data=DataVariable(numerical_stats),
                columns=[*numerical_stats.columns],
            ),
        )
