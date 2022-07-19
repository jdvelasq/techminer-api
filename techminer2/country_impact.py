"""
Country Impact
===============================================================================




>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/country_impact.html"


>>> from techminer2 import country_impact
>>> country_impact(
...     impact_measure='h_index', 
...     top_n=20, 
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/country_impact.html" height="600px" width="100%" frameBorder="0"></iframe>


"""
from .impact import impact


def country_impact(
    impact_measure="h_index",
    top_n=20,
    directory="./",
):
    """Plots the selected impact measure by country."""
    return impact(
        column="countries",
        impact_measure=impact_measure,
        top_n=top_n,
        directory=directory,
        title="Country Local Impact by " + impact_measure.replace("_", " ").title(),
    )
