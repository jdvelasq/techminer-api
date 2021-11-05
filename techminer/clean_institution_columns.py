"""
Cleaning institutions fields
===============================================================================
"""
# pylint: disable=no-member

import os

import pandas as pd

from .utils import logging
from .utils.map import map_
from .utils.thesaurus import read_textfile


def clean_institution_columns(directory):
    """
    Cleans all the institution fields in the records in the given directory using the
    institutions thesaurus (institutions.txt file).

    """

    logging.info("Applying thesaurus to institutions ...")

    # --------------------------------------------------------------------------
    # Loads documents.csv
    filename = directory + "documents.csv"
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    documents = pd.read_csv(filename, sep=",", encoding="utf-8")
    # --------------------------------------------------------------------------

    if directory[-1] != "/":
        directory = directory + "/"

    #
    # Loads the thesaurus
    #
    thesaurus_file = directory + "institutions.txt"
    th = read_textfile(thesaurus_file)
    th = th.compile_as_dict()

    #
    # Copy affiliations to institutions
    #
    documents["institutions"] = documents.affiliations.map(
        lambda w: w.lower().strip(), na_action="ignore"
    )

    #
    # Cleaning
    #
    logging.info("Extract and cleaning institutions.")
    documents["institutions"] = map_(
        documents, "institutions", lambda w: th.apply_as_dict(w, strict=True)
    )

    logging.info("Extracting institution of first author ...")
    documents["institution_1st_author"] = documents.institutions.map(
        lambda w: w.split(";")[0] if isinstance(w, str) else w
    )

    # --------------------------------------------------------------------------
    documents.to_csv(
        directory + "documents.csv",
        sep=",",
        encoding="utf-8",
        index=False,
    )
    # --------------------------------------------------------------------------
    logging.info("The thesaurus was applied to institutions.")
