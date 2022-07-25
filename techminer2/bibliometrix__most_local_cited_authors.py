"""
Most Local Cited Authors
===============================================================================




>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__most_local_cited_authors.html"


>>> from techminer2 import bibliometrix__most_local_cited_authors
>>> bibliometrix__most_local_cited_authors(
...     topics_length=20,
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/bibliometrix__most_local_cited_authors.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .vantagepoint__chart import vantagepoint__chart


def bibliometrix__most_local_cited_authors(
    directory="./",
    topics_length=20,
    plot="cleveland",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Most Local Cited Authors (from Reference Lists)."""

    return vantagepoint__chart(
        criterion="authors",
        directory=directory,
        database=database,
        metric="local_citations",
        start_year=start_year,
        end_year=end_year,
        topics_length=topics_length,
        min_occ=None,
        max_occ=None,
        custom_topics=None,
        title="Most Local Cited Authors (from Reference Lists)",
        plot=plot,
        **filters,
    )
