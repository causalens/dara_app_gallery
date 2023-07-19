import json
from typing import List

from dara.core import Variable, get_icon, py_component
from dara.core.definitions import ComponentInstance
from dara.components import (
    CodeEditor, Grid, Heading, Select, Spacer, Stack, Tab, TabbedCard,
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
            Heading("Customizing Components", level=3),
            TabbedCard(
                Tab(
                    self.css_properties_content(),
                    title='Quick Properties',
                ),
                Tab(
                    self.css_dict_content(),
                    title='Dictionary of CSSProperties',
                ),
                Tab(
                    self.css_str_content(),
                    title='String of CSS',
                ),
            ),
        )

    @py_component
    def select_from_str(self, script: str):
        return Stack(
            Select(value=Variable(['first']), items=['first', 'second', 'third'], multiselect=True, raw_css=script),
        )

    @py_component
    def select_from_dict(self, script: dict):
        script_dict = json.loads(script)
        return Stack(
            Select(
                value=Variable(['first']), items=['first', 'second', 'third'], multiselect=True, raw_css=script_dict
            ),
        )

    @py_component
    def tab_card_from_str(self, card_css: str):
        return TabbedCard(
            Tab(Text('Some text'), title='Card 1'),
            Tab(Text('Some other text'), title='Card 2'),
            raw_css=card_css,
        )

    @py_component
    def tab_card_from_dict(self, card_css: dict):
        script_dict = json.loads(card_css)
        return TabbedCard(
            Tab(Text('Some text'), title='Card 1'),
            Tab(Text('Some other text'), title='Card 2'),
            raw_css=script_dict,
        )

    def display_attribute(self, attribute: str, description: str):
        return Stack(
            Text(attribute, bold=True),
            Tooltip(
                Icon(icon=get_icon('circle-question', style='regular'), color='lightslategrey'),
                content=description,
            ),
            direction='horizontal',
        )

    def box_model_slider(self, var: Variable, label: str):
        return Slider(
            domain=[0, 100],
            value=var,
            disable_input_alternative=True,
            rail_labels=[label],
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
        top_padding: List[int],
        right_padding: List[int],
        bottom_padding: List[int],
        left_padding: List[int],
        top_margin: List[int],
        right_margin: List[int],
        bottom_margin: List[int],
        left_margin: List[int]
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
            padding=f'{top_padding[0]}px {right_padding[0]}px {bottom_padding[0]}px {left_padding[0]}px',
            margin=f'{top_margin[0]}px {right_margin[0]}px {bottom_margin[0]}px {left_margin[0]}px',
        )

    def css_str_content(self):
        return Grid(
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text(
                            'Components in Dara have a property called raw_css which allows you to pass \
                                CSS properties as a dictionary or string. In this tab, you can explore \
                                how to set raw_css as a string with the code editors. This allows you \
                                the most amount of freedom when styling your components because you can access \
                                individual CSS selectors. CSS selectors are patterns used to select the element(s) \
                                you want to style.'),
                        Spacer(line=True, size='2%')
                    )
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('Select Component:', raw_css={'font-weight': 'bold', 'font-size': '1.3em'}),
                        self.select_from_str(self.script_str_1),
                    )
                ),
                Grid.Column(
                    CodeEditor(
                        script=self.script_str_1, width='100%', background='#fafaff'
                    ),
                    span=6,
                ),
                height='40%',
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text(
                            'Tabbed Card Component:', raw_css={'font-weight': 'bold', 'font-size': '1.3em'}
                        ),
                        self.tab_card_from_str(self.script_str_2),
                    )
                ),
                Grid.Column(
                    CodeEditor(
                        script=self.script_str_2, width='100%', background='#fafaff'
                    ),
                    span=6,
                ),
                height='40%',
            ),
        )

    def css_dict_content(self):
        return Grid(
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text(
                            'Components in Dara have a property called raw_css which allows you to pass \
                                CSS properties as a dictionary or string. In this tab, you can explore \
                                how to set raw_css as a dict with the code editors.  Notice how you may \
                                not be able to change all the properties of the component. This is \
                                because the raw_css only applies to the parent entity and more complex \
                                components may have a child or multiple child entities. The next tab \
                                can show you how to get around this if needed.'),
                    )
                ),
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text('Select Component:', raw_css={'font-weight': 'bold', 'font-size': '1.3em'}),
                        self.select_from_dict(self.script_dict_1),
                    )
                ),
                Grid.Column(
                    CodeEditor(script=self.script_dict_1, width='100%', background='#fafaff'),
                    span=6,
                ),
                height='40%',
            ),
            Grid.Row(
                Grid.Column(
                    Stack(
                        Text(
                            'Tabbed Card Component:', raw_css={'font-weight': 'bold', 'font-size': '1.3em'}
                        ),
                        self.tab_card_from_dict(self.script_dict_2),
                    )
                ),
                Grid.Column(
                    CodeEditor(
                        script=self.script_dict_2, width='100%', background='#fafaff'
                    ),
                    span=6,
                ),
                height='40%',
            ),
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
        top_padding_var, right_padding_var = Variable([20]), Variable([20])
        bottom_padding_var, left_padding_var = Variable([20]), Variable([20])
        top_margin_var, right_margin_var = Variable([20]), Variable([20])
        bottom_margin_var, left_margin_var = Variable([20]), Variable([20])

        return Stack(
            Grid(
                Grid.Row(
                    Grid.Column(
                        Stack(
                            Text(
                                'This method is the simplest and should account for most of the cases in \
                                        which you need to change the styling of components. These are properties \
                                        which all components inherit. You can pass them to the component as \
                                        you would with any other property. Interact with the for below to see \
                                        how each property changes the component on the right.'
                            )
                        ),
                    ),
                ),
                Grid.Row(
                    Grid.Column(
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
                                self.display_attribute('background', 'sets a background color on the component'),
                                Select(items=['aliceblue', 'honeydew', 'white'], value=background_var),
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
                            Text('* applied within the Text component')
                        ),
                    ),
                    Grid.Column(
                        Stack(
                            self.display_attribute('border', 'border style of the component'),
                            Grid(
                                Grid.Row(
                                    Grid.Column(
                                        Text('width (px):'),
                                        span=4
                                    ),
                                    Grid.Column(
                                        Text('style:'),
                                        span=4
                                    ),
                                    Grid.Column(
                                        Text('color:'),
                                        span=4
                                    ),
                                    column_gap=1
                                ),
                                Grid.Row(
                                    Grid.Column(
                                        Input(value=border_width_var, width='100%'),
                                        span=4
                                    ),
                                    Grid.Column(
                                        Select(
                                            value=border_style_var,
                                            items=['dashed', 'dotted', 'solid', 'double'],
                                            width='100%'
                                        ),
                                        span=4
                                    ),
                                    Grid.Column(
                                        Select(
                                            value=border_color_var,
                                            items=['black', 'steelblue', 'seagreen'],
                                            width='100%'
                                        ),
                                        span=4
                                    ),
                                    column_gap=1
                                ),
                                raw_css={'gap': '0rem'}
                            ),
                            Stack(
                                Stack(
                                    self.display_attribute(
                                        'height',
                                        'the height of the component; can be an number which will be converted to pixels, \
                                            or a percentage'
                                    ),
                                    width='20%'
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
                                Stack(
                                    self.display_attribute(
                                        'width',
                                        'the width of the component; can be an number which will be converted to pixels, \
                                            or a percentage'
                                    ),
                                    width='20%'
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
                                Stack(
                                    self.display_attribute('padding', 'the amount of padding to apply to the component'),
                                    width='20%'
                                ),
                                Stack(
                                    Stack(
                                        self.box_model_slider(top_padding_var, 'top'),
                                        self.box_model_slider(right_padding_var, 'right'),
                                    ),
                                    Stack(
                                        self.box_model_slider(bottom_padding_var, 'bottom'),
                                        self.box_model_slider(left_padding_var, 'left'),
                                    ),
                                    direction='horizontal'
                                ),
                                direction='horizontal',
                                justify='start'
                            ),
                            Stack(
                                Stack(
                                    self.display_attribute('margin', 'the amount of margin to apply to the component'),
                                    width='20%'
                                ),
                                Stack(
                                    Stack(
                                        self.box_model_slider(top_margin_var, 'top'),
                                        self.box_model_slider(right_margin_var, 'right'),
                                    ),
                                    Stack(
                                        self.box_model_slider(bottom_margin_var, 'bottom'),
                                        self.box_model_slider(left_margin_var, 'left'),
                                    ),
                                    direction='horizontal'
                                ),
                                direction='horizontal',
                                justify='start'
                            ),
                        ),
                        span=5
                    ),
                    Grid.Column(
                        self.dynamic_component(
                            align_var, background_var, bold_var, color_var, text_size_var, italic_var,
                            border_radius_var, border_width_var, border_style_var, border_color_var,
                            height_value_var, height_type_var, width_value_var, width_type_var,
                            top_padding_var, right_padding_var, bottom_padding_var, left_padding_var,
                            top_margin_var, right_margin_var, bottom_margin_var, left_margin_var
                        ),
                        span=3
                    ),
                    column_gap=3,
                    height='calc(100% - 200px)'
                ),
                row_gap=1,
            ),
            scroll=True
        )
