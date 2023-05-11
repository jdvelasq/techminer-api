"""
Abstracts Report
===============================================================================


>>> directory = "data/regtech/"

>>> # file generated in data/regtech/reports/abstracts_report.txt
>>> from techminer2 import techminer

>>> techminer.reports.abstracts_report(
...     criterion="author_keywords",
...     custom_topics=["regulatory technology", "regtech"],
...     directory=directory,
... )
--INFO-- The file 'data/regtech/reports/abstracts_report.txt' was created

"""
import os.path
import sys
import textwrap

import pandas as pd

from ..._read_records import read_records


def abstracts_report(
    criterion=None,
    custom_topics=None,
    file_name="abstracts_report.txt",
    use_textwrap=True,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Extracts abstracts of documents meeting the given criteria."""

    records = read_records(
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    if criterion is not None:
        records = _sort_by_custom_terms(criterion, custom_topics, records)
    else:
        records = records.sort_values(
            by=["global_citations", "local_citations"],
            ascending=[False, False],
        )

    # records = records.head(n_abstracts)

    _write_report(criterion, file_name, use_textwrap, directory, records)


def _sort_by_custom_terms(criterion, custom_topics, records):
    selected_records = records[["article", criterion]]
    selected_records[criterion] = selected_records[criterion].str.split(";")
    selected_records = selected_records.explode(criterion)
    selected_records[criterion] = selected_records[criterion].str.strip()
    selected_records = selected_records[selected_records[criterion].isin(custom_topics)]
    records = records[records["article"].isin(selected_records["article"])]

    ##
    records["TOPICS"] = records[criterion].copy()
    records["TOPICS"] = records["TOPICS"].str.split(";")
    records["TOPICS"] = records["TOPICS"].map(lambda x: [y.strip() for y in x])

    records["POINTS"] = ""
    for topic in custom_topics:
        records["POINTS"] += records["TOPICS"].map(lambda x: "1" if topic in x else "0")

    records = records.sort_values(
        by=["POINTS", "global_citations", "local_citations"],
        ascending=[False, False, False],
    )

    # records["RNK"] = records.groupby("POINTS")["global_citations"].rank(
    #     ascending=False, method="dense"
    # )

    # records = records[records["RNK"] < 10]

    records["TERMS"] = records[criterion].str.split(";")
    records["TERMS"] = records["TERMS"].map(lambda x: [y.strip() for y in x])
    records["TERMS_1"] = records["TERMS"].map(
        lambda x: [
            "(*) " + custom_topic for custom_topic in custom_topics if custom_topic in x
        ],
        na_action="ignore",
    )
    records["TERMS_2"] = records["TERMS"].map(
        lambda x: [y for y in x if y not in custom_topics], na_action="ignore"
    )
    records["TERMS"] = records["TERMS_1"] + records["TERMS_2"]
    records[criterion] = records["TERMS"].str.join("; ")
    return records


def _write_report(criterion, file_name, use_textwrap, directory, records):
    file_path = os.path.join(directory, "reports", file_name)

    with open(file_path, "w", encoding="utf-8") as out_file:
        counter = 0

        text_article = ""

        for _, row in records.iterrows():
            if use_textwrap:
                if not pd.isna(row["article"]):
                    text_article = textwrap.fill(
                        row["article"],
                        width=87,
                        initial_indent=" " * 0,
                        subsequent_indent=" " * 3,
                        fix_sentence_endings=True,
                    )
                if not pd.isna(row["title"]):
                    text_title = textwrap.fill(
                        row["title"],
                        width=87,
                        initial_indent=" " * 0,
                        subsequent_indent=" " * 3,
                        fix_sentence_endings=True,
                    )
                if not pd.isna(row[criterion]):
                    text_criterion = textwrap.fill(
                        row[criterion],
                        width=87,
                        initial_indent=" " * 0,
                        subsequent_indent=" " * 3,
                        fix_sentence_endings=True,
                    )
                if "abstract" in row.index and not pd.isna(row["abstract"]):
                    text_abstract = textwrap.fill(
                        row["abstract"],
                        width=87,
                        initial_indent=" " * 0,
                        subsequent_indent=" " * 3,
                        fix_sentence_endings=True,
                    )
                else:
                    text_abstract = ""

            else:
                text_article = row["article"]
                text_title = row["title"]
                text_criterion = row[criterion]
                if not pd.isna(row["abstract"]):
                    text_abstract = row["abstract"]

            text_citation = str(row["global_citations"])

            # print("-" * 90, file=out_file)
            print("-- {:03d} ".format(counter) + "-" * 83, file=out_file)
            print("AR ", end="", file=out_file)
            print(text_article, file=out_file)

            print("TI ", end="", file=out_file)
            print(text_title, file=out_file)

            print("KW ", end="", file=out_file)
            print(text_criterion, file=out_file)

            print("TC ", end="", file=out_file)
            print(text_citation, file=out_file)

            print("AB ", end="\n", file=out_file)
            print('"""', end="", file=out_file)
            text_abstract = text_abstract.split("\n")
            text_abstract = [x.strip() for x in text_abstract]
            text_abstract = " \\\n".join(text_abstract)
            print(text_abstract, file=out_file)
            print('"""', end="\n", file=out_file)

            print("\n", file=out_file)

            counter += 1

    sys.stdout.write(f"--INFO-- The file '{file_path}' was created\n")
