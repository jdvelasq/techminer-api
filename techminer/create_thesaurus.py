"""
Thesaurus --- create
===============================================================================

"""
import os
from os.path import isfile

import pandas as pd

from .utils import *
from .utils.thesaurus import Thesaurus, load_file_as_dict, text_clustering


def create_thesaurus(
    directory,
    thesaurus_file,
    column,
    sep,
):

    documents = load_filtered_documents(directory)
    thesaurus_file = os.path.join(directory, thesaurus_file)

    if column not in documents.columns:
        raise ValueError("Column '{}' not in documents".format(column))

    logging.info("Creating thesaurus ...")
    words_list = documents[column]
    words_list = words_list.dropna()

    if sep is not None:
        words_list = words_list.str.split(sep)
        words_list = words_list.explode()

    if isfile(thesaurus_file):
        #
        # Loads existent thesaurus
        #
        dict_ = load_file_as_dict(thesaurus_file)
        clustered_words = [word for key in dict_.keys() for word in dict_[key]]
        words_list = [word for word in words_list if word not in clustered_words]

        if len(words_list) > 0:

            th_ = text_clustering(pd.Series(words_list))

            th_ = Thesaurus(
                x={**th_._thesaurus, **dict_},
                ignore_case=True,
                full_match=False,
                use_re=False,
            )
            th_.to_textfile(thesaurus_file)
    else:
        #
        # Creates a new thesaurus
        #
        text_clustering(pd.Series(words_list)).to_textfile(thesaurus_file)

    logging.info(f"Thesaurus file '{thesaurus_file}' created.")
