import json
from typing import List

from dara.core import Variable, get_icon, py_component
from dara.core.definitions import ComponentInstance
from dara.components import (
    Grid, Heading, Select, Spacer, Stack, 
    Text, Slider, Input, Switch, Tooltip, Icon
)


class RawCSSPage:
    def __init__(self) -> None:
        self.script_str_1 = Variable("div > span {\n\tcolor: red\n}\nspan > svg {\n\tcolor: tomato\n}")
        self.script_str_2 = Variable(
            "span > h2 {\n\tcolor: indigo;\n\n\t&:hover {\n\t\tcolor: white;\n\t}\n}\nspan:hover {\n\tbackground-color: plum;\n}"
        )

        self.script_dict_1 = Variable('{\n\t"color": "lightcoral", \n\t"font-size": "1.2em"\n}')
        self.script_dict_2 = Variable('{\n\t"color": "indigo"\n}')

    def __call__(self) -> ComponentInstance:
        return Stack(
            Heading("Customizing Components"),
            self.css_properties_content()
        )

    def display_attribute(self, attribute: str, description: str):
        return Stack(
            Stack(
                Text(attribute, bold=True),
                Tooltip(
                    Icon(icon=get_icon('circle-question', style='regular'), color='lightslategrey'),
                    content=description,
                    placement='top',
                ),
                direction='horizontal',
                hug=True
            ),
            width='120px'
        )

    def box_model_slider(self, var: Variable):
        return Slider(
            domain=[0, 100],
            value=var,
            disable_input_alternative=True,
            ticks=[*range(20, 100, 20)]
        )

    @py_component
    def dynamic_component(
        self,
        align: str,
        background: str,
        bold: bool,
        color: str,
        font_size: List[int],
        italic: str,
        border_radius: List[int],
        border_width: str,
        border_style: str,
        border_color: str,
        height_value: List[int],
        height_type: str,
        width_value: List[int],
        width_type: str,
        padding: int,
        margin: int
    ):
        def _convert_float(value: str, default: float):
            try:
                value = float(value)
            except ValueError:
                value = default
            return value

        height = _convert_float(height_value, 50.0)
        width = _convert_float(width_value, 50.0)
        border_width = _convert_float(border_width, 1.0)

        return Stack(
            Text('Text in a box', bold=bold, color=color, italic=italic),
            align=align,
            background=background,
            font_size=f'{font_size[0]}px',
            border_radius=f'{border_radius[0]}px',
            border=f'{border_width}px {border_style} {border_color}',
            height=f'{height}{height_type}',
            width=f'{width}{width_type}',
            padding=f'{padding}px',
            margin=f'{margin}px',
        )

    def css_properties_content(self):
        bold_var = Variable(False)
        align_var = Variable('start')
        background_var = Variable('white')
        color_var = Variable('black')
        text_size_var = Variable([12])
        italic_var = Variable(False)
        border_radius_var = Variable([5])
        border_color_var = Variable('black')
        border_style_var = Variable('dashed')
        border_width_var = Variable(1)
        height_value_var = Variable('50')
        height_type_var = Variable('%')
        width_value_var = Variable('50')
        width_type_var = Variable('%')
        padding_var = Variable(20)
        margin_var = Variable(20)

        return Stack(
            Text(
                'This method is the simplest and should account for most of the cases in \
                which you need to change the styling of components. These are properties \
                which all components inherit. You can pass them to the component as \
                you would with any other property. Interact with the for below to see \
                how each property changes the component on the right.'
            ),
            Spacer(),
            Stack(
                Stack(
                    Stack(
                        self.display_attribute(
                            'align',
                            'an alignment string, any flexbox alignment or start/center/end are accepted'
                        ),
                        Select(items=['start', 'center', 'end'], value=align_var),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('bold*', 'whether to bold the font'),
                        Switch(value=bold_var),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('italic*', 'whether to italicize the font'),
                        Switch(value=italic_var),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('color*', 'the text color of the component'),
                        Select(value=color_var, items=['black', 'steelblue', 'seagreen']),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('font_size*', 'the size of the font'),
                        Slider(
                            domain=[1, 30],
                            step=1,
                            value=text_size_var,
                            disable_input_alternative=True,
                            ticks=[*range(5, 30, 5)],
                            padding='5px'
                        ),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute(
                            'border_radius',
                            'set the radius of a components corners (i.e. round them)'
                        ),
                        Slider(
                            domain=[1, 30],
                            step=1,
                            value=border_radius_var,
                            disable_input_alternative=True,
                            ticks=[*range(5, 30, 5)],
                            padding='5px'
                        ),
                        direction='horizontal'
                    ),
                    Text('* applied within the Text component'),
                    width='30%'
                ),
                Spacer(),
                Stack(
                    Stack(
                        self.display_attribute('background', 'sets a background color on the component'),
                        Select(items=['aliceblue', 'honeydew', 'white'], value=background_var),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('border', 'border style of the component'),
                        Stack(
                            Stack(
                                Text('width:'),
                                Input(value=border_width_var, width='100%'),
                            ),
                            Stack(
                                Text('style:'),
                                Select(
                                    value=border_style_var,
                                    items=['dashed', 'dotted', 'solid', 'double'],
                                )
                            ),
                            Stack(
                                Text('color:'),
                                Select(
                                    value=border_color_var,
                                    items=['black', 'steelblue', 'seagreen'],
                                )
                            ),
                            direction='horizontal',
                        ),
                        direction='horizontal',
                    ),
                    Stack(
                        self.display_attribute(
                            'height',
                            'the height of the component; can be an number which will be converted to pixels, \
                                or a percentage'
                        ),
                        Grid(
                            Grid.Row(
                                Grid.Column(
                                    Input(value=height_value_var, width='100%'),
                                    span=5
                                ),
                                Grid.Column(
                                    Select(value=height_type_var, items=['px', '%']),
                                    span=7
                                ),
                                column_gap=2
                            )
                        ),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute(
                            'width',
                            'the width of the component; can be an number which will be converted to pixels, \
                                or a percentage'
                        ),
                        Grid(
                            Grid.Row(
                                Grid.Column(
                                    Input(value=width_value_var, width='100%'),
                                    span=5
                                ),
                                Grid.Column(
                                    Select(value=width_type_var, items=['px', '%']),
                                    span=7,
                                ),
                                column_gap=2
                            ),
                        ),
                        direction='horizontal'
                    ),
                    Stack(
                        self.display_attribute('padding', 'the amount of padding to apply to the component'),
                        self.box_model_slider(padding_var),
                        direction='horizontal',
                        justify='start'
                    ),
                    Stack(
                        self.display_attribute('margin', 'the amount of margin to apply to the component'),
                        self.box_model_slider(margin_var),
                        direction='horizontal',
                        justify='start'
                    ),
                ),
                Spacer(line=True),
                Stack(
                    self.dynamic_component(
                            align_var, background_var, bold_var, color_var, text_size_var, italic_var,
                            border_radius_var, border_width_var, border_style_var, border_color_var,
                            height_value_var, height_type_var, width_value_var, width_type_var,
                            padding_var, margin_var
                    ),
                    align='center',
                    justify='center',
                ),   
                direction='horizontal',      
            ),
            scroll=True
        )
