import networkx as nx
import pandas as pd
import numpy as np
from nose import with_setup

from pybbn.learn.cb import get_mwst_skeleton, get_v_structures, MwstAlgo
from pybbn.learn.data import DiscreteData


def setup():
    """
    Setup.
    :return: None.
    """
    np.random.seed(37)


def teardown():
    """
    Teardown.
    :return: None.
    """


def get_good_df():
    """
    Gets a good dataframe.
    :return: Dataframe.
    """
    return pd.DataFrame({
        'x1': ['t', 't', 't', 't', 't', 'f', 'f', 'f', 'f', 'f'],
        'x2': ['t', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f'],
        'x3': ['t', 't', 't', 't', 't', 't', 'f', 'f', 'f', 'f'],
        'x4': ['t', 't', 't', 't', 't', 'f', 'f', 'f', 'f', 'f']
    })


@with_setup(setup, teardown)
def test_get_mwst_skeleton():
    """
    Tests getting the MWST skeleton structure.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    g = get_mwst_skeleton(data)
    assert len(g.nodes) == 4


@with_setup(setup, teardown)
def test_get_v_structures():
    """
    Tests getting all the v-structures from an undirected graph.
    :return: None.
    """
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(2, 3)

    v_structures = get_v_structures(g)
    assert len(v_structures) == 2
    assert (1, 0, 2) in v_structures
    assert (0, 2, 3) in v_structures


@with_setup(setup, teardown)
def test_fit():
    """
    Tests fitting data.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    mwst = MwstAlgo()
    mwst.fit(data)

    bbn = mwst.bbn
    assert 4 == len(bbn.nodes)
    assert 3 == len(bbn.edges)
