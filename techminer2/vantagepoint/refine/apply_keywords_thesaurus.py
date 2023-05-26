"""
Apply Keywords Thesaurus
===============================================================================

Cleans the keywords columns using the `keywords.txt` file.


>>> root_dir = "data/regtech/"

>>> from techminer2 import vantagepoint
>>> vantagepoint.refine.apply_keywords_thesaurus(root_dir)
--INFO-- Applying `keywords.txt` thesaurus to author/index keywords and \
abstract/title words

"""
# pylint: disable=no-member
# pylint: disable=invalid-name

import glob
import os
import os.path
import sys

import pandas as pd

from ..._thesaurus import read_textfile


def apply_keywords_thesaurus(root_dir="./"):
    """Clean all words columns in the records using a thesaurus \
    (keywords.txt)."""

    sys.stdout.write(
        "--INFO-- Applying `keywords.txt` thesaurus to author/index keywords "
        "and abstract/title words\n"
    )

    thesaurus_file = os.path.join(root_dir, "processed", "keywords.txt")
    if os.path.isfile(thesaurus_file):
        thesaurus = read_textfile(thesaurus_file)
        thesaurus = thesaurus.compile_as_dict()
    else:
        raise FileNotFoundError(f"The file {thesaurus_file} does not exist.")
    #

    files = list(glob.glob(os.path.join(root_dir, "processed/_*.csv")))
    for file in files:
        data = pd.read_csv(file, encoding="utf-8")
        #
        for raw_column, column in [
            ("raw_author_keywords", "author_keywords"),
            ("raw_index_keywords", "index_keywords"),
            ("raw_keywords", "keywords"),
            ("raw_title_words", "title_words"),
            ("raw_abstract_words", "abstract_words"),
            ("raw_words", "words"),
        ]:
            if raw_column in data.columns:
                data[column] = data[raw_column].str.split(";")
                data[column] = data[column].map(
                    lambda x: [thesaurus.apply_as_dict(y.strip()) for y in x]
                    if isinstance(x, list)
                    else x
                )
                data[column] = data[column].map(
                    lambda x: sorted(set(x)) if isinstance(x, list) else x
                )
                data[column] = data[column].str.join("; ")
        #
        data.to_csv(file, sep=",", encoding="utf-8", index=False)
