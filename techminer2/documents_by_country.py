"""
Documents by country (!)
===============================================================================

>>> from techminer2.scopus import *
>>> directory = "data/"
>>> file_name = "sphinx/images/documents_by_country.png"

>>> documents_by_country(
...     directory
... ).write_image(file_name)

.. image:: images/documents_by_country.png
    :width: 700px
    :align: center

"""
from .bar_chart import bar_chart


def documents_by_country(directory):
    return bar_chart(
        column="countries",
        min_occ=None,
        max_occ=None,
        top_n=10,
        directory=directory,
        metric="num_documents",
    )
