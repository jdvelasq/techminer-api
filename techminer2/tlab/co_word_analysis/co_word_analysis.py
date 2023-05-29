"""
Co-Word Analysis
===============================================================================


>>> directory = "data/regtech/"


>>> from sklearn.cluster import AgglomerativeClustering


>>> from techminer2 import tlab
>>> cwa = tlab.co_word_analysis.co_word_analysis(
...     criterion='words',
...     topics_length=50,
...     clustering_method=AgglomerativeClustering(n_clusters=5),
...     directory=directory,
... )

>>> file_name = "sphinx/_static/tlab__co_word_analysis__co_word_analysis_mds_map.html"
>>> cwa.mds_map_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/tlab__co_word_analysis__co_word_analysis_mds_map.html" height="600px" width="100%" frameBorder="0"></iframe>


>>> file_name = "sphinx/_static/tlab__co_word_analysis__co_word_analysis_tsne_map.html"
>>> cwa.tsne_map_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/tlab__co_word_analysis__co_word_analysis_tsne_map.html" height="600px" width="100%" frameBorder="0"></iframe>



>>> print(cwa.communities_.to_markdown())
|    | CL_00                        | CL_01                               | CL_02                          | CL_03              | CL_04                        |
|---:|:-----------------------------|:------------------------------------|:-------------------------------|:-------------------|:-----------------------------|
|  0 | blockchain technology 02:021 | blockchain 03:005                   | anti-money laundering 05:024   | charitytech 02:017 | disruptive innovation 02:154 |
|  1 | data protection 02:027       | business models 03:156              | artificial intelligence 08:036 | english law 02:017 | market participants 02:154   |
|  2 | digital identity 03:185      | cost savings 03:014                 | compliance 07:030              |                    | regulatory system 02:154     |
|  3 | distributed ledger 02:022    | digital innovation 04:165           | compliance costs 06:033        |                    |                              |
|  4 | financial stability 02:154   | digital transformation 03:015       | finance 07:017                 |                    |                              |
|  5 | money laundering 02:017      | financial markets 04:151            | financial crisis 07:058        |                    |                              |
|  6 | operational risk 02:021      | financial services 06:195           | financial institutions 16:198  |                    |                              |
|  7 | semantic technologies 02:041 | financial services industry 05:315  | financial regulation 12:395    |                    |                              |
|  8 |                              | financial system 06:339             | financial sector 07:169        |                    |                              |
|  9 |                              | financial technology 06:173         | fintech 12:249                 |                    |                              |
| 10 |                              | innovation 03:012                   | global financial crisis 06:177 |                    |                              |
| 11 |                              | regulation 05:164                   | information technology 06:177  |                    |                              |
| 12 |                              | regulation technology 03:001        | machine learning 05:014        |                    |                              |
| 13 |                              | regulatory framework 03:002         | new technologies 05:012        |                    |                              |
| 14 |                              | regulatory requirements 03:002      | regtech 28:329                 |                    |                              |
| 15 |                              | smart contracts 04:024              | regulatory compliance 15:232   |                    |                              |
| 16 |                              | suptech 03:004                      | regulatory technology 20:274   |                    |                              |
| 17 |                              | systematic literature review 03:004 | risk management 05:019         |                    |                              |
| 18 |                              |                                     | technological solutions 06:016 |                    |                              |





"""
from dataclasses import dataclass

import pandas as pd
import plotly.express as px
from sklearn.manifold import MDS, TSNE
from sklearn.metrics.pairwise import (
    cosine_distances,
    euclidean_distances,
    haversine_distances,
)

from ...matrix_normalization import matrix_normalization
from ...scatter_plot import scatter_plot
from ...vantagepoint.analyze.co_occ_matrix import co_occ_matrix


@dataclass(init=False)
class _Results:
    communities_: None
    mds_map_: None
    tsne_map_: None


