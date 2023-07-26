from typing import Dict

import networkx as nx
from cai_causal_graph import CausalGraph
from dara.components import (Button, CausalGraphViewer, Stack, Tab, TabbedCard,
                             Text)
from dara.components.graphs import EditorMode
from dara.core import (DerivedVariable, ResetVariables, UpdateVariable,
                       Variable, py_component)
from dara.core.interactivity import ActionContext
from dara.core.visual.themes import Light

from dara_graph_viewer.definitions import GRAPH, NX_GRAPH


def color_graph(ctx: ActionContext):
    graph = CausalGraph.from_dict(ctx.inputs.new)
    for edge in graph.get_edges():
        # if not GRAPH.edge_exists(edge.source, edge.destination):
        #     print('hey')
        edge.meta = {'rendering_properties': {'color': Light.colors.success}}
    print('yo')
    return graph


def calculate_transitivity_index(graph: Dict):
    graph = CausalGraph.from_dict(graph)
    nx_graph_new = nx.from_edgelist(graph.get_edge_pairs())
    return nx.transitivity(nx_graph_new)


def calculate_recommendations(node: Dict):
    # all_triplets = nx.triangles(NX_GRAPH)
    # print(all_triplets)
    # print(node)
    return []


@py_component
def DisplayIndex(new_index: float):
    original_index = nx.transitivity(NX_GRAPH)
    if original_index > new_index:
        font_color = Light.colors.error
    elif original_index < new_index:
        font_color = Light.colors.success
    else:
        font_color = Light.colors.text

    return Stack(
        Text(round(original_index * 100, 2), font_size='2rem'),
        Text('→', font_size='2rem'),
        Text(round(new_index * 100, 2), font_size='2rem', color=font_color),
        direction='horizontal',
        justify='center',
        hug=True,
    )


@py_component
def RecommendationsAccordion(connections):
    return Stack()


def ConnectionsPage():
    graph_var = Variable(GRAPH)
    transitivity_var = DerivedVariable(
        calculate_transitivity_index,
        variables=[graph_var],
    )

    selected_node_var = Variable()
    connections_var = DerivedVariable(
        calculate_recommendations, variables=[selected_node_var]
    )

    return TabbedCard(
        Tab(
            Stack(
                CausalGraphViewer(
                    causal_graph=graph_var,
                    editor_mode=EditorMode.PAG,
                    editable=True,
                    disable_latent_node_add=True,
                    disable_node_removal=True,
                    # on_update=UpdateVariable(color_graph, variable=graph_var)
                ),
                Stack(
                    Text('Transitivity Index', font_size='1.2rem'),
                    Text(
                        'The Transitivity Index demonstrates how well your graph is connected out of its full connectivity potential. It is the ratio transitive triads to potential transitive triads.'
                    ),
                    Text(
                        'Try adding or deleting edges to see how it would affect the Transitivity Index of your social network.'
                    ),
                    DisplayIndex(transitivity_var),
                    Text(
                        'In the next tab, you can see recommended connections for each individual and how those connections would boos the Transitivity Index of your network.'
                    ),
                    Stack(
                        Button(
                            'Reset Graph',
                            onclick=ResetVariables(variables=[graph_var]),
                        ),
                        justify='end',
                    ),
                    width='calc(50% - 0.75rem)',
                ),
                direction='horizontal',
            ),
            title='Transitivity',
        ),
        Tab(
            Stack(
                CausalGraphViewer(
                    causal_graph=graph_var,
                    editor_mode=EditorMode.PAG,
                    on_click_node=UpdateVariable(
                        lambda ctx: ctx.inputs.new['identifier'],
                        variable=selected_node_var,
                    ),
                ),
                Stack(
                    Text('Connection Recommendations', font_size='1.2rem'),
                    Text(
                        "Select a node to see an individual's recommended connections based on a naive triad analysis."
                    ),
                    RecommendationsAccordion(connections_var),
                    width='calc(50% - 0.75rem)',
                ),
                direction='horizontal',
            ),
            title='Connection Recommendations',
        ),
    )
