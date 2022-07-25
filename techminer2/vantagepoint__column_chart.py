"""
Column chart
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/vantagepoint__column_chart.html"

>>> from techminer2 import vantagepoint__column_chart
>>> vantagepoint__column_chart(
...     criterion='author_keywords',
...     topics_length=15,
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../_static/vantagepoint__column_chart.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .vantagepoint__chart import vantagepoint__chart


def vantagepoint__column_chart(
    criterion,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    topics_length=20,
    min_occ=None,
    max_occ=None,
    custom_topics=None,
    title=None,
    **filters
):
    """Plots a bar chart from a column of a dataframe."""

    return vantagepoint__chart(
        criterion=criterion,
        directory=directory,
        database=database,
        metric="OCC",
        start_year=start_year,
        end_year=end_year,
        topics_length=topics_length,
        min_occ=min_occ,
        max_occ=max_occ,
        custom_topics=custom_topics,
        title=title,
        plot="bar",
        **filters,
    )
