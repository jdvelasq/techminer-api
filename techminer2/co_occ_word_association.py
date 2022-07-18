"""
Word Association
===============================================================================

>>> from techminer2 import *
>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/co_occ_word_association.html"

>>> co_occ_word_association(
...     term="regtech",
...     min_occ=4,
...     column='author_keywords',
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/co_occ_word_association.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .vp.analyze.matrix.co_occ_matrix_list import co_occ_matrix_list
from .tm2.plots.bar_plot import bar_plot
from .tm2.plots.cleveland_plot import cleveland_plot
from .tm2.plots.column_plot import column_plot
from .tm2.plots.line_plot import line_plot
from .tm2.plots.pie_plot import pie_plot


def co_occ_word_association(
    term,
    column,
    top_n=None,
    min_occ=None,
    max_occ=None,
    directory="./",
    database="documents",
    plot="bar",
):
    """Word Association"""

    matrix_list = co_occ_matrix_list(
        column=column,
        row=None,
        top_n=None,
        min_occ=None,
        max_occ=None,
        directory=directory,
        database=database,
    )

    matrix_list = matrix_list[
        matrix_list["row"].map(lambda x: " ".join(x.split()[:-1]) == term)
    ]

    matrix_list = matrix_list[matrix_list["row"] != matrix_list["column"]]

    matrix_list = matrix_list[["column", "OCC"]]

    if min_occ is not None:
        matrix_list = matrix_list[matrix_list["OCC"] >= min_occ]

    if max_occ is not None:
        matrix_list = matrix_list[matrix_list["OCC"] <= max_occ]

    if top_n is not None:
        matrix_list = matrix_list.head(top_n)

    matrix_list = matrix_list.set_index("column")

    plot_function = {
        "bar": bar_plot,
        "column": column_plot,
        "line": line_plot,
        "pie": pie_plot,
        "cleveland": cleveland_plot,
    }[plot]

    fig = plot_function(
        dataframe=matrix_list,
        metric="OCC",
        title=None,
    )
    fig.update_layout(
        yaxis_title=None,
        margin=dict(l=1, r=1, t=1, b=1),
    )

    return fig
