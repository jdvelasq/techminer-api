"""
Co-occurrence Matrix List
===============================================================================

>>> from techminer2 import *
>>> directory = "data/"

**Item selection by occurrence.**

>>> co_occ_matrix_list(
...    column='author_keywords',
...    row='authors',
...    min_occ=3,
...    directory=directory,
... )
                  row                          column  OCC
0      Arner DW 7:220                  regtech 70:462    6
1      Arner DW 7:220                  fintech 42:406    5
2    Buckley RP 6:217                  regtech 70:462    5
3      Arner DW 7:220     financial regulation 08:091    4
4    Buckley RP 6:217                  fintech 42:406    4
5   Zetzsche DA 4:092                  fintech 42:406    4
6   Zetzsche DA 4:092                  regtech 70:462    4
7   Barberis JN 4:146                  regtech 70:462    3
8     Brennan R 3:008                  account 04:022    3
9     Brennan R 3:008  data protection officer 03:008    3
10    Brennan R 3:008                  regtech 70:462    3
11   Buckley RP 6:217     financial regulation 08:091    3
12       Ryan P 3:008                  account 04:022    3
13       Ryan P 3:008  data protection officer 03:008    3
14       Ryan P 3:008                  regtech 70:462    3

>>> co_occ_matrix_list(
...    column='author_keywords',
...    min_occ=4,
...    directory=directory,
... )
                                         row             column  OCC
0                             regtech 70:462     regtech 70:462   70
1                             fintech 42:406     fintech 42:406   42
2                             fintech 42:406     regtech 70:462   42
3                             regtech 70:462     fintech 42:406   42
4                          blockchain 18:109  blockchain 18:109   18
..                                       ...                ...  ...
75                            regtech 70:462     suptech 04:003    4
76                           regulate 06:120     fintech 42:406    4
77  regulatory technologies (regtech) 12:047     regtech 70:462    4
78                            suptech 04:003     regtech 70:462    4
79                            suptech 04:003     suptech 04:003    4
<BLANKLINE>
[80 rows x 3 columns]


**Seleccition of top terms.**

>>> co_occ_matrix_list(
...    column='author_keywords',
...    row='authors',
...    top_n=5,
...    directory=directory,
... )
                  row                                    column  OCC
0      Arner DW 7:220                            regtech 70:462    6
1      Arner DW 7:220                            fintech 42:406    5
2    Buckley RP 6:217                            regtech 70:462    5
3    Buckley RP 6:217                            fintech 42:406    4
4   Zetzsche DA 4:092                            fintech 42:406    4
5   Zetzsche DA 4:092                            regtech 70:462    4
6   Barberis JN 4:146                            regtech 70:462    3
7     Brennan R 3:008                            regtech 70:462    3
8   Barberis JN 4:146                            fintech 42:406    2
9     Brennan R 3:008                         compliance 12:020    2
10     Arner DW 7:220                         blockchain 18:109    1
11     Arner DW 7:220  regulatory technologies (regtech) 12:047    1
12  Barberis JN 4:146  regulatory technologies (regtech) 12:047    1
13   Buckley RP 6:217                         blockchain 18:109    1
14  Zetzsche DA 4:092                         blockchain 18:109    1


>>> co_occ_matrix_list(
...    column='author_keywords',
...    top_n=5,
...    directory=directory,
... )
                               row                          column  OCC
0                   regtech 70:462                  regtech 70:462   70
1                   fintech 42:406                  fintech 42:406   42
2                   fintech 42:406                  regtech 70:462   42
3                   regtech 70:462                  fintech 42:406   42
4                blockchain 18:109               blockchain 18:109   18
5                blockchain 18:109                  regtech 70:462   17
6                   regtech 70:462               blockchain 18:109   17
7                blockchain 18:109                  fintech 42:406   14
8                   fintech 42:406               blockchain 18:109   14
9   artificial intelligence 13:065  artificial intelligence 13:065   13
10               compliance 12:020               compliance 12:020   12
11               compliance 12:020                  regtech 70:462   12
12                  regtech 70:462               compliance 12:020   12
13  artificial intelligence 13:065                  regtech 70:462   10
14                  regtech 70:462  artificial intelligence 13:065   10
15  artificial intelligence 13:065                  fintech 42:406    8
16                  fintech 42:406  artificial intelligence 13:065    8
17               blockchain 18:109               compliance 12:020    3
18               compliance 12:020               blockchain 18:109    3
19               compliance 12:020                  fintech 42:406    3
20                  fintech 42:406               compliance 12:020    3
21  artificial intelligence 13:065               blockchain 18:109    2
22               blockchain 18:109  artificial intelligence 13:065    2
23  artificial intelligence 13:065               compliance 12:020    1
24               compliance 12:020  artificial intelligence 13:065    1

"""

