"""
Factorial analysis using MDS and agglomerative clustering / Data
===============================================================================


>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "/workspaces/techminer2/sphinx/images/factorial_analysis_mds_map.png"
>>> factorial_analysis_mds_data(
...     'author_keywords', 
...     min_occ=2, 
...     n_clusters=4, 
...     directory=directory,
... ).head()
                                     Dim-1       Dim-2  Cluster
author_keywords        #d  #c                                  
fintech                139 1285 -65.034339  125.407802        3
financial technologies 28  225   24.277541   19.566110        1
financial inclusion    17  339  -16.789895   12.926560        2
blockchain             17  149   -0.898967   20.773784        2
bank                   12  185  -16.571064   -3.766202        0


"""

from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import MDS

from .co_occurrence_matrix import co_occurrence_matrix
from .factorial_analysis_manifold import Factorial_analysis_manifold


def factorial_analysis_mds_data(
    column,
    min_occ=2,
    max_occ=None,
    n_clusters=2,
    random_state=0,
    directory="./",
):
    coc_matrix = co_occurrence_matrix(
        column=column,
        min_occ=min_occ,
        max_occ=max_occ,
        normalization=None,
        directory=directory,
    )

    manifold_method = MDS(n_components=2, random_state=random_state)
    clustering_method = AgglomerativeClustering(n_clusters=n_clusters)

    estimator = Factorial_analysis_manifold(
        matrix=coc_matrix,
        manifold_method=manifold_method,
        clustering_method=clustering_method,
    )

    return estimator.data()
