"""
Most Local Cited Authors
===============================================================================




>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__most_local_cited_authors.html"


>>> from techminer2 import bibliometrix
>>> r = bibliometrix.authors.most_local_cited_authors(
...     topics_length=20,
...     directory=directory,
... )
>>> r.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/bibliometrix__most_local_cited_authors.html" height="600px" width="100%" frameBorder="0"></iframe>


>>> r.table_.head()    
authors
Butler T/1           19
Anagnostopoulos I    17
OBrien L             14
Arner DW              8
Buckley RP            8
Name: local_citations, dtype: int64

>>> print(r.prompt_)


"""
from ...vantagepoint.report.chart import chart


def most_local_cited_authors(
    directory="./",
    topics_length=20,
    topic_min_occ=None,
    topic_min_citations=None,
    plot="cleveland",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Most Local Cited Authors (from Reference Lists)."""

    return chart(
        criterion="authors",
        directory=directory,
        database=database,
        metric="local_citations",
        start_year=start_year,
        end_year=end_year,
        topics_length=topics_length,
        topic_min_occ=topic_min_occ,
        topic_min_citations=topic_min_citations,
        custom_topics=None,
        title="Most Local Cited Authors (from Reference Lists)",
        plot=plot,
        **filters,
    )
