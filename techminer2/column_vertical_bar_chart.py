"""
Column Vertical Bar Chart
===============================================================================

>>> from techminer2 import *
>>> directory = "/workspaces/techminer2/data/"
>>> file_name = "/workspaces/techminer2/sphinx/images/column_vertical_bar_chart.png"
>>> column_vertical_bar_chart('author_keywords', 15, directory=directory).savefig(file_name)

.. image:: images/column_vertical_bar_chart.png
    :width: 700px
    :align: center


>>> column_vertical_bar_chart('author_keywords', 15, directory=directory, plot=False).head()
                        num_documents  global_citations  local_citations
author_keywords                                                         
fintech                           139              1285              218
financial technologies             28               225               41
financial inclusion                17               339               61
block-chain                        17               149               22
bank                               13               193               23

"""

import os

from .column_indicators import column_indicators
from .vertical_bar_chart import vertical_bar_chart


def column_vertical_bar_chart(
    column,
    top_n=10,
    figsize=(8, 6),
    directory="./",
    cmap="Blues",
    plot=True,
):

    indicators = column_indicators(column=column, directory=directory)
    indicators = indicators.sort_values(by="num_documents", ascending=False)

    if plot is False:
        return indicators

    series = indicators.num_documents.head(top_n)
    darkness = indicators.global_citations.head(top_n)
    return vertical_bar_chart(
        series,
        darkness=darkness,
        cmap=cmap,
        figsize=figsize,
        edgecolor="k",
        linewidth=0.5,
        title=None,
        xlabel=None,
        ylabel=None,
        zorder=10,
    )
