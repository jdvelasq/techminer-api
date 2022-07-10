"""
Line Plot
===============================================================================

>>> from techminer2 import *
>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/line_plot.html"

>>> indicators = list_view(
...    column='author_keywords',
...    min_occ=3,
...    directory=directory,
... )

>>> line_plot(indicators).write_html(file_name)

.. raw:: html

    <iframe src="_static/line_plot.html" height="600px" width="100%" frameBorder="0"></iframe>

"""

from .format_dataset_to_plot_with_plotly import format_dataset_to_plot_with_plotly
from .line_px import line_px


def line_plot(
    dataframe,
    metric="OCC",
    title=None,
):
    """Makes a line plot from a dataframe."""

    metric, column, dataframe = format_dataset_to_plot_with_plotly(dataframe, metric)

    return line_px(
        dataframe=dataframe,
        x_label=column,
        y_label=metric,
        title=title,
    )
