"""
Analysis of core sources and core authors

"""

import numpy as np
import pandas as pd
from techminer.term_analysis import count_documents_by_term
from techminer.utils import load_records
from techminer.utils.explode import explode


def core_authors(directory):
    """
    Returns a dataframe with the core analysis.

    Parameters
    ----------
    directory_or_records: str or list
        path to the directory or the records object.

    Returns
    -------
    pandas.DataFrame
        Dataframe with the core authors of the records
    """
    records = load_records(directory)

    z = count_documents_by_term(records, "authors", sep="; ")

    authors_dict = {
        author: num_docs for author, num_docs in zip(z.index, z) if not pd.isna(author)
    }

    #
    #  Num Authors x Documents written per Author
    #
    # z = z[["num_documents"]]
    z = z.to_frame(name="num_documents")
    z = z.groupby(["num_documents"]).size()
    w = [str(round(100 * a / sum(z), 2)) + " %" for a in z]
    z = pd.DataFrame(
        {"Num Authors": z.tolist(), "%": w, "Documents written per Author": z.index}
    )
    z = z.sort_values(["Documents written per Author"], ascending=False)
    z["Acum Num Authors"] = z["Num Authors"].cumsum()
    z["% Acum"] = [
        str(round(100 * a / sum(z["Num Authors"]), 2)) + " %"
        for a in z["Acum Num Authors"]
    ]
    m = explode(records[["authors", "record_id"]], "authors")
    m = m.dropna()
    m["Documents_written"] = m.authors.map(lambda w: authors_dict[w])

    n = []
    for k in z["Documents written per Author"]:
        s = m.query("Documents_written >= " + str(k))
        s = s[["record_id"]]
        s = s.drop_duplicates()
        n.append(len(s))

    k = []
    for index in range(len(n) - 1):
        k.append(n[index + 1] - n[index])
    k = [n[0]] + k
    z["Num Documents"] = k
    z["% Num Documents"] = [str(round(i / max(n) * 100, 2)) + "%" for i in k]
    z["Acum Num Documents"] = n
    z["% Acum Num Documents"] = [str(round(i / max(n) * 100, 2)) + "%" for i in n]

    z = z[
        [
            "Num Authors",
            "%",
            "Acum Num Authors",
            "% Acum",
            "Documents written per Author",
            "Num Documents",
            "% Num Documents",
            "Acum Num Documents",
            "% Acum Num Documents",
        ]
    ]

    return z.reset_index(drop=True)
