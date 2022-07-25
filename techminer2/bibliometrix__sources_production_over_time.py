"""
Sources' Production over Time
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__sources_production_over_time.html"

>>> from techminer2 import bibliometrix__sources_production_over_time
>>> bibliometrix__sources_production_over_time(
...    topics_length=10, 
...    directory=directory,
... ).plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../_static/bibliometrix__sources_production_over_time.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from dataclasses import dataclass

from ._indicators.indicators_by_topic_per_year import indicators_by_topic_per_year
from .bibliometrix__documents_per import bibliometrix__documents_per
from .bibliometrix__production_over_time import bibliometrix__production_over_time


@dataclass(init=False)
class _Results:
    plot_ = None
    production_per_year_ = None
    documents_per_source_ = None


def bibliometrix__sources_production_over_time(
    topics_length=10,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Sources production over time."""

    results = _Results()

    results.plot_ = bibliometrix__production_over_time(
        criterion="source_abbr",
        topics_length=topics_length,
        directory=directory,
        title="Sources' production over time",
        metric="OCC",
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    results.documents_per_source_ = bibliometrix__documents_per(
        criterion="source_abbr",
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    results.production_per_year_ = indicators_by_topic_per_year(
        criterion="source_abbr",
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    return results
