"""
Most local cited institutions (from reference lists) **(NEW)**
===============================================================================

See :doc:`column indicators <column_indicators>` to obtain a `pandas.Dataframe` 
with the data. In this case, use:

.. code:: python

    column_indicators(
        column="institutions",
        directory=directory,
        database="references",
    )


>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/most_local_cited_institutions.html"

>>> most_local_cited_institutions(
...     top_n=20,
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/most_local_cited_institutions.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .bar_chart import bar_chart
from .circle_chart import circle_chart
from .cleveland_chart import cleveland_chart
from .column_chart import column_chart
from .line_chart import line_chart
from .word_cloud import word_cloud


def most_local_cited_institutions(
    directory="./",
    top_n=20,
    plot="cleveland",
):
    """Most local cited institutions from reference lists."""

    plot_function = {
        "bar": bar_chart,
        "column": column_chart,
        "line": line_chart,
        "circle": circle_chart,
        "cleveland": cleveland_chart,
        "wordcloud": word_cloud,
    }[plot]

    return plot_function(
        column="institutions",
        metric="local_citations",
        directory=directory,
        top_n=top_n,
        min_occ=None,
        max_occ=None,
        title="Most local cited institutions from reference lists",
        database="references",
    )
