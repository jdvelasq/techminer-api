"""
Author keywords thematic network
===============================================================================

>>> from techminer import *
>>> directory = "/workspaces/techminer-api/data/"
>>> file_name = "/workspaces/techminer-api/sphinx/images/author_keywords_thematic_network.png"
>>> author_keywords_thematic_network(directory=directory).savefig(file_name)

.. image:: images/author_keywords_thematic_network.png
    :width: 650px
    :align: center

"""

from .co_occurrence_matrix import co_occurrence_matrix
from .co_occurrence_network import co_occurrence_network
from .network_plot import network_plot


def author_keywords_thematic_network(
    min_occ=2,
    figsize=(8, 8),
    k=0.2,
    iterations=50,
    max_labels=20,
    directory="./",
):

    coc_matrix = co_occurrence_matrix(
        column="author_keywords",
        min_occ=min_occ,
        normalization="association",
        directory=directory,
    )

    network = co_occurrence_network(
        co_occurrence_matrix=coc_matrix,
        clustering_method="louvain",
        manifold_method=None,
    )

    return network_plot(
        network,
        figsize=figsize,
        k=k,
        iterations=iterations,
        max_labels=max_labels,
    )
