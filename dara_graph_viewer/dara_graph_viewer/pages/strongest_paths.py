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
from typing import List

import networkx as nx
import pandas as pd
from cai_causal_graph import CausalGraph
from dara.core import ComponentInstance
from dara.components import Button, Card, CausalGraphViewer, Stack, Table, Text
from dara.components.graphs import EditorMode
from dara.core import (
    DerivedDataVariable,
    DerivedVariable,
    ResetVariables,
    UpdateVariable,
    Variable,
    py_component,
)
from dara.core.interactivity import ActionContext
from dara.core.visual.themes import Light

from dara_graph_viewer.definitions import GRAPH, NX_GRAPH
from dara_graph_viewer.utils import filter_friendships_data


def color_graph(nodes: List[str], path: List[str]) -> CausalGraph:
    """
    Color the graph according to the selected nodes and the resulting shortest path.
    Selected nodes are colored violet while nodes and edges along the path are colored orange.

    :param nodes: The list of selected nodes.
    :param path: The list of nodes along the shortest path, including the selected nodes.
    :return: A CausalGraph instance with the updated meta information.
    """
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


def select_two_nodes(ctx: ActionContext) -> List[str]:
    """
    Update the selected nodes list with the user's choice. If the user selects
    more than two nodes it will update the list to the two most recently chosen nodes.

    :param ctx: The `ActionContext` which holds the information from the action.
    :return: A list of two selected nodes.
    """
    current_nodes: List = ctx.inputs.old
    current_nodes.append(ctx.inputs.new['identifier'])
    return current_nodes[-2:]


def calculate_shortest_path(nodes: List[str]) -> List[str]:
    """
    Calculate the shortest path using Dijkstra's algorithm.

    :param nodes: The list of two nodes in which to find the shortest path to and from.
    :return: A list of nodes that represents the shortest path.
    """
    if len(nodes) == 2:
        return nx.dijkstra_path(NX_GRAPH, nodes[0], nodes[1])
    return []


def get_path_data(path: List[str]) -> pd.DataFrame:
    """
    Retrieve the friendship data for the given path.

    :param path: A list of nodes that represents the shortest path.
    :return: A `pandas.DataFrame` holding data pertaining to the nodes in the path.
    """
    data_list = []
    for i in range(0, len(path) - 1):
        data_list.append(filter_friendships_data((path[i], path[i + 1])))
    if data_list:
        return pd.concat(data_list)
    else:
        return pd.DataFrame(
            columns=['Individual 1', 'Individual 2', 'Interactions']
        )


def DisplayPath(
    nodes_var: Variable[List[str]],
    path_var: DerivedVariable[List[str]],
    path_data_var: DerivedDataVariable,
) -> ComponentInstance:
    """
    A component that displays information pertaining to the shortest path.

    :param nodes_var: A `Variable` holding the selected nodes.
    :param path_var: A `DerivedVariable` holding the shortest path.
    :param path_data_var: A `DerivedDataVariable` holding data pertaining to the shortest path.
    """
    @py_component
    def _display_path(
        _nodes: List[str], _path: List[str], _path_data: pd.DataFrame
    ) -> ComponentInstance:
        if len(_nodes) == 2:
            return Card(
                Stack(
                    Text(f'Length of path: {len(_path)}'),
                    Text(
                        f"Cumulative interactions along path: {_path_data['Interactions'].sum()}"
                    ),
                    gap='0.25rem',
                    hug=True,
                ),
                Table(data=path_data_var),
                Stack(
                    Button(
                        'Reset Node Selection',
                        onclick=ResetVariables(variables=[nodes_var]),
                    ),
                    justify='end',
                    hug=True,
                ),
                title=f'{_nodes[0]} → {_nodes[1]}',
            )
        else:
            return Stack()

    return _display_path(nodes_var, path_var, path_data_var)


def StrongestPathsPage() -> ComponentInstance:
    """
    A page-sized component that allows the user to explore the strongest path between
    two individuals in their network.

    This page highlights how the `on_click_node` argument of the `CausalGraphViewer` allows
    you to update your page based on what nodes the user selects in their graph.
    """
    selected_nodes = Variable([])
    path_var = DerivedVariable(
        calculate_shortest_path, variables=[selected_nodes]
    )
    path_data_var = DerivedDataVariable(get_path_data, variables=[path_var])
    graph_var = DerivedVariable(
        color_graph, variables=[selected_nodes, path_var]
    )

    return Stack(
        CausalGraphViewer(
            causal_graph=graph_var,
            editor_mode=EditorMode.PAG,
            on_click_node=[
                UpdateVariable(select_two_nodes, variable=selected_nodes),
            ],
        ),
        Stack(
            Card(
                Text(
                    "Select two nodes to find the strongest connection path between two individuals. The strongest path is found by running Dijkstra's Shortest Path algorithm and setting the weights to their respective inverse as many interactions indicate a strong connection between two nodes. If you have two nodes selected, you must deselect one or more nodes before selecting a different one."
                ),
                title='Strongest Path',
                accent=True,
                hug=True,
            ),
            DisplayPath(selected_nodes, path_var, path_data_var),
            width='calc(50% - 0.75rem)',
        ),
        direction='horizontal',
    )
