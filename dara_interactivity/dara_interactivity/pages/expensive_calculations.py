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
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
from bokeh.palettes import Blues
from bokeh.plotting import figure
from bokeh.transform import transform
from sklearn import datasets
from sklearn.metrics import confusion_matrix

from dara.core import DataVariable, DerivedVariable, Variable, py_component
from dara.core.definitions import ComponentInstance
from dara.components import Stack, Bokeh, Grid, Text, Select, Heading

from dara_interactivity.custom_components import information_button, code_modal
from dara_interactivity.definitions import (
    TASK_WITH_PROGRESS_BAR_CODE, DERIVED_VARIABLE_WITH_TASK_CODE, HYPERPARAMETERS_CODE
)
from dara_interactivity.tasks import grid_search


@py_component(track_progress=True)
def confusion_matrix_plot(results: tuple, target_names) -> ComponentInstance:
    """
    Constructs a confusion matrix plot from the results of a Support Vector Machine prediction

    :param results: tuple of arrays representing the true and predicted values
    :param target_names: the names representing the different classes of the classification dataset
    :return ComponentInstance
    """
    truth, predictions = results
    df = pd.DataFrame(confusion_matrix(truth, predictions), index=target_names, columns=target_names)
    df.index.name = 'Actual'
    df.columns.name = 'Prediction'
    df = df.stack().rename('value').reset_index()

    mapper = LinearColorMapper(
        palette=Blues[9], low=df.value.min(), high=df.value.max()
    )
    p = figure(title='Confusion Matrix', sizing_mode='stretch_both',
               toolbar_location=None, x_axis_label='Predicted', y_axis_label='Actual',
               x_axis_location='above', x_range=target_names, y_range=target_names[::-1])
    p.rect(x='Actual', y='Prediction', width=1, height=1, source=df, line_color=None,
           fill_color=transform('value', mapper))

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0), label_standoff=10,
                         ticker=BasicTicker(desired_num_ticks=3))
    p.add_layout(color_bar, 'right')

    return Bokeh(p, height='99%')


def expensive_calculations_page() -> ComponentInstance:
    """
    Constructs the layout of the page.

    The page displays a some instructional text, along with modals displaying code snippets.

    :return: ComponentInstance
    """
    # Load data from sklearn
    iris = datasets.load_iris()
    target_names = iris.target_names
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['species'] = iris.target

    # Define hyperparameter Variables
    kernel_var = Variable(['linear', 'poly', 'rbf', 'sigmoid'])
    c_var = Variable([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5])
    gamma_var = Variable([5, 1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001])
    results = DerivedVariable(
        grid_search,
        variables=[DataVariable(data), kernel_var, c_var, gamma_var],
        run_as_task=True
    )

    # Define Variables that show/hide the code modals
    show_hyperparameters_instantiation = Variable(False)
    show_dv_task_instantiation = Variable(False)
    show_progress_bar_implementation = Variable(False)

    return Stack(
        Heading('Heavy CPU Bound Calculations'),
        Text('Click on the ? buttons to show the underlying code in which the information is referring to.', italic=True),
        Grid(
            Grid.Row(
                Grid.Column(
                    Text('CPU bound calculations are calculations that require intensive processing. \
                          Typically this will include machine learning calculations or expensive data manipulations. \
                          Due to Python\'s Global Interpreter Lock, it helps to offload heavy calculations to \
                          seperate processes. Offloading computation to another process can get complicated \
                          fairly quickly, so Dara provides an easy way define certain functions as tasks \
                          that can be offloaded to another process outside the main one running your web app.'),
                    span=11
                ),
            ),
            padding='10px'
        ),
        Grid(
            Grid.Row(
                Grid.Column(                        
                    Stack(
                        Stack(
                            Text('Kernel:', width='7%'),
                            Select(
                                items=['linear', 'poly', 'rbf', 'sigmoid'],
                                value=kernel_var,
                                multiselect=True
                            ),
                            direction='horizontal'
                        ),
                        Stack(
                            Text('C:', width='7%'),
                            Select(
                                items=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5],
                                value=c_var,
                                multiselect=True
                            ),
                            direction='horizontal'
                        ),
                        Stack(
                            Text('Gamma:', width='7%'),
                            Select(
                                items=[5, 1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001],
                                value=gamma_var,
                                multiselect=True
                            ),
                            direction='horizontal'
                        )
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_hyperparameters_instantiation),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Grid.Column(
                    Stack(confusion_matrix_plot(results, target_names)),
                    span=6
                ),
                Grid.Column(
                    Grid(
                        Grid.Row(
                            Grid.Column(
                                Stack(
                                    Text('In this example, the user can choose some hyperparameters for doing a grid search on a \
                                          Support Vector Machine. It will use these hyperparameters to choose the best model \
                                          and display a confusion matrix. Depending on how many choices there are it could be \
                                          helpful to offload this calculation to a separate process. \
                                          To use this feature you must put the definition of the resolver of the \
                                          DerivedVariable into a separate file. This example will define the resolver in \
                                          tasks.py.'),
                                    justify='center'
                                ),
                            ),
                            Grid.Column(
                                Stack(
                                    information_button(show_dv_task_instantiation),
                                    justify='center',
                                    align='center'
                                ),
                                span=2
                            )
                        ),
                        Grid.Row(
                            Grid.Column(
                                Stack(
                                    Text('It is often beneficial to provide the end-user with live progress updates \
                                          on a long-running task. Dara provides a simple API to send progress updates \
                                          from inside a task and display them in the form of a progress bar while a \
                                          task is running, rather than displaying a plain loading spinner which is the default. \
                                          This involves wrapping your task function in a track_progress decorator while setting \
                                          track_progress to True in the py_component that is waiting for the task results.'),
                                    justify='center'
                                )
                            ),
                            Grid.Column(
                                Stack(
                                    information_button(show_progress_bar_implementation),
                                    justify='center',
                                    align='center'
                                ),
                                span=2
                            )
                        )
                    ),
                    span=6
                ),
            ),
            padding='10px'
        ),
        code_modal(HYPERPARAMETERS_CODE, show_hyperparameters_instantiation),
        code_modal(DERIVED_VARIABLE_WITH_TASK_CODE, show_dv_task_instantiation),
        code_modal(TASK_WITH_PROGRESS_BAR_CODE, show_progress_bar_implementation),
    )
