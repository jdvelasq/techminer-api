"""
Organization Impact (GPT)
===============================================================================



>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/bibliometrix__organization_impact.html"

>>> from techminer2 import bibliometrix
>>> r = bibliometrix.organizations.organization_impact(
...     impact_measure='h_index',
...     topics_length=20,
...     directory=directory,
... )
>>> r.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/bibliometrix__organization_impact.html" height="600px" width="100%" frameBorder="0"></iframe>


>>> print(r.table_.head().to_markdown())
| organizations           |   OCC |   Global Citations |   First Pb Year |   Age |   H-Index |   G-Index |   M-Index |   Global Citations Per Year |   Avg Global Citations |
|:------------------------|------:|-------------------:|----------------:|------:|----------:|----------:|----------:|----------------------------:|-----------------------:|
| University of Hong Kong |     3 |                185 |            2017 |     7 |         3 |         3 |      0.43 |                       26.43 |                  61.67 |
| ---FinTech HK           |     2 |                161 |            2017 |     7 |         2 |         2 |      0.29 |                       23    |                  80.5  |
| University College Cork |     3 |                 41 |            2018 |     6 |         2 |         2 |      0.33 |                        6.83 |                  13.67 |
| Ahlia University        |     3 |                 19 |            2020 |     4 |         2 |         2 |      0.5  |                        4.75 |                   6.33 |
| Coventry University     |     2 |                 17 |            2020 |     4 |         2 |         1 |      0.5  |                        4.25 |                   8.5  |

>>> print(r.prompt_)
The table below provides data on top 20 organizations with the highest H-Index. 'OCC' represents the number of documents published by the organization in the dataset. Use the information in the table to draw conclusions about the impact and productivity of the organization. In your analysis, be sure to describe in a clear and concise way, any findings or any patterns you observe, and identify any outliers or anomalies in the data. Limit your description to one paragraph with no more than 250 words.
<BLANKLINE>
| organizations                                                   |   OCC |   Global Citations |   First Pb Year |   Age |   H-Index |   G-Index |   M-Index |   Global Citations Per Year |   Avg Global Citations |
|:----------------------------------------------------------------|------:|-------------------:|----------------:|------:|----------:|----------:|----------:|----------------------------:|-----------------------:|
| University of Hong Kong                                         |     3 |                185 |            2017 |     7 |         3 |         3 |      0.43 |                       26.43 |                  61.67 |
| ---FinTech HK                                                   |     2 |                161 |            2017 |     7 |         2 |         2 |      0.29 |                       23    |                  80.5  |
| University College Cork                                         |     3 |                 41 |            2018 |     6 |         2 |         2 |      0.33 |                        6.83 |                  13.67 |
| Ahlia University                                                |     3 |                 19 |            2020 |     4 |         2 |         2 |      0.5  |                        4.75 |                   6.33 |
| Coventry University                                             |     2 |                 17 |            2020 |     4 |         2 |         1 |      0.5  |                        4.25 |                   8.5  |
| University of Westminster                                       |     2 |                 17 |            2020 |     4 |         2 |         1 |      0.5  |                        4.25 |                   8.5  |
| Dublin City University                                          |     2 |                 14 |            2020 |     4 |         2 |         1 |      0.5  |                        3.5  |                   7    |
| ---Kingston Business School                                     |     1 |                153 |            2018 |     6 |         1 |         1 |      0.17 |                       25.5  |                 153    |
| ---Centre for Law                                               |     1 |                150 |            2017 |     7 |         1 |         1 |      0.14 |                       21.43 |                 150    |
| Duke University School of Law                                   |     1 |                 30 |            2016 |     8 |         1 |         1 |      0.12 |                        3.75 |                  30    |
| ---UNSW Sydney                                                  |     1 |                 24 |            2020 |     4 |         1 |         1 |      0.25 |                        6    |                  24    |
| Heinrich Heine University                                       |     1 |                 24 |            2020 |     4 |         1 |         1 |      0.25 |                        6    |                  24    |
| University of Luxembourg                                        |     1 |                 24 |            2020 |     4 |         1 |         1 |      0.25 |                        6    |                  24    |
| University of Zurich                                            |     1 |                 24 |            2020 |     4 |         1 |         1 |      0.25 |                        6    |                  24    |
| ---KS Strategic                                                 |     1 |                 21 |            2018 |     6 |         1 |         1 |      0.17 |                        3.5  |                  21    |
| ---Panepistemio Aigaiou                                         |     1 |                 21 |            2018 |     6 |         1 |         1 |      0.17 |                        3.5  |                  21    |
| ---School of Engineering                                        |     1 |                 21 |            2018 |     6 |         1 |         1 |      0.17 |                        3.5  |                  21    |
| European Central Bank                                           |     1 |                 21 |            2018 |     6 |         1 |         1 |      0.17 |                        3.5  |                  21    |
| Harvard University Weatherhead Center for International Affairs |     1 |                 21 |            2018 |     6 |         1 |         1 |      0.17 |                        3.5  |                  21    |
| Hebei University of Technology                                  |     1 |                 13 |            2022 |     2 |         1 |         1 |      0.5  |                        6.5  |                  13    |
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>


"""
from ..criterion_impact import criterion_impact


def organization_impact(
    impact_measure="h_index",
    topics_length=20,
    topic_min_occ=None,
    topic_max_occ=None,
    topic_min_citations=None,
    topic_max_citations=None,
    custom_topics=None,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Plots the selected impact measure by organizations."""

    obj = criterion_impact(
        criterion="organizations",
        metric=impact_measure,
        topics_length=topics_length,
        topic_min_occ=topic_min_occ,
        topic_max_occ=topic_max_occ,
        topic_min_citations=topic_min_citations,
        topic_max_citations=topic_max_citations,
        custom_topics=custom_topics,
        directory=directory,
        title="Organization Local Impact by "
        + impact_measure.replace("_", " ").title(),
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    obj.prompt_ = _create_prompt(obj.table_, impact_measure)

    return obj


def _create_prompt(table, impact_measure):
    return f"""\
The table \
below provides data on top {table.shape[0]} organizations with the highest \
{impact_measure.replace("_", "-").title()}. 'OCC' represents the number of \
documents published by the organization in the dataset. Use the information in the \
table to draw conclusions about the impact and productivity of the organization. \
In your analysis, be sure to describe in a clear and concise way, any \
findings or any patterns you observe, and identify any outliers or anomalies in \
the data. Limit your description to one paragraph with no more than 250 words.

{table.to_markdown()}


"""
