import networkx as nx
import pandas as pd
from typing import List
from dara.components import Button, Card, Stack, Table, Text
from dara.core import DerivedDataVariable, DerivedVariable, UpdateVariable, ResetVariables, Variable, py_component
from dara.core.interactivity import ActionContext
from dara.components import CausalGraphViewer
from dara.components.graphs import EditorMode
from dara.core.visual.themes import Light
from dara_graph_viewer.definitions import GRAPH, NX_GRAPH
from dara_graph_viewer.utils import filter_friendships_data


def color_graph(nodes: List[str], path: List[str]):
    graph_copy = GRAPH.copy()
    for node in nodes:
        temp_node = graph_copy.get_node(node)
        temp_node.meta['rendering_properties']['color'] = Light.colors.violet
        temp_node.meta['rendering_properties']['label_color'] = Light.colors.grey1
    for i in range(0, len(path)):
        if path[i] not in nodes:
            temp_node = graph_copy.get_node(path[i])
            temp_node.meta['rendering_properties']['color'] = Light.colors.orange
            
        if i != len(path) - 1:
            if graph_copy.edge_exists(path[i], path[i + 1]):
                temp_edge = graph_copy.get_edge(path[i], path[i + 1])
                temp_edge.meta['rendering_properties']['color'] = Light.colors.orange
            elif graph_copy.edge_exists(path[i + 1], path[i]):
                temp_edge = graph_copy.get_edge(path[i + 1], path[i])
                temp_edge.meta['rendering_properties']['color'] = Light.colors.orange
    return graph_copy


def select_two_nodes(ctx: ActionContext):
    current_nodes: List = ctx.inputs.old
    current_nodes.append(ctx.inputs.new['identifier'])
    return current_nodes[-2:]


def calculate_dijikstras(nodes: List[str]):
    if len(nodes) == 2:
        return nx.dijkstra_path(NX_GRAPH, nodes[0], nodes[1])

    return []

def get_path_data(path: List[str]):
    data_list = []
    for i in range(0, len(path) - 1):
        data_list.append(filter_friendships_data((path[i], path[i + 1])))
    if data_list:
        return pd.concat(data_list)
    else:
        return pd.DataFrame(columns=['Individual 1', 'Individual 2', 'Interactions'])


def DisplayPath(
    nodes_var: Variable[List[str]],
    path_var: DerivedVariable[List[str]],
    path_data_var: DerivedDataVariable,
):
    @py_component
    def _display_path(_nodes: List[str], _path: List[str], _path_data: pd.DataFrame):
        if len(_nodes) == 2:
            return Card(
                Stack(
                    Text(f'Length of path: {len(_path)}'),
                    Text(f"Cumulative interactions along path: {_path_data['Interactions'].sum()}"),
                    gap='0.25rem',
                    hug=True,
                ),
                Table(data=path_data_var),
                Stack(
                    Button('Reset Node Selection', onclick=ResetVariables(variables=[nodes_var])),
                    justify='end',
                    hug=True,
                ),
                title=f"{_nodes[0]} → {_nodes[1]}"
            )
        else:
            return Stack()
        
    return _display_path(nodes_var, path_var, path_data_var)

def StrongestPathsPage():
    selected_nodes = Variable([])
    path_var = DerivedVariable(calculate_dijikstras, variables=[selected_nodes])
    path_data_var = DerivedDataVariable(get_path_data, variables=[path_var])
    graph_var = DerivedVariable(color_graph, variables=[selected_nodes, path_var])

    return Stack(
        CausalGraphViewer(
            causal_graph=graph_var,
            editor_mode=EditorMode.PAG,
            on_click_node=[
                UpdateVariable(select_two_nodes, variable=selected_nodes),
            ]
        ),
        Stack(
            Card(
                Text('Select two nodes to find the strongest connection path between two individuals. The strongest path is found by running Dijkstra\'s Shortest Path algorithm and setting the weights to their respective inverse as many interactions indicates a strong connection between two nodes. If you have two nodes selected, you must deselect one or more nodes before selecting a different one.'),
                title='Strongest Path',
                accent=True,
                hug=True,
            ),
            DisplayPath(selected_nodes, path_var, path_data_var),
            width='calc(50% - 0.75rem)',
        ),
        direction='horizontal',
    )
