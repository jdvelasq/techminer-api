# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=import-outside-toplevel
"""
Coverage
===============================================================================

>>> from techminer2.analyze import Coverage
>>> Coverage(
...     #
...     # DATABASE_PARAMS
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).compute(
...     #
...     # PARAMS:
...     field="author_keywords",
... )
--INFO-- Number of documents : 50
--INFO--   Documents with NA : 12
--INFO--  Efective documents : 38
   min_occ  cum_sum_documents  coverage  cum num items
0       31                 31   81.58 %              1
1        7                 33   86.84 %              2
2        4                 35   92.11 %              4
3        3                 35   92.11 %             15
4        2                 36   94.74 %             27
5        1                 38  100.00 %            137



"""
from .._read_records import ReadRecordsMixin
from .._stopwords import StopwordsMixin


class Coverage(
    ReadRecordsMixin,
    StopwordsMixin,
):
    def __init__(
        self,
        #
        # DATABASE PARAMS
        root_dir: str = "./",
        database: str = "main",
        year_filter: tuple = (None, None),
        cited_by_filter: tuple = (None, None),
        **filters,
    ):
        # initialize mixins
        StopwordsMixin.__init__(
            self,
            #
            # PROJECT DIR
            root_dir=root_dir,
        )
        ReadRecordsMixin.__init__(
            self,
            #
            # DATABASE PARAMS
            root_dir=root_dir,
            database=database,
            year_filter=year_filter,
            cited_by_filter=cited_by_filter,
            **filters,
        )

    def compute(self, field):
        stopwords = self.load_stopwords()

        documents = self.read_records()

        documents = documents.reset_index()
        documents = documents[[field, "article"]]

        n_documents = len(documents)
        print(f"--INFO-- Number of documents : {n_documents}")
        print(
            "--INFO--   Documents with NA : " f"{n_documents - len(documents.dropna())}"
        )
        documents = documents.dropna()
        n_documents = len(documents)
        print(f"--INFO--  Efective documents : {n_documents}")

        documents = documents.assign(num_documents=1)
        documents[field] = documents[field].str.split("; ")
        documents = documents.explode(field)

        documents = documents[~documents[field].isin(stopwords)]

        documents = documents.groupby(by=[field]).agg(
            {"num_documents": "count", "article": list}
        )
        documents = documents.sort_values(by=["num_documents"], ascending=False)

        documents = documents.reset_index()

        documents = documents.groupby(by="num_documents", as_index=False).agg(
            {"article": list, field: list}
        )

        documents = documents.sort_values(by=["num_documents"], ascending=False)
        documents["article"] = documents.article.map(
            lambda x: [term for sublist in x for term in sublist]
        )

        documents = documents.assign(cum_sum_documents=documents.article.cumsum())
        documents = documents.assign(
            cum_sum_documents=documents.cum_sum_documents.map(set)
        )
        documents = documents.assign(
            cum_sum_documents=documents.cum_sum_documents.map(len)
        )

        documents = documents.assign(
            coverage=documents.cum_sum_documents.map(
                lambda x: f"{100 * x / n_documents:5.2f} %"
            )
        )

        documents = documents.assign(cum_sum_items=documents[field].cumsum())
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.map(set))
        documents = documents.assign(cum_sum_items=documents.cum_sum_items.map(len))

        documents.drop("article", axis=1, inplace=True)
        documents.drop(field, axis=1, inplace=True)
        documents = documents.reset_index(drop=True)

        documents = documents.rename(
            columns={
                "num_documents": "min_occ",
                "cum_sum": "cum num documents",
                "cum_sum_items": "cum num items",
            }
        )

        return documents
