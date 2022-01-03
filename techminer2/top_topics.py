"""
Top Topics
===============================================================================

Extract and plot the top topics of the selected column.


>>> from techminer2 import *
>>> directory = "/workspaces/techminer2/data/"
>>> file_name = "/workspaces/techminer2/sphinx/images/top_topics.png"
>>> top_topics(
...     column="author_keywords", 
...     directory=directory,
... ).savefig(file_name)

.. image:: images/top_topics.png
    :width: 700px
    :align: center


>>> top_topics(
...     column='author_keywords',
...     directory=directory, 
...     plot=False,
... ).head()
                        before 2020  between 2020-2021
fintech                          42                 97
financial technologies           11                 17
financial inclusion               4                 13
block-chain                       9                  8
innovating                        9                  4


"""

from .growth_indicators import growth_indicators
from .stacked_bar_chart import stacked_bar_chart


def top_topics(
    column,
    top_n=20,
    time_window=2,
    figsize=(6, 6),
    directory="./",
    plot=True,
):

    indicators = growth_indicators(column, time_window=time_window, directory=directory)
    indicators = indicators[indicators.columns[:2]]
    indicators = indicators.assign(
        num_documents=indicators[indicators.columns[0]]
        + indicators[indicators.columns[1]]
    )
    indicators = indicators.sort_values(by="num_documents", ascending=False)
    indicators.pop("num_documents")

    if plot is False:
        return indicators

    indicators = indicators.head(top_n)

    return stacked_bar_chart(
        indicators,
        title="Total Num Documents",
        xlabel="Num Documents",
        ylabel=column,
        figsize=figsize,
    )
