"""
Thematic analysis
===============================================================================

The implemented methodology is based on the Thematic Analysis of Elementary
Contexts implemented in T-LAB.



>>> from techminer2 import *
>>> from sklearn.cluster import KMeans
>>> from sklearn.manifold import MDS
>>> directory = "/workspaces/techminer-api/data/"
>>> tfidf_matrix = tf_idf_matrix('author_keywords', min_occ=3, directory=directory)
>>> thematic_analysis(
...     tfidf_matrix, 
...     clustering_method=KMeans(n_clusters=6, random_state=0), 
...     manifold_method=MDS(random_state=0)
... ).themes_by_words_
author_keywords    fintech  ... open innovation
#d                     139  ...             3  
#c                    1285  ...            12  
THEME_0           3.531425  ...        0.000000
THEME_1           4.109095  ...        0.000000
THEME_2          15.040339  ...        1.521395
THEME_3          21.000000  ...        0.000000
THEME_4           2.715340  ...        0.000000
THEME_5           2.014328  ...        0.628626
<BLANKLINE>
[6 rows x 59 columns]

>>> file_name = "/workspaces/techminer-api/sphinx/images/thematic_analysis_map.png"
>>> thematic_analysis(
...     tfidf_matrix, 
...     clustering_method=KMeans(n_clusters=6), 
...     manifold_method=MDS()
... ).map().savefig(file_name)

.. image:: images/thematic_analysis_map.png
    :width: 700px
    :align: center

"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import MDS

from .plots import bubble_map


class ThematicAnalysis:
    def __init__(self, tf_idf_matrix, manifold_method=None, clustering_method=None):
        self.tf_idf_matrix = tf_idf_matrix.copy()
        if clustering_method is None:
            clustering_method = KMeans(n_clusters=6)
        if manifold_method is None:
            manifold_method = MDS(n_components=20, random_state=0)
        self.clustering_method = clustering_method
        self.manifold_method = manifold_method
        self.themes_by_words_ = None
        self.run()

    def run(self):

        self.clustering_method.fit(self.tf_idf_matrix)
        clustered_tf_idf_matrix = self.tf_idf_matrix.copy()
        clustered_tf_idf_matrix["CLUSTER"] = self.clustering_method.labels_
        themes_by_words = clustered_tf_idf_matrix.groupby("CLUSTER").sum()
        themes_by_words.index = [
            "THEME_{:d}".format(i) for i in range(len(themes_by_words))
        ]
        self.themes_by_words_ = themes_by_words.copy()

        new_n_components = self.clustering_method.get_params()["n_clusters"] - 1
        self.manifold_method.set_params(n_components=new_n_components)
        decomposed_themes_by_words_ = self.manifold_method.fit_transform(
            themes_by_words
        )

        self.decomposed_themes_by_words_ = pd.DataFrame(
            decomposed_themes_by_words_,
            columns=[f"DIM-{i}" for i in range(new_n_components)],
            index=["THEME_{:d}".format(i) for i in range(len(themes_by_words))],
        )

        self.num_documents_by_theme_ = clustered_tf_idf_matrix.groupby("CLUSTER").size()

        self.cluster_centers_ = self.clustering_method.cluster_centers_

    def map(self, dim_x=0, dim_y=1, color_scheme="clusters", figsize=(7, 7)):

        return bubble_map(
            node_x=self.decomposed_themes_by_words_["DIM-{:d}".format(dim_x)],
            node_y=self.decomposed_themes_by_words_["DIM-{:d}".format(dim_y)],
            node_clusters=range(len(self.decomposed_themes_by_words_)),
            node_texts=self.decomposed_themes_by_words_.index.tolist(),
            node_sizes=self.num_documents_by_theme_,
            x_axis_at=0,
            y_axis_at=0,
            color_scheme=color_scheme,
            xlabel=f"X-Axis (Dim-{dim_x})",
            ylabel=f"Y-Axis (Dim-{dim_y})",
            figsize=figsize,
            fontsize=7,
        )

    # def table(self):
    #     return self.co_occurrence_network.table()

    # def network(self):
    #     return self.co_occurrence_network.plot()

    # def clusters(self):
    #     return self.clusters_
