"""
Apply a thesaurus to a column
===============================================================================


>>> from techminer2 import *
>>> directory = "data/"

>>> create_thesaurus(
...     column="author_keywords",
...     output_file="test_keywords.txt",
...     directory=directory,
... )
--INFO-- Creating a thesaurus file from `author_keywords` column in all databases
--INFO-- The thesaurus file data/processed/test_keywords.txt was created


>>> apply_thesaurus(
...     thesaurus_file="test_keywords.txt",
...     input_column="author_keywords",
...     output_column="author_keywords_thesaurus",
...     strict=False,
...     directory=directory,
... )
--INFO-- The thesaurus was applied to all databases


"""
import glob
import os
import sys

import pandas as pd

from .map_ import map_
from .thesaurus import read_textfile


def apply_thesaurus(
    thesaurus_file,
    input_column,
    output_column,
    strict,
    directory="./",
):
    """Apply a thesaurus to a column of a dataframe."""

    def apply_strict(text):
        return thesaurus.apply_as_dict(text, strict=True)

    def apply_unstrict(text):
        return thesaurus.apply_as_dict(text, strict=False)

    thesaurus_file = os.path.join(directory, "processed", thesaurus_file)
    thesaurus = read_textfile(thesaurus_file)
    thesaurus = thesaurus.compile_as_dict()

    files = list(glob.glob(os.path.join(directory, "processed/_*.csv")))
    for file in files:
        data = pd.read_csv(file, encoding="utf-8")
        if strict:
            data[output_column] = map_(data, input_column, apply_strict)
        else:
            data[output_column] = map_(data, input_column, apply_unstrict)
        data.to_csv(file, sep=",", encoding="utf-8", index=False)

    sys.stdout.write("--INFO-- The thesaurus was applied to all databases\n")
