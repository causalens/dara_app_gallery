from dara.core import Variable, py_component
from dara.core.definitions import ComponentInstance
from dara.components import CodeEditor, Grid, Heading, Spacer, Stack, Text


class CSSUnitsPage:
    def __init__(self) -> None:
        pass

    def __call__(self) -> ComponentInstance:

        grid_css = """
        div div * {å
            font-size: 1.1rem;
        }
        """

        script = Variable(
            'div\n{\n\tbackground: steelblue;\t\t\t\n\twidth: 400px !important;\t\t\t\n}'
        )

        @py_component
        def size_example(script: str):
            return Stack(
                Stack(
                    Stack(),
                    raw_css=script,
                ),
                raw_css={'border-style': 'solid'},
                width='600px',
                height='100px',
            )

        return Stack(
            Heading('CSS Units Explained', level=3),
            Spacer(),
            Grid(
                Grid.Row(
                    Grid.Column(
                        Text('Unit', bold=True), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text('Description', bold=True),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('px'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text(
                            'The px unit is the magic unit of CSS. It is not related to the current font and usually \
                                not related to physical centimeters or inches either. The px unit is defined to be \
                                small but visible, and such that a horizontal 1px wide line can be displayed with \
                                sharp edges (no anti-aliasing). What is sharp, small and visible depends on the \
                                device and the way it is used: do you hold it close to your eyes, like a mobile \
                                phone, at arms length, like a computer monitor, or somewhere in between, like \
                                an e-book reader? The px is thus not defined as a constant length, but as \
                                something that depends on the type of device and its typical use.'
                        ),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        justify='center',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('em'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text(
                            'These are related to the font size, and if the user has a big font (e.g., on a big screen) \
                                or a small font (e.g., on a handheld device), the sizes will be in proportion. \
                                Declarations such as text-indent: 1.5em and margin: 1em are extremely common in CSS.'
                        ),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        justify='center',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('rem'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text(
                            'Is the "root em", it relates to the font size of the root element, whereas em varies \
                                depending on the parent element'
                        ),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('vw'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text('Relative to 1% of the width of the viewport'),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('vh'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text('Relative to 1% of the height of the viewport'),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        align_items='center',
                    ),
                ),
                Grid.Row(
                    Grid.Column(
                        Text('%'), span=3, raw_css={'border-style': 'solid'}, justify='center', align_items='center'
                    ),
                    Grid.Column(
                        Text('Size relative to parent element'),
                        raw_css={'border-style': 'solid'},
                        padding='0px 20px 0px 20px',
                        align_items='center',
                    ),
                ),
                raw_css=grid_css,
                row_gap=0
            ),
            Spacer(),
            Text(
                'Example: The outer box has 600px width. \
                    The code editor is updating the CSS of the inner entity in blue. \
                    Play around with different width values and units to get a feel for how it works.',
            ),
            Stack(
                size_example(script),
                CodeEditor(script=script, background='#fafaff'),
                direction='horizontal',
            ),
        )
