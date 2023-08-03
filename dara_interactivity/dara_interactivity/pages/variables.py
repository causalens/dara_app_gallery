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
from dara.core import Variable
from dara.core.definitions import ComponentInstance
from dara.components import Heading, Grid, Stack, Text, Input, Spacer, Paragraph

from dara_interactivity.custom_components import code_modal, information_button
from dara_interactivity.definitions import (
    VARIABLES_INSTANTIATION_CODE, VARIABLES_INPUT_CODE, VARIABLES_PARAGRAPH_CODE
)


def variables_page() -> ComponentInstance:
    """
    Constructs the layout of the page.

    The page displays a some instructional text, along with modals displaying code snippets.

    :return: ComponentInstance
    """
    num_1 = Variable(1)
    num_2 = Variable(1)

    # Define Variables that show/hide the code modals
    show_variable_instantiation = Variable(False)
    show_variable_inputs = Variable(False)
    show_variable_paragraph = Variable(False)

    return Stack(
        Heading('Variables'),
        Text('Click on the ? buttons to show the underlying code in which the information is referring to.', italic=True),
        Grid(
            Grid.Row(
                Grid.Column(
                    Text('A Variable is the core of the framework\'s reactivity system. \
                          It represents a dynamic value that can be read and written to by components. \
                          The state is managed entirely in the user\'s browser which means there is no \
                          need to call back to the Python server on each update.'),
                    span=11
                )
            ),
            Grid.Row(
                Grid(
                    Grid.Row(
                        Grid.Column(
                            Text('In this example you\'ll have two Variables, both representing a number \
                                  that the user can interact with. Variables can take a default value. In this \
                                  example the default value will be set to one.'),
                            span=11
                        ),
                        Grid.Column(
                            Stack(
                                information_button(show_variable_instantiation),
                                align='center',
                            ),
                            span=1,
                            justify='center',
                        )
                    ),
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Text('A Variable cannot be written to with traditional Python code. Variables can   \
                          however be written to by components like the Input fields below.'),
                    span=11
                )
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('Input first number:', bold=True),
                        Spacer(size='2%'),
                        Input(value=num_1),
                        direction='horizontal',
                    ),
                    span=5
                ),
                Grid.Column(
                    Stack(
                        Text('Input second number:', bold=True),
                        Spacer(size='2%'),
                        Input(value=num_2),
                        direction='horizontal'
                    ),
                    span=6
                ),
                Grid.Column(
                    Stack(
                        information_button(show_variable_inputs),
                        justify='center',
                        align='center',
                    ),
                    span=1,
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Text('A Variable can also not be read from with traditional Python code. Variables can  \
                          however be read by components that accept them as arguments like the Text fields below.'),
                    span=11
                )
            ),
            Grid.Row(
                Grid.Column(
                    Paragraph(
                        Text('First number:', bold=True),
                        Text(num_1)
                    ),
                    span=5
                ),
                Grid.Column(
                    Paragraph(
                        Text('Second number:', bold=True),
                        Text(num_2)
                    ),
                    span=6,
                ),
                Grid.Column(
                    Stack(
                        information_button(show_variable_paragraph),
                        align='center',
                    ),
                    span=1,
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Text('You\'ll notice that whenever an Input field changes, it updates the values of its \
                          associated Variable and its value is displayed in the Text component. \
                          The whole process is synchronized as the value is stored entirely in the frontend \
                          so there are no calls to the Python server.'),
                    span=11
                )
            ),
            padding='10px'
        ),
        code_modal(VARIABLES_INSTANTIATION_CODE, show_variable_instantiation),
        code_modal(VARIABLES_INPUT_CODE, show_variable_inputs),
        code_modal(VARIABLES_PARAGRAPH_CODE, show_variable_paragraph),
    )
