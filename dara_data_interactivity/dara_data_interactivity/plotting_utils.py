from collections import defaultdict
from typing import Union
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Blues

import numpy as np
import pandas as pd

from dara_data_interactivity.definitions import CATEGORICAL_FEATURES, GREEN, RED


def _categorical_bar_plot(data: pd.DataFrame, feature: str, individual: Union[None, dict] = None):
    """
    Plots a horizontal bar plot of the value counts of a categorical variable

    :param data: DataFrame hosting the data in question
    :param feature: the feature in which the distribution of will be plotted
    :param individual: optional individual datapoint to be highlighted in the distribution plot
    :return: the Bokeh figure to be plotted by the Bokeh extension
    """
    value_counts = data[feature].value_counts()
    hist_data = pd.DataFrame({
        feature: [*value_counts.index],
        'count': value_counts.values
    })
    if individual is not None:
        # highlighting individual in coral
        color_dict = defaultdict(lambda: 'steelblue')
        color_dict[individual[feature]] = 'coral'
        hist_data['color'] = hist_data[feature].map(color_dict)

        title = f'{feature} Distribution (Whole Dataset)'
    else:
        if feature == 'Income Bracket':
            # color coding Income Bracket in blue gradient as in the table
            hist_data['color'] = hist_data[feature].map({
                'Below Q1': Blues[4][0],
                'Above Q1': Blues[4][1],
                'Above Q2': Blues[4][2],
                'Above Q3': Blues[4][3]
            })
        else:
            # color coding Y/N features in green/red as in the table
            hist_data['color'] = hist_data[feature].map({'Y': GREEN, 'N': RED})

        title = f'{feature} Distribution (Selected Individuals)'

    p = figure(title=title, toolbar_location=None, height=225, y_range=hist_data[feature],
               tools='hover', tooltips='@{%s}: @count' % feature)
    p.hbar(y=feature, right='count', left=0, source=ColumnDataSource(hist_data),
           line_color='white', height=0.8, color='color')

    return p


def _continuous_histogram(data: pd.DataFrame, feature: str, individual: Union[None, dict] = None):
    """
    Plots a histogram of a continuous variable

    :param data: DataFrame hosting the data in question
    :param feature: the feature in which the distribution of will be plotted
    :param individual: optional individual datapoint to be highlighted in the distribution plot
    :return: the Bokeh figure to be plotted by the Bokeh extension
    """

    hist, edges = np.histogram(data[feature].dropna(), bins=10)
    hist_data = pd.DataFrame({
        feature: hist,
        'left': edges[:-1],
        'right': edges[1:]
    })

    if individual is not None:
        # highlighting individual in coral
        colors = []
        for _, row in hist_data.iterrows():
            if individual[feature] > row['left'] and individual[feature] < row['right']:
                colors.append('coral')
            else:
                colors.append('steelblue')
        hist_data['color'] = colors

        title = f'{feature} Distribution (Whole Dataset)'
    else:
        hist_data['color'] = ['steelblue'] * len(hist)

        title = f'{feature} Distribution (Selected Individuals)'

    p = figure(title=title, toolbar_location=None, height=225, sizing_mode='stretch_width',
               tools='hover', tooltips=[(feature, '@{%s}{0.00}' % feature)])
    p.quad(bottom=0, top=feature, left='left', right='right', source=ColumnDataSource(hist_data), color='color')

    p.yaxis.formatter.use_scientific = False
    p.xaxis.formatter.use_scientific = False

    return p


def plot_distribution(data: pd.DataFrame, feature: str, individual: Union[None, dict] = None):
    """
    Plots the correct type of distribution plot based on whether the feature is categorical or continuous

    :param data: DataFrame hosting the data in question
    :param feature: the feature in which the distribution of will be plotted
    :param individual: optional individual datapoint to be highlighted in the distribution plot
    :return: the Bokeh figure to be plotted by the Bokeh extension
    """
    if feature in CATEGORICAL_FEATURES:
        return _categorical_bar_plot(data, feature, individual)
    else:
        return _continuous_histogram(data, feature, individual)
