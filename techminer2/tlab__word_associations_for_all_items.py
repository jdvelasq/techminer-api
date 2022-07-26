"""
Word Associations for All Items
===============================================================================




>>> directory = "data/regtech/"

>>> from techminer2 import tlab__word_associations_for_all_items
>>> tlab__word_associations_for_all_items(
...     column='author_keywords',
...     directory=directory,
... ).head(10)
                              row                          column  OCC
0                  regtech 70:462                  regtech 70:462   70
1                  fintech 42:406                  fintech 42:406   42
2                  fintech 42:406                  regtech 70:462   42
3                  regtech 70:462                  fintech 42:406   42
4               blockchain 18:109               blockchain 18:109   18
5               blockchain 18:109                  regtech 70:462   17
6                  regtech 70:462               blockchain 18:109   17
7               blockchain 18:109                  fintech 42:406   14
8                  fintech 42:406               blockchain 18:109   14
9  artificial intelligence 13:065  artificial intelligence 13:065   13


"""
from .vantagepoint__co_occ_matrix_list import vantagepoint__co_occ_matrix_list


def tlab__word_associations_for_all_items(
    column,
    directory="./",
    database="documents",
):
    """Computes the co-occurrence matrix list."""

    return vantagepoint__co_occ_matrix_list(
        criterion=column,
        row=None,
        topics_length=None,
        min_occ_per_topic=None,
        min_citations_per_topic=None,
        directory=directory,
        database=database,
    )
