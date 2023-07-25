import networkx as nx
import plotly.express as px
import numpy as np
import bisect

from typing import Dict
from dara.components import Card, Modal, Select, Stack, Text
from dara.core import DerivedVariable, Variable, py_component
from dara.components import CausalGraphViewer
from dara.components.graphs import EditorMode
from dara.components.plotting import Plotly
from dara_graph_viewer.definitions import GRAPH, NX_GRAPH

COLOR_PALETTE = px.colors.sequential.Redor

# For every pair of vertices in a connected graph, there exists at least one shortest path between the vertices such that either the number of edges that the path passes through (for unweighted graphs) or the sum of the weights of the edges (for weighted graphs) is minimized. The betweenness centrality for each vertex is the number of these shortest paths that pass through the vertex

CENTRALITY_DEFINITIONS = {
    'Degree Centrality': 'The degree centrality of a node is the number of edges associated with it. The higher the degree, the more central the node is. The degree centrality is then normalized.',
    'Betweenness Centrality': 'The betweenness centrality of a node is based on the shortest paths. For every pair of nodes in a connected graph, there exists at least one shortest path between the them. The betweenness centrality for each node is the number of these shortest paths that pass through the node.',
    'Eigenvector Centrality': 'A high eigenvector score means that a node is connected to many nodes who themselves have high scores.',
}

def calculate_centrality(measure: str):
    if measure == 'Degree Centrality':
        return nx.degree_centrality(NX_GRAPH)
    elif measure == 'Betweenness Centrality':
        return nx.betweenness_centrality(NX_GRAPH)
    else:
        return nx.eigenvector_centrality(NX_GRAPH)


def color_graph(scores: Dict[str, float]):
    graph = GRAPH.copy()
    
    score_linspace = np.linspace(min([*scores.values()]), max([*scores.values()]), len(COLOR_PALETTE))
    for name, value in scores.items():
        ind = bisect.bisect_left(score_linspace, value)
        node = graph.get_node(name)
        node.meta = {'rendering_properties': {'color': COLOR_PALETTE[ind], 'label_color': 'white'}}

    return graph

@py_component
def CentralityScoresGraph(measure: str, scores: Dict[str, float]):
    fig = px.bar(
        {'Name': scores.keys(), 'Value': scores.values()},
        x='Value',
        y='Name',
        orientation='h',
        color='Value',
        color_continuous_scale=COLOR_PALETTE,
    )
    return Stack(
        Text(CENTRALITY_DEFINITIONS[measure]),
        Plotly(fig)
    )


def InfluentialIndividualsPage():
    selected_measure = Variable('Degree Centrality')
    show_report_modal = Variable(False)
    centrality_scores = DerivedVariable(
        calculate_centrality, variables=[selected_measure]
    )
    scored_graph = DerivedVariable(
        color_graph, variables=[centrality_scores]
    )

    return Stack(
        CausalGraphViewer(causal_graph=scored_graph, editor_mode=EditorMode.PAG),
        Card(
            Text('Select a centrality measure. The color of the nodes in the graph will reflect its respective centrality score.'),
            Stack(
                Text('Centrality Measure', width='30%'),
                Select(
                    items=[
                        'Degree Centrality',
                        'Betweenness Centrality',
                        'Eigenvector Centrality'
                    ],
                    value=selected_measure,
                ),
                direction='horizontal',
                hug=True,
            ),
            CentralityScoresGraph(selected_measure, centrality_scores),
            title='Influential Individuals',
            width='calc(50% - 0.75rem)',
        ),
        Modal(show=show_report_modal, width='80vw', height='50vh'),
        direction='horizontal',
    )
