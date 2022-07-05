"""
World map
===============================================================================


>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/world_map.html"

>>> world_map(
...     directory=directory,
...     metric="OCC",
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/world_map.html" height="410px" width="100%" frameBorder="0"></iframe>

"""
from .column_indicators import column_indicators
from .world_map_plot import world_map_plot


def world_map(
    directory="./",
    metric="OCC",
    title=None,
    database="documents",
    colormap="Blues",
):
    """Makes a world map from a dataframe."""

    indicators = column_indicators(
        column="countries", directory=directory, database=database
    )
    indicators = indicators.sort_values(metric, ascending=False)

    return world_map_plot(
        dataframe=indicators,
        metric=metric,
        title=title,
        colormap=colormap,
    )
