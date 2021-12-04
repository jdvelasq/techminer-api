"""
Source local impact
===============================================================================



>>> from techminer import *
>>> directory = "/workspaces/techminer-api/data/"
>>> file_name = "/workspaces/techminer-api/sphinx/images/source_impact.png"
>>> source_local_impact(20, directory=directory).savefig(file_name)

.. image:: images/source_impact.png
    :width: 650px
    :align: center


>>> source_local_impact(20, directory=directory, plot=False).head(5)
                         num_documents  ...  avg_global_citations
FINANCIAL INNOV                     11  ...                 12.00
SUSTAINABILITY                      15  ...                  6.47
ENVIRON PLANN A                      4  ...                  7.50
FRONTIER ARTIF INTELL                5  ...                  4.60
J ASIAN FINANC ECON BUS              3  ...                  5.33
<BLANKLINE>
[5 rows x 9 columns]

"""


from .cleveland_dot_chart import cleveland_dot_chart
from .impact_indicators import impact_indicators


def source_local_impact(
    top_n=20,
    metric="h_index",
    color="k",
    figsize=(8, 6),
    directory="./",
    plot=True,
):
    indicators = impact_indicators(directory=directory, column="iso_source_name")
    indicators = indicators.sort_values(by=metric, ascending=False)

    if plot is False:
        return indicators

    indicators = indicators[metric].head(top_n)

    return cleveland_dot_chart(
        indicators,
        figsize=figsize,
        color=color,
        title="Source local impact",
        xlabel=metric.replace("_", " ").title(),
        ylabel="Source",
    )
