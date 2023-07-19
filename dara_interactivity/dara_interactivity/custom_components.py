from dara.core import UpdateVariable, Variable
from dara.core.definitions import ComponentInstance
from dara.components import Button, Text, Modal, Code, Stack


def information_button(var_to_update: Variable) -> ComponentInstance:
    """
    Defines a Button that displays as a "?" and updates a variable with True when clicked

    :param var_to_update: Variable to update with the button's onclick action
    :return ComponentInstance
    """
    return Button(
        Text('?', bold=True),
        onclick=UpdateVariable(lambda ctx: True, variable=var_to_update),
        raw_css={'border-radius': '100px'},
        styling='secondary',
        width='50px'
    )


def code_modal(code: str, show_var: Variable) -> ComponentInstance:
    """
    Defines a pop-up Modal that displays code when variable in show_var is True

    :param code: code snippet for the Modal to display
    :param show_var: Variable dictating when the Modal shown
    :return ComponentInstance
    """
    return Modal(
        Stack(
            Code(code=code, language='python'),
            padding='1rem',
            scroll=True,
            width='900px',
            height='500px'
        ),
        show=show_var
    )
