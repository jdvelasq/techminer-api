"""
Num documents by source (Most relevant sources)
===============================================================================

>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/num_documents_by_source.html"

>>> num_documents_by_source(
...     directory,
...     top_n=20,
...     plot="cleveland",
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/num_documents_by_source.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .plot_metric_by_item import plot_metric_by_item


def num_documents_by_source(
    directory="./",
    top_n=20,
    min_occ=None,
    max_occ=None,
    title="Num documents by source",
    plot="bar",
):
    """Plots the number of documents by source using the specified plot."""

    return plot_metric_by_item(
        column="iso_source_name",
        metric="num_documents",
        directory=directory,
        top_n=top_n,
        min_occ=min_occ,
        max_occ=max_occ,
        title=title,
        plot=plot,
    )