from ._read_records import read_records
from .items2counters import items2counters
from .load_stopwords import load_stopwords


def co_occ_matrix_list(
    column,
    row=None,
    top_n=None,
    min_occ=None,
    max_occ=None,
    directory="./",
    database="documents",
):
    """Creates a list of the cells of a co-occurrence matrix."""

    if row is None:
        row = column

    matrix_list = _create_matrix_list(column, row, directory, database)
    matrix_list = _remove_stopwords(directory, matrix_list)
    matrix_list = _remove_terms_by_occ(min_occ, max_occ, matrix_list)
    matrix_list = _add_counters_to_items(column, row, directory, database, matrix_list)
    matrix_list = _select_top_n_items(top_n, matrix_list)
    matrix_list = matrix_list.reset_index(drop=True)

    return matrix_list


def _select_top_n_items(top_n, matrix_list):
    for name in ["row", "column"]:
        terms = matrix_list[name].drop_duplicates().to_list()
        sorted_terms = sorted(
            terms, key=lambda x: x.split()[-1].split(":")[0], reverse=True
        )
        sorted_terms = sorted_terms[:top_n]
        matrix_list = matrix_list[matrix_list[name].isin(sorted_terms)]
    return matrix_list


def _add_counters_to_items(column, row, directory, database, matrix_list):
    new_row_names = items2counters(
        column=row,
        directory=directory,
        database=database,
        use_filter=True,
    )
    new_column_names = items2counters(
        column=column,
        directory=directory,
        database=database,
        use_filter=True,
    )
    matrix_list["row"] = matrix_list["row"].map(new_row_names)
    matrix_list["column"] = matrix_list["column"].map(new_column_names)
    return matrix_list


def _remove_terms_by_occ(min_occ, max_occ, matrix_list):
    if min_occ is not None:
        matrix_list = matrix_list[matrix_list.OCC >= min_occ]
    if max_occ is not None:
        matrix_list = matrix_list[matrix_list.OCC <= max_occ]
    matrix_list = matrix_list.sort_values(
        by=["OCC", "row", "column"], ascending=[False, True, True]
    )
    return matrix_list


def _remove_stopwords(directory, matrix_list):
    stopwords = load_stopwords(directory)
    matrix_list = matrix_list[~matrix_list["column"].isin(stopwords)]
    matrix_list = matrix_list[~matrix_list["row"].isin(stopwords)]
    return matrix_list


def _create_matrix_list(column, row, directory, database):

    records = read_records(directory, database=database, use_filter=True)

    matrix_list = records[[column]].copy()
    matrix_list = matrix_list.rename(columns={column: "column"})
    matrix_list = matrix_list.assign(row=records[[row]])

    for name in ["column", "row"]:
        matrix_list[name] = matrix_list[name].str.split(";")
        matrix_list = matrix_list.explode(name)
        matrix_list[name] = matrix_list[name].str.strip()

    matrix_list["OCC"] = 1
    matrix_list = matrix_list.groupby(["row", "column"], as_index=False).aggregate(
        "sum"
    )

    return matrix_list
