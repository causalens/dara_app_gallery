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
from dara.core.definitions import ComponentInstance
from dara.components import Anchor, Heading, Spacer, Stack


class ResourcePage:
    def __init__(self) -> None:
        pass

    def __call__(self) -> ComponentInstance:
        return Stack(
            Heading('Useful Resources for Learning CSS', level=3),
            Spacer(),
            Heading('General CSS and CSS Propreties', level=4),
            Stack(
                Anchor(
                    '• W3 Schools',
                    href='https://www.w3schools.com/cssref/index.php',
                    new_tab=True
                ),
                Anchor(
                    '• MDN',
                    href='https://developer.mozilla.org/en-US/docs/Web/CSS',
                    new_tab=True
                ),
                Anchor(
                    '• CSS Tricks',
                    href='https://css-tricks.com/guides/',
                    new_tab=True
                ),
                padding='8px 8px 8px 20px',
            ),
            Heading('CSS Box Model (Margin and Padding)', level=4),
            Stack(
                Anchor(
                    '• MDN - The Box Model ',
                    href='https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model',
                    new_tab=True
                ),
                padding='8px 8px 8px 20px',
            ),
            Heading('CSS Units', level=4),
            Stack(
                Anchor(
                    '• W3 Schools - CSS Units Reference',
                    href='https://www.w3schools.com/cssref/css_units.php',
                    new_tab=True,
                ),
                Anchor(
                    '• Web Style Sheets CSS Tips & Tricks - Font Size Units',
                    href='https://www.w3.org/Style/Examples/007/units.en.html',
                    new_tab=True,
                ),
                padding='8px 8px 8px 20px',
            ),
            Heading('CSS Selectors', level=4),
            Stack(
                Anchor(
                    '• W3 Schools - CSS Selector Reference',
                    href='https://www.w3schools.com/cssref/css_selectors.php',
                    new_tab=True
                ),
                Anchor(
                    '• MDN - CSS Selector Reference',
                    href='https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors',
                    new_tab=True
                ),
                padding='8px 8px 8px 20px',
            ),
            Heading('Debugging CSS', level=4),
            Stack(
                Anchor(
                    '• Visbug Chrome Extension',
                    href='https://chrome.google.com/webstore/detail/visbug/cdockenadnadldjbbgcallicgledbeoc?hl=en',
                    new_tab=True,
                ),
                Anchor(
                    '• Chrome DevTools',
                    href='https://developer.chrome.com/docs/devtools/css/',
                    new_tab=True,
                ),
                Anchor(
                    '• Safari DevTools',
                    href='https://developer.apple.com/safari/tools/',
                    new_tab=True,
                ),
                padding='8px 8px 8px 20px',
            ),
            padding='20px',
        )
