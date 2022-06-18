"""
Most Frequent Words
===============================================================================

>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/images/most_frequent_words.png"
>>> most_frequent_words(
...     'author_keywords', 
...     top_n=20,
...     directory=directory,
... ).write_image(file_name)

.. image:: images/most_frequent_words.png
    :width: 700px
    :align: center



"""
from .cleveland_chart import cleveland_chart

most_frequent_words = cleveland_chart
