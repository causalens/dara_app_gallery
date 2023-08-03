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
GREEN = '#4f9a5c'
RED = '#c25450'

VARIABLES_INSTANTIATION_CODE = """
    from dara_core import Variable                      

    num_1 = Variable(1)  
    num_2 = Variable(2)   
"""

VARIABLES_INPUT_CODE = """
    from dara.components import Stack, Text, Input               

    Stack(
        Text('Input first number:', bold=True),                         
        Input(value=num_1),
        direction='horizontal',
    )
    Stack(
        Text('Input second number:', bold=True),
        Input(value=num_2),
        direction='horizontal'
    )  
"""

VARIABLES_PARAGRAPH_CODE = """
    from dara.components import Paragraph, Text          

    Paragraph(
        Text('First number:', bold=True),
        Text(num_1)
    )
    Paragraph(
        Text('Second number:', bold=True),
        Text(num_2)
    )
"""

DERIVED_VARIABLE_CODE = """
    from typing import Union

    from dara.core import Variable, DerivedVariable
    from dara.components import Paragraph, Text, Card         

    def sum(a, b) -> Union[float, str]:
        try:
            return float(a) + float(b)
        except ValueError:
            return ' not calculable.'

    num_1 = Variable(1)
    num_2 = Variable(1)

    summation = DerivedVariable(func=sum, variables=[num_1, num_2])

    Card(
        Paragraph(
            Text('The sum of '),
            Text(num_1),
            Text('and '),
            Text(num_2),
            Text('is '),
            Text(summation)
        )
    )
"""

DERIVED_VARIABLE_WITH_DEPS_CODE = """
    rom typing import Union

    from dara.core import Variable, DerivedVariable
    from dara.components import Paragraph, Text, Card

    def sum(a, b) -> Union[float, str]:
        try:
            return float(a) + float(b)
        except ValueError:
            return ' not calculable.'
    
    num_1 = Variable(1)
    num_2 = Variable(1)

    summation_with_deps = DerivedVariable(func=sum, variables=[num_1, num_2], deps=[num_2])         

    Card(
        Paragraph(
            Text('The sum of '),
            Text(num_1),
            Text('and '),
            Text(num_2),
            Text('is '),
            Text(summation_with_deps)
        )
    )
"""

DERIVED_VARIABLE_WITH_TRIGGER_CODE = """
    from typing import Union

    from dara.core import Variable, DerivedVariable
    from dara.components import Paragraph, Text, Card, Button

    def sum(a, b) -> Union[float, str]:
        try:
            return float(a) + float(b)
        except ValueError:
            return ' not calculable.'

    num_1 = Variable(1)
    num_2 = Variable(1)

    summation_with_empty_deps = DerivedVariable(func=sum, variables=[num_1, num_2], deps=[])            

    Stack(
        Card(
            Paragraph(
                Text('The sum of '),
                Text(num_1),
                Text('and '),
                Text(num_2),
                Text('is '),
                Text(summation_with_empty_deps)
            )
        ),
        Button(
            'Recalculate Sum',
            onclick=summation_with_empty_deps.trigger(),
        ),
        direction='horizontal'
    )
"""

VARIABLES_AND_INPUT_CODE = """
    from dara.core import Variable
    from dara.components import Stack, Text, Input, Paragraph                

    num_1 = Variable(1)
    num_2 = Variable(1)

    Stack(
        Stack(
            Text('Input first number:', bold=True),                         
            Input(value=num_1),
            Text('Input second number:', bold=True),
            Input(value=num_2),
            direction='horizontal'
        ),
        Stack(
            Paragraph(
                Text('First number:', bold=True),
                Text(num_1)
            )
            Paragraph(
                Text('Second number:', bold=True),
                Text(num_2)
            ),
            direction='horizontal'
        )
    )
"""


