"""
Coverage
===============================================================================

Computes coverage of terms in a column discarding stopwords.


>>> directory = "data/regtech/"

>>> from techminer2 import tm2__coverage
>>> tm2__coverage(
...     "author_keywords",
...     directory=directory,
... ).head(10)
--INFO-- Number of documents : 94
--INFO-- Documents with NA: 9
--INFO-- Efective documents : 94
   min_occ  cum_sum_documents coverage  cum num items
0       69                 69  73.40 %              1
1       42                 69  73.40 %              2
2       18                 70  74.47 %              3
3       13                 73  77.66 %              4
4       12                 80  85.11 %              6
5        9                 81  86.17 %              7
6        8                 81  86.17 %              8
7        6                 81  86.17 %             10
8        5                 81  86.17 %             12
9        4                 82  87.23 %             22


"""

import sys

from ._load_stopwords import load_stopwords
from ._read_records import read_records


def tm2__coverage(
    column,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Coverage of terms in a column discarding stopwords."""

    stopwords = load_stopwords(directory)

    documents = read_records(
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )
    documents = documents.reset_index()
    documents = documents[[column, "article"]]

    n_documents = len(documents)
    sys.stdout.write(f"--INFO-- Number of documents : {n_documents}\n")
    sys.stdout.write(
        f"--INFO-- Documents with NA: {n_documents - len(documents.dropna())}\n"
    )

    documents = documents.dropna()
    sys.stdout.write(f"--INFO-- Efective documents : {n_documents}\n")

    documents = documents.assign(num_documents=1)
    documents[column] = documents[column].str.split("; ")
    documents = documents.explode(column)

    documents = documents[~documents[column].isin(stopwords)]

    documents = documents.groupby(by=[column]).agg(
        {"num_documents": "count", "article": list}
    )
    documents = documents.sort_values(by=["num_documents"], ascending=False)

    documents = documents.reset_index()

    documents = documents.groupby(by="num_documents", as_index=False).agg(
        {"article": list, column: list}
    )

    documents = documents.sort_values(by=["num_documents"], ascending=False)
    documents["article"] = documents.article.map(
        lambda x: [term for sublist in x for term in sublist]
    )

    documents = documents.assign(cum_sum_documents=documents.article.cumsum())
    documents = documents.assign(cum_sum_documents=documents.cum_sum_documents.map(set))
    documents = documents.assign(cum_sum_documents=documents.cum_sum_documents.map(len))

    documents = documents.assign(
        coverage=documents.cum_sum_documents.map(
            lambda x: "{:5.2f} %".format(100 * x / n_documents)
        )
    )

    documents = documents.assign(cum_sum_items=documents[column].cumsum())
    documents = documents.assign(cum_sum_items=documents.cum_sum_items.map(set))
    documents = documents.assign(cum_sum_items=documents.cum_sum_items.map(len))

    documents.drop("article", axis=1, inplace=True)
    documents.drop(column, axis=1, inplace=True)

    documents = documents.rename(
        columns={
            "num_documents": "min_occ",
            "cum_sum": "cum num documents",
            "cum_sum_items": "cum num items",
        }
    )
    documents = documents.reset_index(drop=True)

    return documents
