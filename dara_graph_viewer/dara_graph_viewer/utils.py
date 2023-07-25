from typing import Optional, Tuple
import pandas as pd

from dara_graph_viewer.definitions import INTERACTIONS_DATA, FRIENDSHIPS_DATA

def filter_interactions_data(edge: Optional[Tuple[str, str]]):
    if edge is None:
        return INTERACTIONS_DATA
    filter1 = INTERACTIONS_DATA[(INTERACTIONS_DATA['Individual 1'] == edge[0]) & (INTERACTIONS_DATA['Individual 2'] == edge[1])]
    filter2 = INTERACTIONS_DATA[(INTERACTIONS_DATA['Individual 1'] == edge[1]) & (INTERACTIONS_DATA['Individual 2'] == edge[0])]
    return pd.concat([filter1, filter2])


def filter_friendships_data(edge: Optional[Tuple[str, str]]):
    if edge is None:
        return FRIENDSHIPS_DATA
    filter1 = FRIENDSHIPS_DATA[(FRIENDSHIPS_DATA['Individual 1'] == edge[0]) & (FRIENDSHIPS_DATA['Individual 2'] == edge[1])]
    filter2 = FRIENDSHIPS_DATA[(FRIENDSHIPS_DATA['Individual 1'] == edge[1]) & (FRIENDSHIPS_DATA['Individual 2'] == edge[0])]
    return pd.concat([filter1, filter2])