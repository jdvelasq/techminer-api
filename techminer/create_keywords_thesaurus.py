import os.path
from os.path import isfile

import pandas as pd

from techminer.utils.thesaurus import Thesaurus, load_file_as_dict, text_clustering

from .utils import *


def create_keywords_thesaurus(records_path):
    """
    Createa a keywords thesaurus from the keywords in the articles.

    """
    logging.info("Creating keywords thesaurus ...")

    data = load_records_from_directory(records_path)

    thesaurus_file = records_path + "keywords.txt"

    words_list = []

    if "author_keywords" in data.columns:
        words_list += data.author_keywords.tolist()

    if "index_keywords" in data.columns:
        words_list += data.index_keywords.tolist()

    ##
    ## Rules for keywords
    ##
    words_list = [words for words in words_list if not pd.isna(words)]
    words_list = [word for words in words_list for word in words.split(";")]
    words_list = [word for word in words_list if len(word.strip()) > 2]
    words_list = [
        word.replace('"', "")
        .replace(chr(8212), "")
        .replace(chr(8220), "")
        .replace(chr(8221), "")
        for word in words_list
    ]
    words_list = [
        word.replace("-", "") if word[0] == "-" and len(word) > 1 else word
        for word in words_list
    ]

    if os.path.isfile(thesaurus_file):

        ##
        ##  Loads existent thesaurus
        ##
        dict_ = load_file_as_dict(thesaurus_file)

        ##
        ##  Selects words to cluster
        ##
        clustered_words = [word for key in dict_.keys() for word in dict_[key]]
        words_list = [word for word in words_list if word not in clustered_words]

        if len(words_list) > 0:

            th = text_clustering(pd.Series(words_list))

            th = Thesaurus(
                x={**th._thesaurus, **dict_},
                ignore_case=True,
                full_match=False,
                use_re=False,
            )
            th.to_textfile(thesaurus_file)

    else:
        #
        # Creates a new thesaurus
        #
        text_clustering(pd.Series(words_list)).to_textfile(thesaurus_file)

    logging.info(f"Thesaurus file '{thesaurus_file}' created.")
