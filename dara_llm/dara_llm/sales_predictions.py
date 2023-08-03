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
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

from dara.components import Card, Paragraph, Plotly, Select, Stack, Table, Text
from dara.core import ComponentInstance, DataVariable, Variable, py_component
from dara.core.visual.themes import Light

from dara_llm.chatbox import ChatBox
from dara_llm.definitions import (
    COEFFICIENTS,
    DATA,
    MODEL,
    RANDOM_STATE,
    TEST_SIZE,
    TRAIN_SIZE,
)


@py_component
def ScatterPlot(
    x: str, y: str, data: pd.DataFrame, feature_fit: bool = False
) -> ComponentInstance:
    """
    A component that plots a scatter plot of x vs y.
    If x is a independent variable of the model and feature_fit is True,
    the plot will include a line of fit.

    :param x: The column to plot on the x axis.
    :param y: The column to plot on the y axis.
    :param data: The data.
    :param feature_fit: Whether to plot a line of fit from the coefficients of the OLS model.
    """
    plot_data = data.copy()

    # Scatter plot of feature vs target.
    fig = px.scatter(plot_data, x=x, y=y, title=f'{x} vs. {y}')
    fig.update_layout(margin={'l': 10, 'r': 0, 'b': 10, 't': 40})
    fig.update_traces(marker_color=Light.colors.violet)

    # Plot line of fit for that particular feature if specified.
    if feature_fit and x in MODEL.params.index:
        plot_data['Fit'] = (
            MODEL.params['const'] + plot_data[x] * MODEL.params[x]
        )
        fig.add_trace(px.line(plot_data, x, 'Fit').data[0])
        fig.update_traces(line_color=Light.colors.orange)

    return Plotly(fig, min_height='350px')


def ModelDetails() -> ComponentInstance:
    """A component that displays the model details like the independent variable coefficients."""
    return Card(
        Text(
            f'The Ordinary Least Squares model was trained on {int(len(DATA) * TRAIN_SIZE)} \
              entries and it predicts the data to fit to the following equation:'
        ),
        Paragraph(
            Text('Sales', bold=True),
            Text('='),
            Text(f"{round(MODEL.params['TV'], 2)} ×"),
            Text('TV', bold=True),
            Text(f"+ {round(MODEL.params['Radio'], 2)} ×"),
            Text('Radio', bold=True),
            Text(f"+ {round(MODEL.params['Newspaper'], 2)} ×"),
            Text('Newspaper', bold=True),
            Text(f"+ {round(MODEL.params['const'], 2)}"),
            align='center',
        ),
        Table(
            data=DataVariable(COEFFICIENTS[COEFFICIENTS['Feature'] != 'const'])
        ),
        title='Model Details',
    )


def ModelPerformance() -> ComponentInstance:
    """A component that displays information about the model's performance."""
    # Predict Sales for the test data.
    _, x_test, _, y_test = train_test_split(
        DATA[['TV', 'Radio', 'Newspaper']],
        DATA['Sales'],
        train_size=TRAIN_SIZE,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )
    x_test = sm.add_constant(x_test)
    y_pred = MODEL.predict(x_test)

    # Run residual analysis on test set predictions.
    res: pd.DataFrame = (y_test - y_pred).to_frame()
    res = res.rename(columns={0: 'Value'})
    fig = px.histogram(
        res,
        x='Value',
        color_discrete_sequence=[Light.colors.orange],
        title='Residual Distribution',
    )

    # Prepare data for scatter plot.
    plot_data = pd.DataFrame(
        {'Sales (Predictions)': y_pred, 'Residuals': res['Value'].values}
    )

    # Define performance metrics table.
    performance_stats = pd.DataFrame(
        {
            'F Statistic': [MODEL.fvalue],
            'R Squared': [MODEL.rsquared],
            'Log Likelihood': [MODEL.llf],
        }
    ).round(2)

    return Card(
        Table(data=DataVariable(performance_stats), min_height='120px'),
        Stack(
            Plotly(fig, min_height='400px'),
            ScatterPlot('Sales (Predictions)', 'Residuals', plot_data),
            direction='horizontal',
        ),
        title='Model Performance',
    )


def SalesPredictionsPage():
    """
    A page-sized component that displays the problem, dataset, model details, and model performance.
    This page also contains a button on the top-right corner that provides an overlay in which
    users can query ChatGPT about the model.
    """
    selected_feature = Variable('TV')

    return Stack(
        ChatBox(),
        Stack(
            Card(
                Stack(
                    Text(
                        'This page is a summary of an OLS model that predicts Sales based on \
                        marketing spend in TV, Radio, and Newspaper.'
                    ),
                    Text(
                        'Click on the chat box on the top right to query ChatGPT with questions \
                        you may have about the model or the data. There are some predefined questions \
                        that you may try or you can create a custom query.'
                    ),
                    scroll=True,
                    gap='0.2rem',
                ),
                accent=True,
                title='Sales Prediction',
                width='30%',
            ),
            Table(data=DataVariable(data=DATA)),
            direction='horizontal',
            min_height='310px',
        ),
        Stack(
            Card(
                Stack(
                    Text('Select a feature', width='25%'),
                    Select(
                        items=['TV', 'Radio', 'Newspaper'],
                        value=selected_feature,
                    ),
                    direction='horizontal',
                    hug=True,
                ),
                ScatterPlot(selected_feature, 'Sales', DATA, feature_fit=True),
                hug=True,
                width='calc(50% - 0.75rem)',
            ),
            ModelDetails(),
            direction='horizontal',
        ),
        ModelPerformance(),
        scroll=True,
    )
