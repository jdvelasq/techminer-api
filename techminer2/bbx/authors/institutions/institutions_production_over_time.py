"""
Institutions' Production over Time
===============================================================================


>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/institutions_production_over_time.html"

>>> from techminer2.bbx.authors.institutions import institutions_production_over_time
>>> institutions_production_over_time(
...    top_n=10, 
...    directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/institutions_production_over_time.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from ....production_over_time_chart import production_over_time_chart


def institutions_production_over_time(
    top_n=10,
    directory="./",
):

    return production_over_time_chart(
        column="institutions",
        top_n=top_n,
        directory=directory,
        title="Institutions' production over time",
    )
