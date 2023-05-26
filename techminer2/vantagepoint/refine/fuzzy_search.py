"""
Fuzzy Search --- ChatGPT
===============================================================================

Finds a string in the terms of a thesaurus using fuzzy search.


>>> root_dir = "data/regtech/"

>>> from techminer2 import vantagepoint
>>> vantagepoint.refine.fuzzy_search(
...     thesaurus_file="keywords.txt",
...     patterns='intelligencia',
...     threshold=80,
...     root_dir=root_dir,
... )
ambient intelligence
artificial intelligence
     artificial intelligence
     artificial intelligence (ai)
artificial intelligence & law
artificial intelligence course
     artificial intelligence course
     artificial intelligence courses
artificial intelligence systems
artificial intelligence technologies
     artificial intelligence technologies
     artificial intelligence technology
augmented intelligence collaboration
business intelligence
collective intelligence
competitive intelligence
computational and artificial intelligence
     computational and artificial intelligence
     computational and artificial intelligences
computational intelligence
financial intelligence units
intelligence
intelligence activities
regulatory intelligence
responsible artificial intelligence


"""
import os.path
import sys

import pandas as pd
from fuzzywuzzy import process

from ..._thesaurus import load_file_as_dict


def fuzzy_search(
    thesaurus_file,
    patterns,
    threshold=80,
    root_dir="./",
):
    """Find the specified keyword and reorder the thesaurus file."""

    th_file = os.path.join(root_dir, "processed", thesaurus_file)
    if os.path.isfile(th_file):
        th_dict = load_file_as_dict(th_file)
    else:
        raise FileNotFoundError(f"The file {th_file} does not exist.")

    reversed_th = {
        value: key for key, values in th_dict.items() for value in values
    }

    pdf = pd.DataFrame(
        {
            "text": reversed_th.keys(),
            "key": reversed_th.values(),
        }
    )

    result = []

    if isinstance(patterns, str):
        patterns = [patterns]

    for pattern in patterns:
        potential_matches = process.extract(pattern, pdf.text, limit=None)
        for potential_match in potential_matches:
            if potential_match[1] >= threshold:
                result.append(pdf[pdf.text.str.contains(potential_match[0])])

    if len(result) == 0:
        sys.stdout.write(
            "--INFO-- No matches found for the current thresold\n"
        )
        return

    pdf = pd.concat(result)

    keys = pdf.key.drop_duplicates()

    findings = {key: th_dict[key] for key in sorted(keys)}

    # reorder the thesaurus to reflect the search
    for key in findings.keys():
        th_dict.pop(key)

    with open(th_file, "w", encoding="utf-8") as file:
        for key in sorted(findings.keys()):
            file.write(key + "\n")
            for item in findings[key]:
                file.write("    " + item + "\n")

        for key in sorted(th_dict.keys()):
            file.write(key + "\n")
            for item in th_dict[key]:
                file.write("    " + item + "\n")

    for key, items in sorted(findings.items()):
        print(key)
        if len(items) > 1:
            for item in sorted(items):
                print("    ", item)
