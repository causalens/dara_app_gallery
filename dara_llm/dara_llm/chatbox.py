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
        custom_question = Variable('')
        answer_predefined = DerivedVariable(
            query_chat_gpt,
            variables=[predefined_question],
            run_as_task=True,
            deps=[],
        )
        answer_custom = DerivedVariable(
            query_chat_gpt,
            variables=[custom_question],
            run_as_task=True,
            deps=[],
        )
        return Overlay(
            If(
                open_chat,
                Stack(height='40px'),
                Button(
                    'Ask ChatGPT',
                    onclick=UpdateVariable(lambda _: True, variable=open_chat),
                    width='10vw',
                    height='40px',
                ),
            ),
            If(
                open_chat,
                Card(
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
                    ),
                    Stack(
                        Button(
                            'Query',
                            width='7vw',
                            onclick=TriggerVariable(
                                variable=answer_predefined
                            ),
                            styling='secondary',
                        ),
                        align='end',
                    ),
                    Stack(Text(answer_predefined)),
                    Text(
                        'Or alternatively ask me anything given the context of this page:'
                    ),
                    Textarea(value=custom_question),
                    Stack(
                        Button(
                            'Query',
                            width='7vw',
                            onclick=TriggerVariable(variable=answer_custom),
                            styling='secondary',
                        ),
                        align='end',
                    ),
                    Stack(Text(answer_custom)),
                    Stack(
                        Button(
                            'Close',
                            onclick=UpdateVariable(
                                lambda _: False, variable=open_chat
                            ),
                            width='10vw',
                            styling='error',
                        ),
                        align='center',
                        hug=True,
                    ),
                    width='40vw',
                ),
            ),
            align='end',
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
