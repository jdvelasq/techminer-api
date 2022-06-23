"""
Source local impact
===============================================================================

See :doc:`impact indicators <impact_indicators>` to obtain a `pandas.Dataframe` 
with the data. 

>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/source_local_impact.html"

>>> source_local_impact(
...     impact_measure='h_index', 
...     top_n=20, 
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/source_local_impact.html" height="600px" width="100%" frameBorder="0"></iframe>


"""
from .impact_indicators_plot import impact_indicators_plot


def source_local_impact(
    impact_measure="h_index",
    top_n=20,
    directory="./",
):
    return impact_indicators_plot(
        column="iso_source_name",
        impact_measure=impact_measure,
        top_n=top_n,
        directory=directory,
        title="Source Local Impact by " + impact_measure.replace("_", " ").title(),
    )
