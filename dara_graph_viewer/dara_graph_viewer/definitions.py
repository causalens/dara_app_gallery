import pandas as pd
import networkx as nx
from cai_causal_graph import CausalGraph

from dara.core.visual.themes import Light

FRIENDSHIPS_DATA = pd.read_csv('data/friendships.csv', index_col=0)
INTERACTIONS_DATA = pd.read_csv('data/interactions.csv', index_col=0)

def build_graph(friendships: pd.DataFrame):
    graph = CausalGraph()

    for _, row in friendships.iterrows():
        if (
            graph.edge_exists(row['Individual 1'], row['Individual 2'])
            or graph.edge_exists(row['Individual 2'], row['Individual 1'])
        ):  
            continue
        graph.add_edge(
            row['Individual 1'], row['Individual 2'],
            edge_type='<>',
            meta={'rendering_properties': {'tooltip': f"{row['Interactions']} interactions"}}
        )
    for node in graph.get_nodes():
        node.meta = {'rendering_properties': {'color': Light.colors.blue4, 'highlight_color': Light.colors.primary, 'label_color': Light.colors.text}}

    return graph

def build_nx_graph(friendships: pd.DataFrame):
    nx_graph = nx.Graph()
    
    for _, row in friendships.iterrows():
        if (
            nx_graph.get_edge_data(row['Individual 1'], row['Individual 2'])
            or nx_graph.get_edge_data(row['Individual 2'], row['Individual 1'])
        ):  
            continue
        nx_graph.add_edge(
            row['Individual 1'],
            row['Individual 2'],
            weight=1/row['Interactions'],
        )
        nx_graph.add_edge(
            row['Individual 2'],
            row['Individual 1'],
            weight=1/row['Interactions'],
        )

    return nx_graph

GRAPH = build_graph(FRIENDSHIPS_DATA)
NX_GRAPH = build_nx_graph(FRIENDSHIPS_DATA)

