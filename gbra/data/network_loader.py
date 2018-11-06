"""
Classes and routines for loading SNAP networks
"""

import abc
import os
import snap
import random

from gbra.util.ei_graph import EIGraph

class NetworkLoader(object):
    """Override this base class. Implement `load()` to return an EIGraph."""

    @abc.abstractmethod
    def load(self):
        """Construct or load a network into memory.

        returns an EIGraph
        """
        raise Exception('Override me')

class TinyTestLoader(NetworkLoader):
    """Returns a very simple undirected network with unweighted edges:

    Entity -> Items
    1 -> [2, 4, 6]
    3 -> [8]
    5 -> [4, 8]
    7 -> [6, 8, 10]
    9 -> [2, 10]
    11 -> [10]

    """

    def load(self):
        G = EIGraph(6, 5)
        G.add_edge(1, 2)
        G.add_edge(1, 4)
        G.add_edge(1, 6)
        G.add_edge(3, 8)
        G.add_edge(5, 4)
        G.add_edge(5, 8)
        G.add_edge(7, 6)
        G.add_edge(7, 8)
        G.add_edge(7, 10)
        G.add_edge(9, 2)
        G.add_edge(9, 10)
        G.add_edge(11, 10)

        return G

class ErdosRenyiLoader(NetworkLoader):
    """Erdos-Renyi graph bipartite graph.

    Parameterized by NUM_ENTITIES, NUM_ITEMS, and NUM_EDGES chosen uniformly
    at random between entities and items.
    """

    def __init__(self, num_entities, num_items, num_edges):
        """
        :param - num_entities: number of entities to include
        :param - num_items: number of items to include
        :param - num_edges: the number of edges desired.
        """
        if num_edges > num_entities * num_items:
            raise ValueError("More edges requested than possible.")

        self.num_entities = num_entities
        self.num_items = num_items
        self.num_edges = num_edges

    def load(self):
        # TODO: this will take a long time if num_edges is close
        # to num_items/num_entities. If we need to make graphs like this in
        # the future, please update my logic :)
        Graph = EIGraph(num_entities=self.num_entities, num_items=self.num_items)
        edges_left = self.num_edges
        while edges_left > 0:
            entity_node_id = 2 * random.randint(0, self.num_entities - 1) + 1
            item_node_id = 2 * random.randint(0, self.num_items - 1)
            if not Graph.is_edge(entity_node_id, item_node_id):
                edges_left -= 1
                print entity_node_id, item_node_id
                Graph.add_edge(entity_node_id, item_node_id)

        return Graph

class DataFileLoader(NetworkLoader):

    EXTENSION = '.dat'

    def __init__(self, filename):
        full_filename = os.path.join(os.path.dirname(__file__), filename)
        self.filename = full_filename + DataFileLoader.EXTENSION
        if not os.path.exists(self.filename):
            raise Exception(
                "{fn} does not exist, please load the corresponding data by"
                " executing:\n"
                "gbra/data/scripts/generate_{fn}.sh".format(fn=filename))

    def load(self):
        return EIGraph.load(self.filename)

class MovielensLoader(DataFileLoader):
    """Loads the small Movielens dataset.

    For more info, see:
    http://files.grouplens.org/datasets/movielens/ml-1m-README.txt
    """

    def __init__(self):
        super(MovielensLoader, self).__init__('movielens')


class BeeradvocateLoader(DataFileLoader):
    """Loads the SNAP BeerAdvocate dataset.

    For more info, see:
    https://snap.stanford.edu/data/web-BeerAdvocate.html
    (inspect the HTML)
    """

    def __init__(self):
        super(BeeradvocateLoader, self).__init__('beeradvocate')
