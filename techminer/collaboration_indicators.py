"""
Collaboration indicators
===============================================================================

>>> from techminer import *
>>> directory = "/workspaces/techminer-api/tests/data/"
>>> collaboration_indicators(directory, "countries").head()
                num_documents  ...  mp_ratio
countries                      ...          
china                     240  ...      0.47
united states             239  ...      0.44
united kingdom            182  ...      0.54
indonesia                 151  ...      0.07
india                      88  ...      0.30
<BLANKLINE>
[5 rows x 4 columns]

"""


import numpy as np
import pandas as pd

from .utils import explode, load_filtered_documents


def collaboration_indicators(
    directory,
    column,
    sep="; ",
):
    documents = load_filtered_documents(directory)
    documents = documents.assign(num_documents=1)
    documents["single_publication"] = documents[column].map(
        lambda x: 1 if isinstance(x, str) and len(x.split(";")) == 1 else 0
    )
    documents["multiple_publication"] = documents[column].map(
        lambda x: 1 if isinstance(x, str) and len(x.split(";")) > 1 else 0
    )

    exploded = explode(
        documents[
            [
                column,
                "num_documents",
                "single_publication",
                "multiple_publication",
                "record_no",
            ]
        ],
        column=column,
        sep=sep,
    )
    indicators = exploded.groupby(column, as_index=False).agg(
        {
            "num_documents": np.sum,
            "single_publication": np.sum,
            "multiple_publication": np.sum,
        }
    )
    indicators["mp_ratio"] = [
        round(mp / nd, 2)
        for nd, mp in zip(indicators.num_documents, indicators.multiple_publication)
    ]

    indicators = indicators.set_index(column)
    indicators = indicators.sort_values(by=["num_documents"], ascending=False)

    return indicators
