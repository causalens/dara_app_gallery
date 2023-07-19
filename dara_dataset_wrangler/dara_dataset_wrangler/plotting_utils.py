from enum import Enum

import numpy
import pandas
from scipy.stats import gaussian_kde

from bokeh.plotting import figure

from dara.core import py_component
from dara.core.definitions import ComponentInstance
from dara.components import Stack, Text, Bokeh


class ColumnType(Enum):
    CATEGORICAL = 'categorical'
    DATETIME = 'datetime'
    NUMERICAL = 'numerical'


def infer_column_type(data: pandas.DataFrame, col: str) -> ColumnType:
    """
    Get ColumnType for a given column of a dataframe.

    Returns None for datetime columns if treat_datetime_as_numerical is True.
    Otherwise treats datatime as numerical.

    :param data: dataset as a pandas dataframe
    :param col: column to get type for
    """
    series_values = data[col].values

    # This inference logic follows Dataset.from_dataframe column inference process
    if isinstance(series_values.dtype, numpy.dtype):
        if numpy.issubdtype(series_values.dtype, numpy.number):
            return ColumnType.NUMERICAL
        elif numpy.issubdtype(series_values.dtype, numpy.datetime64):
            return ColumnType.DATETIME
        else:
            return ColumnType.CATEGORICAL
    else:
        return ColumnType.CATEGORICAL


def plot_column_numerical(dataset: pandas.DataFrame, x: str, **kwargs) -> figure:
    df = dataset.copy()
    df = df[[x]].dropna()
    lin = numpy.linspace(df[x].min(), df[x].max(), 500)

    p = figure(
        title=f'Distribution - {x}',
        tools='',
        toolbar_location=None,
        sizing_mode='stretch_both',
        **kwargs,
    )
    p.toolbar.logo = None
    p.toolbar_location = 'above'

    p.yaxis.formatter.use_scientific = False
    p.xaxis.formatter.use_scientific = False

    pdf = gaussian_kde(df[x].dropna())
    y = pdf(lin)
    p.line(
        lin,
        y,
        alpha=0.6,
        line_width=3,
    )

    return p


def plot_column_categorical(dataset: pandas.DataFrame, x: str, **kwargs) -> figure:
    # clean infinities
    df = dataset.copy()
    df = df[[x]].dropna().astype(str)

    values_counts = df[x].value_counts()

    p = figure(
        x_range=sorted(list(df[x].unique())),
        title=f'Histogram - {x}',
        toolbar_location=None,
        tools='',
        sizing_mode='stretch_both',
        **kwargs,
    )

    p.vbar(x=values_counts.index, top=values_counts.values, width=0.5)

    p.toolbar.logo = None
    p.toolbar_location = 'above'

    p.xgrid.grid_line_color = None

    return p


def render_input_plot(dataset: pandas.DataFrame, column: str) -> ComponentInstance:
    """
    Render an input plot for a given column of a dataset.

    :param dataset: input dataset
    :param column: column name
    """
    if column is None:
        return Stack(Text('Select variable to see the plot.'), align='center')

    column_type = infer_column_type(dataset, column)

    if column_type == ColumnType.CATEGORICAL:
        fig = plot_column_categorical(dataset, column)
    elif column_type == ColumnType.NUMERICAL:
        fig = plot_column_numerical(dataset, column)
    else:
        return Stack(Text('Datetime columns cannot be plotted'))

    if fig is None:
        return Stack(Text('Error rendering this part of the report.'), align='center')
    return Bokeh(fig)


@py_component
def plot_column(dataset: pandas.DataFrame, selected_column: str) -> ComponentInstance:
    """
    Select and plot a column
    """
    if len(dataset.index) < 2:
        return Stack(Text('Plots are available for datasets with at least two rows'))

    return render_input_plot(dataset, selected_column)
