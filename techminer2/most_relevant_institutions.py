"""
Most Relevant Institutions
===============================================================================

>>> from techminer2 import *
>>> directory = "/workspaces/techminer2/data/"
>>> file_name = "/workspaces/techminer2/sphinx/images/most_relevant_institutions.png"
>>> most_relevant_institutions(directory=directory).savefig(file_name)

.. image:: images/most_relevant_institutions.png
    :width: 700px
    :align: center


>>> most_relevant_institutions(directory=directory, plot=False).head()
                                     num_documents  ...  local_citations
institutions                                        ...                 
Bina Nusantara University IDN                    6  ...                7
Singapore Management University SGP              5  ...               35
University of Sydney AUS                         5  ...               25
University of Latvia LVA                         4  ...                4
University of Pavia ITA                          4  ...                1
<BLANKLINE>
[5 rows x 3 columns]



"""
from .column_cleveland_dot_chart import column_cleveland_dot_chart


def most_relevant_institutions(
    top_n=20,
    color="k",
    figsize=(6, 6),
    directory="./",
    plot=True,
):
    return column_cleveland_dot_chart(
        column="institutions",
        top_n=top_n,
        color=color,
        figsize=figsize,
        directory=directory,
        plot=plot,
    )
