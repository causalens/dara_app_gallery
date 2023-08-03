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
from typing import Union

from dara.core import Variable, DerivedVariable
from dara.core.definitions import ComponentInstance
from dara.components import Heading, Grid, Stack, Text, Input, Spacer, Paragraph, Card, Card, Button

from dara_interactivity.custom_components import code_modal, information_button
from dara_interactivity.definitions import (
    DERIVED_VARIABLE_CODE, DERIVED_VARIABLE_WITH_DEPS_CODE, DERIVED_VARIABLE_WITH_TRIGGER_CODE
)


def sum(a, b) -> Union[float, str]:
    """
    Calculates the sum of two inputs, first converting them to floats.

    :param a: first string input
    :param b: second string input
    :return float or a warning string if the inputs cannot be converted to floats
    """
    try:
        return float(a) + float(b)
    except ValueError:
        return ' not calculable.'


def derived_variables_page() -> ComponentInstance:
    """
    Constructs the layout of the page.

    The page displays a some instructional text, along with modals displaying code snippets.

    :return: ComponentInstance
    """
    num_1 = Variable(1)
    num_2 = Variable(1)

    summation = DerivedVariable(func=sum, variables=[num_1, num_2])
    summation_with_deps = DerivedVariable(func=sum, variables=[num_1, num_2], deps=[num_2])
    summation_with_empty_deps = DerivedVariable(func=sum, variables=[num_1, num_2], deps=[])

    # Define Variables that show/hide the code modals
    show_derived_variable = Variable(False)
    show_derived_variable_with_deps = Variable(False)
    show_derived_variable_with_trigger = Variable(False)

    return Stack(
        Heading('Derived Variables'),
        Text('Click on the ? buttons to show the underlying code in which the information is referring to.', italic=True),
        Grid(
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('Input first number:', bold=True),
                        Input(value=num_1),
                        direction='horizontal',
                    ),
                    span=6
                ),
                Grid.Column(
                    Stack(
                        Text('Input second number:', bold=True),
                        Input(value=num_2),
                        direction='horizontal'
                    ),
                    span=6
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('First number:', bold=True),
                        Text(num_1),
                        direction='horizontal'
                    ),
                    span=6
                ),
                Grid.Column(
                    Stack(
                        Text('Second number:', bold=True),
                        Text(num_2), 
                        direction='horizontal'
                    ),
                    span=6,
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Text('As values in Variables cannot be extracted with traditional Python code, \
                          you can use DerivedVariables to access these values and make calculations. \
                          In this example, the two Variables will be summed together.'),
                    span=11
                )
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('When defining a DerivedVariable, you have to specify a function and a list of Variables \
                              or other DerivedVariables that act as arguments to that function. Every time one of the \
                              specified variables changes, the function is re-run with the current values of the variables.'),
                        Stack(
                            Card(
                                Paragraph(
                                    Text('The sum of '),
                                    Text(num_1),
                                    Text('and '),
                                    Text(num_2),
                                    Text('is '),
                                    Text(summation)
                                ),
                                width='25%',
                            ),
                            justify='center',
                            direction='horizontal',
                        ),
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_derived_variable),
                        justify='center',
                        align='center'
                    ),
                    span=1,
                )
            ),
            Grid.Row(
                Spacer(line=True)
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('You\'ll notice that whenever an Input field changes, it updates the values of its \
                              associated Variable and thus the DerivedVariable is updated as well. You can have more \
                              control over when your DerivedVariable is updated with the dep argument as it specifies \
                              what triggers the recalculation.'),
                        Text('The following example will only change when the second number is changed.'),
                        Stack(
                            Card(
                                Paragraph(
                                    Text('The sum of '),
                                    Text(num_1),
                                    Text('and '),
                                    Text(num_2),
                                    Text('is '),
                                    Text(summation_with_deps)
                                ),
                                width='25%',
                            ),
                            justify='center',
                            direction='horizontal',
                        )
                    )
                ),
                Grid.Column(
                    Stack(
                        information_button(show_derived_variable_with_deps),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('In this example, it makes the most sense to wait until both inputs are filled out by \
                              the user to make the calculation. By setting deps to an empty list, the DerivedVariable \
                              will only recalculate when explicitly told to do so. This message can be sent by the \
                              DerivedVariable\'s trigger method. You can associate the trigger method to user interactions \
                              like button clicks.'),
                        Text('The following example will only change when the button is clicked.'),
                        Stack(
                            Card(
                                Paragraph(
                                    Text('The sum of '),
                                    Text(num_1),
                                    Text('and '),
                                    Text(num_2),
                                    Text('is '),
                                    Text(summation_with_empty_deps)
                                ),
                                width='25%'
                            ),
                            Spacer(),
                            Button(
                                'Recalculate Sum',
                                onclick=summation_with_empty_deps.trigger(),
                            ),
                            direction='horizontal',
                            justify='center',
                            align='center'
                        )
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_derived_variable_with_trigger),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            padding='10px'
        ),
        code_modal(DERIVED_VARIABLE_CODE, show_derived_variable),
        code_modal(DERIVED_VARIABLE_WITH_DEPS_CODE, show_derived_variable_with_deps),
        code_modal(DERIVED_VARIABLE_WITH_TRIGGER_CODE, show_derived_variable_with_trigger),
    )
