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
import networkx as nx
import pandas as pd
from cai_causal_graph import CausalGraph
from dara.core.visual.themes import Light

FRIENDSHIPS_DATA = pd.read_csv('data/friendships.csv', index_col=0)
INTERACTIONS_DATA = pd.read_csv('data/interactions.csv', index_col=0)


def build_graph(friendships: pd.DataFrame):
    """
    Build a CausalGraph from the friendships in the dataset.
    The meta of the CausalGraph is updated so that the interactions between
    two nodes are shown when hovering over an edge. The meta can also specify
    aesthetic properties like background color and text color. 
    """
    graph = CausalGraph()

    for _, row in friendships.iterrows():
        if graph.edge_exists(
            row['Individual 1'], row['Individual 2']
        ) or graph.edge_exists(row['Individual 2'], row['Individual 1']):
            continue
        graph.add_edge(
            row['Individual 1'],
            row['Individual 2'],
            edge_type='<>',
            meta={
                'rendering_properties': {
                    'tooltip': f"{row['Interactions']} interactions"
                }
            },
        )
    for node in graph.get_nodes():
        node.meta = {
            'rendering_properties': {
                'color': Light.colors.blue4,
                'highlight_color': Light.colors.primary,
                'label_color': Light.colors.text,
            }
        }

    return graph


def build_nx_graph(friendships: pd.DataFrame):
    """Build a Networkx graph from the friendships in the dataset."""
    nx_graph = nx.Graph()

    for _, row in friendships.iterrows():
        if nx_graph.get_edge_data(
            row['Individual 1'], row['Individual 2']
        ) or nx_graph.get_edge_data(row['Individual 2'], row['Individual 1']):
            continue
        # Dijkstra's algorithm finds the shortest path with the smallest weights.
        # As you will want to find the shortest path with the strongest connections,
        # the weights should be the inverse of the interactions so that smaller weights
        # equate to more interactions.
        nx_graph.add_edge(
            row['Individual 1'],
            row['Individual 2'],
            weight=1 / row['Interactions'],
        )
        nx_graph.add_edge(
            row['Individual 2'],
            row['Individual 1'],
            weight=1 / row['Interactions'],
        )

    return nx_graph


GRAPH = build_graph(FRIENDSHIPS_DATA)
NX_GRAPH = build_nx_graph(FRIENDSHIPS_DATA)
