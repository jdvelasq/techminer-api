"""
Import records

"""

import os

import pandas as pd
from techminer.utils import logging


def load_records(directory, fileerror=True):
    """
    Loads records from project directory.

    """
    if directory[-1] != "/":
        directory += "/"

    filename = directory + "records.csv"

    if not os.path.isfile(filename):
        if fileerror:
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        return pd.DataFrame()
    return pd.read_csv(filename, sep=",", encoding="utf-8")


def save_records(records, directory):
    """
    Saves records to project directory.

    """
    if directory[-1] != "/":
        directory += "/"

    filename = directory + "records.csv"
    if os.path.isfile(filename):
        logging.info(f"The file '{filename}' was rewrited.")

    records.to_csv(filename, sep=",", encoding="utf-8", index=False)
