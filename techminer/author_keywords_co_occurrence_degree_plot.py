"""
Author keywords co-occurrence degree plot
===============================================================================

>>> from techminer import *
>>> directory = "/workspaces/techminer-api/data/"
>>> file_name = "/workspaces/techminer-api/sphinx/images/author_keywords_co_occurrence_degree_plot.png"
>>> author_keywords_co_occurrence_degree_plot(directory=directory).savefig(file_name)

.. image:: images/author_keywords_co_occurrence_degree_plot.png
    :width: 550px
    :align: center

"""

from .co_occurrence_matrix import co_occurrence_matrix
from .co_occurrence_network import co_occurrence_network
from .network_degree_plot import network_degree_plot


def author_keywords_co_occurrence_degree_plot(
    min_occ=2,
    max_occ=None,
    normalization=None,
    clustering_method="louvain",
    manifold_method=None,
    figsize=(8, 8),
    directory="./",
):

    coc_matrix = co_occurrence_matrix(
        column="author_keywords",
        min_occ=min_occ,
        max_occ=max_occ,
        association=normalization,
        directory=directory,
    )

    network = co_occurrence_network(
        co_occurrence_matrix=coc_matrix,
        clustering_method=clustering_method,
        manifold_method=manifold_method,
    )

    return network_degree_plot(
        network,
        figsize=figsize,
    )
