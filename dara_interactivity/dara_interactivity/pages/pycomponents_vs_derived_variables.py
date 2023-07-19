from dara.core import Variable, DerivedVariable, py_component
from dara.core.definitions import ComponentInstance
from dara.components import Grid, Stack, Text, Input, Spacer, Paragraph, Card, Heading

from dara_interactivity.custom_components import information_button, code_modal
from dara_interactivity.definitions import (
    INPUT_INSTANTIATION_CODE, HORIZONTAL_CODE, VERTICAL_CODE, BACKWARDS_CODE
)


@py_component
def my_py_component(input_str: str) -> ComponentInstance:
    """
    Returns a component that displays the input string vertically

    :param input_str: input string
    :return ComponentInstance
    """
    vertical_text = Stack()
    for letter in input_str:
        vertical_text.append(Text(letter, font_size='9px'))
    return vertical_text


def comparison_page() -> ComponentInstance:
    """
    Constructs the layout of the page.

    The page displays a some instructional text, along with modals displaying code snippets.

    :return: ComponentInstance
    """
    user_input = Variable('hello')
    backwards_input = DerivedVariable(lambda text: ''.join(reversed(text)), variables=[user_input])

    # Define Variables that show/hide the code modals
    show_input_instantiation = Variable(False)
    show_horizontal = Variable(False)
    show_backwards = Variable(False)
    show_vertical = Variable(False)

    return Stack(
        Heading('DerivedVariable vs py_component'),
        Text('Click on the ? buttons to show the underlying code in which the information is referring to.', italic=True),
        Grid(
            Grid.Row(
                Grid.Column(
                    Stack(
                        Paragraph(
                            Text('It may be that you are unsure of which to use, and the answer may often be a \
                                  combination of both! DerivedVariables and py_components are similar in the way \
                                  that they both will calculate something based on other Variable-type values. \
                                  The key difference is that a '),
                            Text('py_component', bold=True),
                            Text(' returns a '),
                            Text('component', bold=True),
                            Text(' whereas a '),
                            Text('DerivedVariable', bold=True),
                            Text(' is used to recalculate a '),
                            Text('value.', bold=True),
                        ),
                        Text('The example below is aimed at illustrating how these might work together. \
                              The user will input some text, stored in a Variable. You will be tasked \
                              with displaying input horizontally, vertically and backwards, displaying how and when \
                              to use DerivedVariable and py_component.')
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_input_instantiation),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Stack(
                    Text('Please input some text:'),
                    Spacer(size='2%'),
                    Input(value=user_input),
                    direction='horizontal'
                ),   
            ),
            Grid.Row(
                Spacer(line=True)
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Heading('Horizontal', level=3),
                        Text('This is the simplest case. You just need to show the Variable value as is.'),
                        Text(user_input)
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_horizontal),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Spacer(line=True)
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Heading('Backwards', level=3),
                        Text('To display the text backwards you need to transform the string. \
                              This involves changing the value of the string so in this case you \
                              would use a DerivedVariable.'),
                        Text(backwards_input)
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_backwards),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            Grid.Row(
                Spacer(line=True)
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Heading('Vertical', level=3),
                        Text('In this case you will choose to loop through each letter of the input \
                              text and add each letter as a separate Text component so that they can \
                              be placed vertically in a Stack. Because you want a varying layout, you \
                              must use the py_component-decorator.'),
                        my_py_component(user_input),
                    ),
                    span=11
                ),
                Grid.Column(
                    Stack(
                        information_button(show_vertical),
                        justify='center',
                        align='center'
                    ),
                    span=1
                )
            ),
            padding='10px'
        ),
        code_modal(INPUT_INSTANTIATION_CODE, show_input_instantiation),
        code_modal(HORIZONTAL_CODE, show_horizontal),
        code_modal(BACKWARDS_CODE, show_backwards),
        code_modal(VERTICAL_CODE, show_vertical),
    )
