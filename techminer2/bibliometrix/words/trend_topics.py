# flake8: noqa
"""
Trend Topics
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__trend_topics.html"

>>> from techminer2 import bibliometrix
>>> bibliometrix.words.trend_topics(
...     'author_keywords',
...     directory=directory, 
... ).table_.head(20)
year                             OCC  year_q1  ...  global_citations  rn
author_keywords                                ...                      
corporate social responsibility    1     2017  ...                 1   0
credit                             1     2017  ...                 1   1
semantic technologies              2     2018  ...                41   0
smart contracts                    2     2017  ...                22   1
business models                    1     2018  ...               153   2
future research directions         1     2018  ...               153   3
algorithmic standards              1     2018  ...                21   4
financial services                 4     2018  ...               168   0
blockchain                         3     2018  ...                 5   1
sandbox                            2     2018  ...                12   2
standards                          1     2019  ...                33   3
dogmas                             1     2019  ...                 5   4
regtech                           28     2019  ...               329   0
fintech                           12     2019  ...               249   1
compliance                         7     2020  ...                30   2
regulation                         5     2018  ...               164   3
artificial intelligence            4     2020  ...                23   4
regulatory technology              7     2020  ...                37   0
financial regulation               4     2019  ...                35   1
anti-money laundering              3     2020  ...                21   2
<BLANKLINE>
[20 rows x 6 columns]





>>> bibliometrix.words.trend_topics(
...     'author_keywords', 
...     directory=directory,
... ).plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/bibliometrix__trend_topics.html" height="900px" width="100%" frameBorder="0"></iframe>



>>> bibliometrix.words.trend_topics(
...     'author_keywords',
...     custom_topics=[
...         "fintech",
...         "regulatory technology",
...         "blockchain",
...         "suptech",
...         "artificial intelligence",
...     ], 
...     directory=directory, 
... ).table_.head(10)
year                     OCC  year_q1  year_med  year_q3  global_citations  rn
author_keywords                                                               
blockchain                 3     2018      2019     2020                 5   0
fintech                   12     2019      2020     2020               249   0
artificial intelligence    4     2020      2020     2020                23   1
regulatory technology      7     2020      2021     2022                37   0
suptech                    3     2020      2022     2022                 4   0


"""
from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from ...techminer.indicators.indicators_by_item import indicators_by_item
from ...techminer.indicators.items_occ_by_year import items_occ_by_year


@dataclass(init=False)
class _Results:
    plot_: None
    table_: None


def trend_topics(
    criterion,
    n_words_per_year=5,
    custom_topics=None,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Trend topics"""

    words_by_year = items_occ_by_year(
        field=criterion,
        min_occ=1,
        root_dir=directory,
        database=database,
        year_filter=start_year,
        cited_by_filter=end_year,
        **filters,
    )

    if custom_topics is not None:
        words_by_year = words_by_year.loc[custom_topics, :]

    year_q1 = []
    year_med = []
    year_q3 = []

    for _, row in words_by_year.iterrows():
        sequence = []
        for item, year in zip(row, words_by_year.columns):
            if item > 0:
                sequence.extend([year] * int(item))

        year_q1.append(int(round(np.percentile(sequence, 25))))
        year_med.append(int(round(np.percentile(sequence, 50))))
        year_q3.append(int(round(np.percentile(sequence, 75))))

    words_by_year["year_q1"] = year_q1
    words_by_year["year_med"] = year_med
    words_by_year["year_q3"] = year_q3

    words_by_year = words_by_year.assign(
        OCC=words_by_year[words_by_year.columns[:-3]].sum(axis=1)
    )

    words_by_year = words_by_year[["OCC", "year_q1", "year_med", "year_q3"]]

    global_citations = indicators_by_item(
        criterion, root_dir=directory
    ).global_citations

    word2citation = dict(zip(global_citations.index, global_citations.values))
    words_by_year = words_by_year.assign(
        global_citations=words_by_year.index.map(word2citation)
    )

    words_by_year = words_by_year.sort_values(
        by=["year_med", "OCC", "global_citations"],
        ascending=[True, False, False],
    )

    words_by_year = words_by_year.assign(
        rn=words_by_year.groupby(["year_med"]).cumcount()
    ).sort_values(["year_med", "rn"], ascending=[True, True])

    words_by_year = words_by_year.query(f"rn < {n_words_per_year}")

    results = _Results()
    results.table_ = words_by_year

    min_occ = words_by_year.OCC.min()
    max_occ = words_by_year.OCC.max()
    words_by_year = words_by_year.assign(
        height=0.15
        + 0.82 * (words_by_year.OCC - min_occ) / (max_occ - min_occ)
    )
    words_by_year = words_by_year.assign(
        width=words_by_year.year_q3 - words_by_year.year_q1 + 1
    )

    fig = go.Figure(
        go.Bar(
            x=words_by_year.width,
            y=words_by_year.index,
            base=words_by_year.year_q1,
            width=words_by_year.height,
            orientation="h",
            marker_color="lightslategrey",
        ),
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_yaxes(
        linecolor="gray",
        linewidth=1,
        gridcolor="lightgray",
        griddash="dot",
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=1,
        gridcolor="lightgray",
        griddash="dot",
        tickangle=270,
        dtick=1.0,
    )
    results.plot_ = fig

    return results