PY_COMPONENTS_CODE = """
    from typing import Union
    from bokeh.plotting import figure

    from dara.components import Bokeh
    from dara.core import py_component, Variable, DerivedVariable
    from dara.core.definitions import ComponentInstance

    from dara_interactivity.definitions import GREEN, RED

    def sum(a, b) -> Union[float, None]:                                                                    
        try:
            return float(a) + float(b)
        except ValueError:
            return None

    num_1 = Variable(1)
    num_2 = Variable(1)

    summation = DerivedVariable(func=sum, variables=[num_1, num_2])

    @py_component
    def bar_plot(first_num: str, second_num: str, sum: Union[float, None]) -> ComponentInstance:
        try:
            first_num = float(first_num)
            second_num = float(second_num)
        except ValueError:
            return Stack(
                Text('Please make sure your inputs are numerical values.'),
                align='center'
            )
        labels = ['num_1', 'num_2', 'sum']
        values = [first_num, second_num, sum]
        colors=[GREEN if x >= 0 else RED for x in values]
        
        p = figure(title='Bar Plot', toolbar_location=None, y_range=labels, sizing_mode='stretch_both')
        p.hbar(y=['num_1', 'num_2', 'sum'], right=values, left=0, height=0.7, color=colors)

        return Bokeh(p, height='99%')

    bar_plot(num_1, num_2, summation)
"""

INPUT_INSTANTIATION_CODE = """
    from dara.core import Variable
    from dara.components import Stack, Input, Text           

    user_input = Variable('My text')
    
    Stack(
        Text('Please input some text:'),
        Input(value=user_input),
        direction='horizontal'
    )
"""

HORIZONTAL_CODE = """
    from dara.core import Variable
    from dara.components import Stack, Text, Heading             
    
    user_input = Variable('My text')

    Stack(
        Heading('Horizontal', level=3),
        Text(user_input)
    )
"""

BACKWARDS_CODE = """
    from dara.core import Variable, DerivedVariable
    from dara.components import Stack, Text, Heading             
    
    user_input = Variable('My text')
    backwards_input = DerivedVariable(lambda text: ''.join(reversed(text)), variables=[user_input])

    Stack(
        Heading('Backwards', level=3),
        Text(backwards_input)
    )
"""

VERTICAL_CODE = """
    from dara.core import Variable, py_component
    from dara.core.definitions import ComponentInstance
    from dara.components import Stack, Text, Heading                             
    
    user_input = Variable('My text')

    @py_component
    def my_py_component(input_str: str) -> ComponentInstance:
        # returns a varying component based on the input Variable
        vertical_text = Stack(scroll=True)
        for letter in input_str:
            vertical_text.append(Text(letter, font_size='9px'))
        return vertical_text

    Stack(
        Heading('Vertical', level=3),
        my_py_component(user_input)
    )
"""

HYPERPARAMETERS_CODE = """
    from dara.core import Variable
    from dara.components import Stack, Text, Select


    kernel_var = Variable(['linear', 'poly', 'rbf', 'sigmoid'])
    c_var = Variable([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5])
    gamma_var = Variable([5, 1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001])

    Stack(
        Text('Kernel:'),
        Select(
            items=['linear', 'poly', 'rbf', 'sigmoid'],
            value=kernel_var,
            multiselect=True
        ),
        Text('C:'),
        Select(
            items=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5],
            value=c_var,
            multiselect=True
        ),
        Text('Gamma:'),
        Select(
            items=[5, 1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001],
            value=gamma_var,
            multiselect=True
        ),
        direction='horizontal'
    )
"""

DERIVED_VARIABLE_WITH_TASK_CODE = """
    # tasks.py                                                                                              
    import pandas as pd

    from sklearn import svm
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    def grid_search(data: pd.DataFrame, kernels: list, c_list: list, gamma_list: list):
        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(columns=['species', '__index__']),
            data['species'],
            test_size=0.30
        )
        best_model, best_score = None, 0
        for kernel in kernels:
            for c in c_list:
                for gamma in gamma_list:
                    model = svm.SVC(C=c, kernel=kernel, gamma=gamma)
                    model.fit(X_train, y_train)
                    pred = model.predict(X_test)
                    score = accuracy_score(y_test, pred)
                    if score > best_score:
                        best_score = score
                        best_model = model
        
        return (y_test, best_model.predict(X_test))


    # expensive_calculations.py
    import pandas as pd
    from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
    from bokeh.palettes import Blues
    from bokeh.plotting import figure
    from bokeh.transform import transform
    from sklearn import datasets
    from sklearn.metrics import confusion_matrix

    from dara.components import Bokeh
    from dara.core import DataVariable, DerivedVariable, Variable, py_component
    from dara.core.definitions import ComponentInstance

    from dara_interactivity.tasks import grid_search

    iris = datasets.load_iris()
    target_names = iris.target_names
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['species'] = iris.target

    results = DerivedVariable(
        grid_search,
        variables=[DataVariable(data), kernel_var, c_var, gamma_var],
        run_as_task=True
    )

    @py_component
    def confusion_matrix_plot(results, target_names) -> ComponentInstance:
        truth, predictions = results
        df = pd.DataFrame(confusion_matrix(truth, predictions), index=target_names, columns=target_names)
        df.index.name = 'Actual'
        df.columns.name = 'Prediction'
        df = df.stack().rename('value').reset_index()

        mapper = LinearColorMapper(
            palette=Blues[9], low=df.value.min(), high=df.value.max()
        )
        p = figure(title=f"Confusion Matrix", sizing_mode='stretch_both',
                toolbar_location=None, x_axis_label='Predicted', y_axis_label='Actual',
                x_axis_location="above", x_range=target_names, y_range=target_names[::-1])
        p.rect(x="Actual", y="Prediction", width=1, height=1, source=df, line_color=None,
            fill_color=transform('value', mapper))

        color_bar = ColorBar(color_mapper=mapper, location=(0, 0), label_standoff=10,
                            ticker=BasicTicker(desired_num_ticks=3))
        p.add_layout(color_bar, 'right')

        return Bokeh(p, height='99%')

    confusion_matrix_plot(results, target_names)
"""

