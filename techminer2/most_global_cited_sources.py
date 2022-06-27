"""
Most global cited sources
===============================================================================

>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/most_global_cited_sources.html"


>>> most_global_cited_sources(
...     directory,
...     top_n=20,
...     plot="bar",
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/most_global_cited_sources.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .plot_metric_by_item import plot_metric_by_item


def most_global_cited_sources(
    directory="./",
    top_n=20,
    min_occ=None,
    max_occ=None,
    title="Most global cited sources",
    plot="bar",
):
    """Plots the number of global citations by source name using the specified plot."""

    return plot_metric_by_item(
        column="iso_source_name",
        metric="global_citations",
        directory=directory,
        top_n=top_n,
        min_occ=min_occ,
        max_occ=max_occ,
        title=title,
        plot=plot,
        file_name="documents.csv",
    )
