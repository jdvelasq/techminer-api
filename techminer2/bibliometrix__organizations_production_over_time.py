"""
Organizations' Production over Time
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__organizations_production_over_time.html"

>>> from techminer2 import bibliometrix__organizations_production_over_time
>>> pot = bibliometrix__organizations_production_over_time(
...    topics_length=10, 
...    directory=directory,
... )

>>> pot.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/bibliometrix__organizations_production_over_time.html" height="600px" width="100%" frameBorder="0"></iframe>

>>> pot.documents_per_organization_.head()
                               organizations  ...                           doi
0                 University of Johannesburg  ...    10.1057/S41261-020-00134-0
1  ---Indian Institute of Management Lucknow  ...    10.1057/S41261-020-00127-Z
2                           Ahlia University  ...  10.1007/978-981-15-3383-9_32
3                Conventional Wholesale Bank  ...  10.1007/978-981-15-3383-9_32
4                  Mendel University in Brno  ...   10.1007/978-3-030-62796-6_9
<BLANKLINE>
[5 rows x 7 columns]

>>> pot.production_per_year_.head()
                                                         OCC  ...  local_citations_per_year
organizations                                      year       ...                          
---3PB                                             2022    1  ...                     0.000
---ABES Engineering College                        2021    1  ...                     0.000
---AML Forensic library KPMG Luxembourg Societe... 2020    1  ...                     0.333
---Audencia PRES LUNAM                             2018    1  ...                     0.600
---BITS Pilani                                     2020    1  ...                     0.000
<BLANKLINE>
[5 rows x 7 columns]


"""
from dataclasses import dataclass

from ._indicators.indicators_by_topic_per_year import indicators_by_topic_per_year
from .bibliometrix__documents_per import bibliometrix__documents_per
from .bibliometrix__production_over_time import bibliometrix__production_over_time


@dataclass(init=False)
class _Results:
    plot_ = None
    production_per_year_ = None
    documents_per_organization_ = None


def bibliometrix__organizations_production_over_time(
    topics_length=10,
    min_occ_per_topic=None,
    min_citations_per_topic=0,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Institution production over time."""

    results = _Results()

    results.plot_ = bibliometrix__production_over_time(
        criterion="organizations",
        topics_length=topics_length,
        min_occ_per_topic=min_occ_per_topic,
        min_citations_per_topic=min_citations_per_topic,
        directory=directory,
        title="Organizations' production over time",
        metric="OCC",
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    results.documents_per_organization_ = bibliometrix__documents_per(
        criterion="organizations",
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    results.production_per_year_ = indicators_by_topic_per_year(
        criterion="organizations",
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    return results