TASK_WITH_PROGRESS_BAR_CODE = """
    # tasks.py
    import time                                                                                                                 
    import pandas as pd

    from sklearn import svm
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    from dara.core import ProgressUpdater, track_progress

    # injecting ProgressUpdater object into the task
    @track_progress
    def grid_search(data: pd.DataFrame, kernels: list, c_list: list, gamma_list: list, updater: ProgressUpdater):
        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(columns=['species', '__index__']),
            data['species'],
            test_size=0.30
        )
        best_model, best_score = None, 0
        for i, kernel in enumerate(kernels):
            for c in c_list:
                for gamma in gamma_list:
                    model = svm.SVC(C=c, kernel=kernel, gamma=gamma)
                    model.fit(X_train, y_train)
                    pred = model.predict(X_test)
                    score = accuracy_score(y_test, pred)
                    if score > best_score:
                        best_score = score
                        best_model = model
            time.sleep(1) # arbitrarily making task longer to show progress bar
            # sending iterative updates for the progress bar
            updater.send_update((i / len(kernels)) * 100, f'Step {i}')
        updater.send_update(100, 'Done')
        return (y_test, best_model.predict(X_test))


    # expensive_calculations.py
    import pandas as pd
    from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
    from bokeh.palettes import Blues
    from bokeh.plotting import figure
    from bokeh.transform import transform
    from sklearn import datasets
    from sklearn.metrics import confusion_matrix

    from dara.components import Bokeh
    from dara.core import DataVariable, DerivedVariable, Variable, py_component
    from dara.core.definitions import ComponentInstance

    from dara_interactivity.tasks import grid_search

    iris = datasets.load_iris()
    target_names = iris.target_names
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['species'] = iris.target

    results = DerivedVariable(
        grid_search,
        variables=[DataVariable(data), kernel_var, c_var, gamma_var],
        run_as_task=True
    )

    @py_component(track_progress=True)
    def confusion_matrix_plot(results, target_names) -> ComponentInstance:
        truth, predictions = results
        df = pd.DataFrame(confusion_matrix(truth, predictions), index=target_names, columns=target_names)
        df.index.name = 'Actual'
        df.columns.name = 'Prediction'
        df = df.stack().rename('value').reset_index()

        mapper = LinearColorMapper(
            palette=Blues[9], low=df.value.min(), high=df.value.max()
        )
        p = figure(title=f"Confusion Matrix", sizing_mode='stretch_both',
                toolbar_location=None, x_axis_label='Predicted', y_axis_label='Actual',
                x_axis_location="above", x_range=target_names, y_range=target_names[::-1])
        p.rect(x="Actual", y="Prediction", width=1, height=1, source=df, line_color=None,
            fill_color=transform('value', mapper))

        color_bar = ColorBar(color_mapper=mapper, location=(0, 0), label_standoff=10,
                            ticker=BasicTicker(desired_num_ticks=3))
        p.add_layout(color_bar, 'right')

        return Bokeh(p, height='99%')

    confusion_matrix_plot(results, target_names)
"""