def co_word_analysis(
    criterion,
    topics_length=None,
    topic_min_occ=None,
    topic_min_citations=None,
    normalization="association",
    #
    distance_metric="euclidean_distances",
    clustering_method=None,
    #
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Word Association"""

    if criterion not in [
        "raw_author_keywords",
        "raw_index_keywords",
        "raw_title_words",
        "raw_abstract_words",
        "raw_words",
        "author_keywords",
        "index_keywords",
        "title_words",
        "abstract_words",
        "words",
    ]:
        raise ValueError(
            "criterion must be one of: "
            "{'author_keywords', 'index_keywords', 'title_words', 'abstract_words', 'words', "
            "{'raw_author_keywords', 'raw_index_keywords', 'raw_title_words', 'raw_abstract_words', "
            "'raw_words'}"
        )

    #
    # Algorithm:
    #

    matrix = co_occ_matrix(
        criterion=criterion,
        topics_length=topics_length,
        topic_min_occ=topic_min_occ,
        topic_min_citations=topic_min_citations,
        root_dir=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    matrix = matrix_normalization(matrix, association=normalization)

    if distance_metric == "euclidean_distances":
        distance_metric_fn = euclidean_distances
    elif distance_metric == "cosine_distances":
        distance_metric_fn = cosine_distances
    elif distance_metric == "haversine_distance":
        distance_metric_fn = haversine_distances
    else:
        raise ValueError(
            "distance_metric must be one of: "
            "{'euclidean_distances', 'cosine_distances', 'haversine_distance'}"
        )

    dissimilarity_matrix = pd.DataFrame(
        distance_metric_fn(matrix),
        columns=matrix.columns,
        index=matrix.columns,
    )

    clustering_method.fit(dissimilarity_matrix)

    results = _Results()
    results.communities_ = _get_matrix_communities(
        clustering_method, dissimilarity_matrix
    )
    results.mds_map_ = _get_manifold_map(
        matrix=dissimilarity_matrix,
        clustering_method=clustering_method,
        manifold_method=MDS(n_components=2),
    )

    results.tsne_map_ = _get_manifold_map(
        matrix=dissimilarity_matrix,
        clustering_method=clustering_method,
        manifold_method=TSNE(n_components=2),
    )

    return results


def _get_manifold_map(matrix, clustering_method, manifold_method):
    transformed_matrix = manifold_method.fit_transform(matrix)

    nodes = matrix.index.to_list()
    node_occ = [int(name.split()[-1].split(":")[0]) for name in nodes]
    node_global_citations = [
        int(name.split()[-1].split(":")[-1]) for name in nodes
    ]

    manifold_data = pd.DataFrame(
        {
            "node": nodes,
            "OCC": node_occ,
            "global_citations": node_global_citations,
        }
    )

    manifold_data["Dim-0"] = transformed_matrix[:, 0]
    manifold_data["Dim-1"] = transformed_matrix[:, 1]

    manifold_data["cluster"] = clustering_method.labels_

    manifold_data["color"] = manifold_data["cluster"].map(
        lambda x: px.colors.qualitative.Dark24[x]
        if x < 24
        else px.colors.qualitative.Light24[x]
    )

    fig = scatter_plot(
        node_x=manifold_data["Dim-0"],
        node_y=manifold_data["Dim-1"],
        node_text=manifold_data["node"],
        node_color=manifold_data["color"],
        node_size=manifold_data["OCC"],
    )

    return fig


def _get_matrix_communities(clustering_method, dissimilarity_matrix):
    """Extracts communities from a dissimilarity matrix"""

    communities = {}
    for cluster_id, cluster in enumerate(clustering_method.labels_):
        text = f"CL_{cluster :02d}"
        if text not in communities:
            communities[text] = []
        communities[text].append(dissimilarity_matrix.columns[cluster_id])

    for key, items in communities.items():
        communities[key] = sorted(items)

    pdf = pd.DataFrame.from_dict(communities, orient="index").T
    pdf = pdf.fillna("")
    pdf = pdf.sort_index(axis=1)

    return pdf
