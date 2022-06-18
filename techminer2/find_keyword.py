"""
Find Keyword
===============================================================================

Finds a string in the terms of a column of a document collection.

>>> from techminer2 import *
>>> directory = "data/"
>>> find_keyword(contains='artificial intelligence', directory=directory)
artificial intelligence
     artificial intelligence
     artificial intelligence (ai)
artificial intelligence systems
artificial intelligence technologies


"""
from os.path import isfile, join

import pandas as pd

from .thesaurus import load_file_as_dict


def find_keyword(
    contains=None,
    startswith=None,
    endswith=None,
    directory="./",
):
    """
    Find the specified keyword and reorder the thesaurus to reflect the search.

    """

    thesaurus_file = join(directory, "processed", "keywords.txt")
    if isfile(thesaurus_file):
        th = load_file_as_dict(thesaurus_file)
    else:
        raise FileNotFoundError("The file {} does not exist.".format(thesaurus_file))

    reversed_th = {value: key for key, values in th.items() for value in values}

    df = pd.DataFrame(
        {
            "text": reversed_th.keys(),
            "key": reversed_th.values(),
        }
    )

    if contains is not None:
        result = []
        if isinstance(contains, str):
            contains = [contains]
        for word in contains:
            result.append(df[df.text.str.contains(word)])
        df = pd.concat(result)
    elif startswith is not None:
        result = []
        if isinstance(startswith, str):
            startswith = [startswith]
        for word in startswith:
            result.append(df[df.text.str.startswith(word)])
        df = pd.concat(result)
    elif endswith is not None:
        result = []
        if isinstance(endswith, str):
            endswith = [endswith]
        for word in endswith:
            result.append(df[df.text.str.endswith(word)])
        df = pd.concat(result)
    else:
        raise ValueError("No filter provided")

    keys = df.key.drop_duplicates()

    findings = {key: th[key] for key in sorted(keys)}

    for key, items in sorted(findings.items()):
        print(key)
        if len(items) > 1:
            for item in sorted(items):
                print("    ", item)

    # reorder the thesaurus to reflect the search
    for key in findings.keys():
        th.pop(key)

    with open(thesaurus_file, "w", encoding="utf-8") as file:

        for key in sorted(findings.keys()):
            file.write(key + "\n")
            for item in findings[key]:
                file.write("    " + item + "\n")

        for key in sorted(th.keys()):
            file.write(key + "\n")
            for item in th[key]:
                file.write("    " + item + "\n")
