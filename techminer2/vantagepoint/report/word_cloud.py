"""
WordCloud
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/images/vantagepoint__word_cloud.png"


>>> from techminer2 import vantagepoint
>>> vantagepoint.report.word_cloud(
...     criterion='author_keywords',
...     title="Author Keywords",
...     topics_length=50,
...     directory=directory,
... ).savefig(file_name)

.. image:: ../../images/vantagepoint__word_cloud.png
    :width: 900px
    :align: center

"""
from ..._plots.word_cloud_for_indicators import word_cloud_for_indicators
from ...core.indicators.tm2__indicators_by_topic import tm2__indicators_by_topic


def word_cloud(
    criterion,
    directory="./",
    database="documents",
    metric="OCC",
    start_year=None,
    end_year=None,
    topics_length=20,
    topic_min_occ=None,
    topic_min_citations=None,
    custom_topics=None,
    title=None,
    figsize=(12, 12),
    **filters,
):
    """Plots a word cloud from a dataframe."""

    indicators = tm2__indicators_by_topic(
        criterion=criterion,
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    if custom_topics is None:
        custom_topics = indicators.copy()
        if topic_min_occ is not None:
            custom_topics = custom_topics[custom_topics["OCC"] >= topic_min_occ]
        if topic_min_citations is not None:
            custom_topics = custom_topics[
                custom_topics["global_citations"] >= topic_min_citations
            ]
        custom_topics = custom_topics.index.copy()
        custom_topics = custom_topics[:topics_length]
    else:
        custom_topics = [
            topic for topic in custom_topics if topic in indicators.index.tolist()
        ]

    indicators = indicators.loc[custom_topics, :]

    return word_cloud_for_indicators(
        dataframe=indicators,
        metric=metric,
        title=title,
        figsize=figsize,
    )
