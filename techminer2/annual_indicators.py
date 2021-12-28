"""
Annual Indicators
===============================================================================

>>> from techminer2 import *
>>> directory = "/workspaces/techminer2/data/"
>>> annual_indicators(directory)
          num_documents  ...  cum_local_citations
pub_year                 ...                     
2016                  5  ...                   29
2017                 10  ...                   77
2018                 34  ...                  204
2019                 38  ...                  315
2020                 62  ...                  377
2021                 99  ...                  397
<BLANKLINE>
[6 rows x 8 columns]

>>> from techminer2.visualization_api.line_chart import line_chart
>>> file_name = "/workspaces/techminer2/sphinx/images/annual_scientific_production_.png"
>>> line_chart(
...     annual_indicators(directory=directory).num_documents, 
...     title="Annual Scientific Production",
... ).savefig(file_name)

.. image:: images/annual_scientific_production_.png
    :width: 700px
    :align: center

"""

from .load_filtered_documents import load_filtered_documents


def annual_indicators(directory="./"):

    indicators = load_filtered_documents(directory)
    indicators = indicators.assign(num_documents=1)
    indicators = indicators[
        [
            "pub_year",
            "num_documents",
            "local_citations",
            "global_citations",
        ]
    ].copy()
    indicators = indicators.groupby("pub_year", as_index=True).sum()
    indicators = indicators.sort_index(ascending=True, axis="index")
    indicators = indicators.assign(
        mean_global_citations=indicators.global_citations / indicators.num_documents
    )
    indicators = indicators.assign(
        mean_local_citations=indicators.local_citations / indicators.num_documents
    )
    indicators = indicators.assign(cum_num_documents=indicators.num_documents.cumsum())
    indicators = indicators.assign(
        cum_global_citations=indicators.global_citations.cumsum()
    )
    indicators = indicators.assign(
        cum_local_citations=indicators.local_citations.cumsum()
    )

    return indicators
