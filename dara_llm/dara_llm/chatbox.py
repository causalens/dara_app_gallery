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
import os
from dotenv import load_dotenv

from dara.components import (
    Button,
    Card,
    If,
    Overlay,
    Select,
    Stack,
    Text,
    Textarea,
)
from dara.core import (
    DerivedVariable,
    ResetVariables,
    TriggerVariable,
    UpdateVariable,
    Variable,
)
from dara.core.visual.themes import Light

from dara_llm.tasks import query_chat_gpt


def ChatBox():
    """
    A component that allows the user to query ChatGPT with questions about the model.
    Predefined questions are defined for the user's convenience but there is also
    an input for a custom question.
    
    To use this component the OPENAI_API_KEY environment variable must be set in .env.
    """
    try:
        load_dotenv()
        assert os.getenv('OPENAI_API_KEY') is not None

        open_chat = Variable(False)

        predefined_question = Variable('')
        predefined_answer = DerivedVariable(
            query_chat_gpt,
            variables=[predefined_question],
            run_as_task=True,
            deps=[],
        )

        custom_question = Variable('')
        custom_answer = DerivedVariable(
            query_chat_gpt,
            variables=[custom_question],
            run_as_task=True,
            deps=[],
        )

        return Overlay(
            If(
                open_chat,
                Stack(),
                Button(
                    'Ask ChatGPT',
                    onclick=UpdateVariable(lambda _: True, variable=open_chat),
                    width='10vw',
                ),
            ),
            If(
                open_chat,
                Card(
                    Stack(
                        Text('Try some of the example prompts below:'),
                        Select(
                            items=[
                                "Explain the model's coefficients and whether they are significant.",
                                "Explain the model's overall performance.",
                                "Explain whether the distribution of my model's residuals is normal.",
                                "Explain the model's R-Squared value.",
                                "Explain the model's F-Statistic value.",
                                "Explain the model's Log Likelihood value.",
                            ],
                            value=predefined_question,
                            min_height='38px',
                        ),
                        Stack(
                            Button(
                                'Query',
                                width='7vw',
                                onclick=TriggerVariable(
                                    variable=predefined_answer
                                ),
                                styling='secondary',
                            ),
                            align='end',
                            hug=True,
                        ),
                        Text(predefined_answer),
                        Text(
                            'Or alternatively ask me anything given the context of this page:'
                        ),
                        Textarea(value=custom_question),
                        Stack(
                            Button(
                                'Query',
                                width='7vw',
                                onclick=TriggerVariable(variable=custom_answer),
                                styling='secondary',
                            ),
                            align='end',
                            hug=True,
                        ),
                        Text(custom_answer),
                        Stack(
                            Button(
                                'Close',
                                onclick=[
                                    UpdateVariable(
                                        lambda _: False, variable=open_chat
                                    ),
                                    ResetVariables(
                                        variables=[
                                            custom_question,
                                            predefined_question,
                                            custom_answer,
                                            predefined_answer,
                                        ]
                                    )
                                ],
                                width='10vw',
                                styling='error',
                            ),
                            align='center',
                            hug=True,
                        ),
                        scroll=True,
                    ),
                    width='40vw',
                    height='90vh',
                ),
            ),
            hug=True,
            position='top-right',
            padding='0rem',
        )
    except AssertionError:
        return Card(
            Text(
                'Please set the OPENAI_API_KEY environment variable in your .env file \
                with your OpenAI API key so that the app can query ChatGPT.',
                align='center',
            ),
            border=f'5px solid {Light.colors.error}',
        )
