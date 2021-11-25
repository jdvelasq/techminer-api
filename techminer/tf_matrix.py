"""
TF matrix
===============================================================================


>>> from techminer import *
>>> directory = "/workspaces/techminer-api/tests/data/"
>>> tf_matrix(directory, 'authors', min_occ=6).head()
authors   Rabbani MR Arner DW Buckley RP  ... Zetzsche D Surjandy Schwienbacher A
#d                10       9          7   ...         6        6               6 
#c               72       154        151  ...        67       19              56 
record_no                                 ...                                    
2016-0023          0        1          0  ...          0        0               0
2017-0005          0        0          0  ...          0        0               0
2017-0008          0        1          1  ...          0        0               0
2017-0021          0        0          0  ...          0        0               0
2017-0064          0        0          0  ...          0        0               0
<BLANKLINE>
[5 rows x 17 columns]

"""
import numpy as np
import pandas as pd

from .utils import *

# pylint: disable=too-many-arguments


def tf_matrix(
    directory,
    column,
    min_occ=None,
    max_occ=None,
    scheme=None,
    sep="; ",
):

    documents = load_filtered_documents(directory)

    documents = documents.reset_index()
    documents = documents[[column, "record_no"]].copy()
    documents["value"] = 1
    documents[column] = documents[column].str.split(sep)
    documents = documents.explode(column)
    # documents = explode(documents, column, sep)

    grouped_records = documents.groupby(["record_no", column], as_index=False).agg(
        {"value": np.sum}
    )

    result = pd.pivot(
        index="record_no",
        data=grouped_records,
        columns=column,
    )
    result = result.fillna(0)

    # ----< Counts term occurrence >-------------------------------------------
    result.columns = [b for _, b in result.columns]
    terms = result.sum(axis=0)
    terms = terms.sort_values(ascending=False)
    if min_occ is not None:
        terms = terms[terms >= min_occ]
    if max_occ is not None:
        terms = terms[terms <= max_occ]
    terms = terms.drop(labels=load_stopwords(directory), errors="ignore")
    result = result.loc[:, terms.index]
    result = index_terms2counters(directory, result, "columns", column, sep)

    # ---< Remove rows with only zeros detected -------------------------------
    result = result.loc[(result != 0).any(axis=1)]

    # ----< Applies scheme >---------------------------------------------------
    if scheme is None or scheme == "raw":
        result = result.astype(int)
    elif scheme == "binary":
        result = result.applymap(lambda w: 1 if w > 0 else 0)
    elif scheme == "log":
        result = result.applymap(lambda x: np.log(x) if x > 0 else 0)
    elif scheme == "sqrt":
        result = result.applymap(lambda x: np.sqrt(x) if x > 0 else 0)
    else:
        raise ValueError("scheme must be 'raw', 'binary', 'log' or 'sqrt'")

    result = result.sort_index(axis=0, ascending=True)

    return result
