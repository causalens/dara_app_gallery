from bokeh.plotting import figure
from typing import Union

from dara.core import py_component, Variable, DerivedVariable
from dara.core.definitions import ComponentInstance
from dara.components import Stack, Bokeh, Grid, Text, Paragraph, Input, Spacer, Heading

from dara_interactivity.custom_components import information_button, code_modal
from dara_interactivity.definitions import GREEN, RED, PY_COMPONENTS_CODE, VARIABLES_AND_INPUT_CODE


@py_component
def bar_plot(first_num: str, second_num: str, sum: Union[float, None]) -> ComponentInstance:
    """
    Constructs a bar plot of two numbers and their sum with colors depending on the numbers' signs.

    :param first_num: first number to be plotted
    :param second_num: second number to be plotted
    :param sum: third number to be plotted (is the sum of first_num and second_num)
    :return ComponentInstance
    """
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
    colors = [GREEN if x >= 0 else RED for x in values]

    p = figure(title='Bar Plot', toolbar_location=None, y_range=labels, sizing_mode='stretch_both')
    p.hbar(y=['num_1', 'num_2', 'sum'], right=values, left=0, height=0.7, color=colors)

    return Bokeh(p, height='99%')


def sum(a: str, b: str) -> Union[float, None]:
    """
    Calculates the sum of two inputs, first converting them to floats.

    :param a: first string input
    :param b: second string input
    :return float or None if the inputs cannot be converted to floats
    """
    try:
        return float(a) + float(b)
    except ValueError:
        return None


def pycomponents_page() -> ComponentInstance:
    """
    Constructs the layout of the page.

    The page displays a some instructional text, along with modals displaying code snippets.

    :return: ComponentInstance
    """
    num_1 = Variable(1)
    num_2 = Variable(1)

    summation = DerivedVariable(func=sum, variables=[num_1, num_2])

    # Define Variables that show/hide the code modals
    show_vars_and_inputs_definitions = Variable(False)
    show_py_component_definition = Variable(False)

    return Stack(
        Heading('py_components'),
        Text('Click on the ? buttons to show the underlying code in which the information is referring to.', italic=True),
        Grid(
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('Input first number:', bold=True),
                        Spacer(size='2%'),
                        Input(value=num_1),
                        direction='horizontal',
                    ),
                    span=6
                ),
                Grid.Column(
                    Stack(
                        Text('Input second number:', bold=True),
                        Spacer(size='2%'),
                        Input(value=num_2),
                        direction='horizontal'
                    ),
                    span=5
                ),
                Grid.Column(
                    Stack(
                        information_button(show_vars_and_inputs_definitions),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Grid.Column(
                    Paragraph(
                        Text('First number:', bold=True),
                        Text(num_1)
                    ),
                    span=6
                ),
                Grid.Column(
                    Paragraph(
                        Text('Second number:', bold=True),
                        Text(num_2)
                    ),
                    span=5,
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Text('While DerivedVariables are a way of making a calculation with the front-end Variables \
                          of your app, py_components are a way of making a dynamic layout with the front-end \
                          Variables of your app.'),
                    span=11
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('In this example, the numbers and their sum will be visualized with a Bokeh plot. \
                              The colors of the bars will be determined by the signs of the values. \
                              In order to visualize these Variables and DerivedVariables, you must have access \
                              to their values. The py_component decorator can give you access to these values.'),
                        Text('The decorated function can take a mixture of regular Python variables and \
                              Variable-based arguments in any combination. The decorator will extract the values \
                              from the Variables so you can use them within Python logic.'),
                        Stack(bar_plot(num_1, num_2, summation), height='200px')
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_py_component_definition),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            padding='10px'
        ),
        code_modal(VARIABLES_AND_INPUT_CODE, show_vars_and_inputs_definitions),
        code_modal(PY_COMPONENTS_CODE, show_py_component_definition),
    )
