"""
Words Radial Diagram
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/tlab__words_radial_diagram.html"

>>> from techminer2 import tlab__words_radial_diagram
>>> tlab__words_radial_diagram(
...     term="regtech",
...     min_occ=4,
...     column='author_keywords',
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../../../../_static/tlab__words_radial_diagram.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
import networkx as nx

from .get_network_graph_plot import network_graph_plot
from .vantagepoint__co_occ_matrix_list import vantagepoint__co_occ_matrix_list


def tlab__words_radial_diagram(
    term,
    column,
    top_n=None,
    min_occ=None,
    max_occ=None,
    directory="./",
    database="documents",
):
    """Creates a radial diagram of term associations from a co-occurrence matrix."""

    matrix_list = vantagepoint__co_occ_matrix_list(
        column=column,
        row=None,
        top_n=None,
        min_occ=None,
        max_occ=None,
        directory=directory,
        database=database,
    )

    matrix_list = matrix_list[
        matrix_list["row"].map(lambda x: " ".join(x.split()[:-1]) == term)
    ]

    if min_occ is not None:
        matrix_list = matrix_list[matrix_list["OCC"] >= min_occ]

    if max_occ is not None:
        matrix_list = matrix_list[matrix_list["OCC"] <= max_occ]

    if top_n is not None:
        matrix_list = matrix_list.head(top_n)

    # create a empty network
    graph = nx.Graph()

    # add nodes
    nodes = [
        (node, dict(size=occ, group=0))
        for node, occ in zip(matrix_list["column"], matrix_list["OCC"])
    ]
    graph.add_nodes_from(nodes)

    # add network edges
    edges = []
    for _, row in matrix_list.iterrows():
        if row[0] != row[1]:
            edges.append((row[0], row[1], row[2]))
    graph.add_weighted_edges_from(edges)

    # create a network plot
    fig = network_graph_plot(
        graph,
        nx_k=0.5,
        nx_iteratons=10,
        delta=1.0,
    )

    return fig
