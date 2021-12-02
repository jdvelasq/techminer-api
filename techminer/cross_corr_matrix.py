"""
Cross-correlation matrix
===============================================================================


>>> from techminer import *
>>> directory = "/workspaces/techminer-api/data/"
>>> cross_corr_matrix('authors', min_occ=3, by='countries', min_occ_by=6, directory=directory)
authors            Wojcik D Rabbani MR  Hornuf L
#d                        5          3         3
#c                      19         39        110
authors    #d #c                                
Wojcik D   5  19   1.000000  -0.525226 -0.332182
Rabbani MR 3  39  -0.525226   1.000000 -0.316228
Hornuf L   3  110 -0.332182  -0.316228  1.000000


"""
import numpy as np
import pandas as pd

from .co_occurrence_matrix import co_occurrence_matrix
from .tf_matrix import tf_matrix
from .utils import index_terms2counters, load_filtered_documents

# pyltin: disable=c0103
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name


def cross_corr_matrix(
    column,
    by=None,
    method="pearson",
    min_occ=1,
    max_occ=None,
    min_occ_by=1,
    max_occ_by=None,
    scheme=None,
    sep="; ",
    directory="./",
):

    co_occ_matrix = co_occurrence_matrix(
        directory=directory,
        column=column,
        by=by,
        min_occ=min_occ,
        max_occ=max_occ,
        min_occ_by=min_occ_by,
        max_occ_by=max_occ_by,
        scheme=scheme,
        sep=sep,
    )

    matrix = co_occ_matrix.corr(method=method)

    return matrix
