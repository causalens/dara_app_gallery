from dara.components import Card, Modal, Stack, Table, Text
from dara.core import DataVariable, DerivedDataVariable, UpdateVariable, Variable
from dara.components import CausalGraphViewer
from dara.components.graphs import EditorMode

from dara_graph_viewer.definitions import GRAPH, FRIENDSHIPS_DATA
from dara_graph_viewer.utils import filter_interactions_data


def IntroductionPage():
    selected_edge = Variable()
    filtered_individuals_data = DerivedDataVariable(filter_interactions_data, variables=[selected_edge])
    show_individuals_modal = Variable(False)

    return Stack(
        CausalGraphViewer(
            causal_graph=GRAPH,
            editor_mode=EditorMode.PAG,
            on_click_edge=[
                UpdateVariable(lambda ctx: (ctx.inputs.new['source'], ctx.inputs.new['destination']) if ctx.inputs.new is not None else None, variable=selected_edge),
                UpdateVariable(lambda ctx: True, variable=show_individuals_modal),
            ]
        ),
        Stack(
            Card(
                Text('Social Network Analysis (SNA) is the process of investigating social structures through the use of graph thoery.'),
                Text('In this app, you will explore various factes of SNA with the network represented by the graph on the left and the dataset below.'),
                Text('Select an edge on the graph to view a log of the individual\'s interactions.'),
                title='Social Network Analysis',
                accent=True,
                hug=True,
            ),
            Table(data=DataVariable(FRIENDSHIPS_DATA)),
            width='calc(50% - 0.75rem)',
        ),
        Modal(Table(data=filtered_individuals_data), show=show_individuals_modal, width='80vw', height='50vh'),
        direction='horizontal',
    )
