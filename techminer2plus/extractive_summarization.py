# flake8: noqa
# pylint: disable=line-too-long
"""
Abstracts Extractive Summarization 
===============================================================================


>>> root_dir = "data/regtech/"

>>> from techminer2 import techminer
>>> techminer.reports.extractive_summarization(
...     criterion="author_keywords",
...     custom_topics=["blockchain", "artificial intelligence"],
...     n_abstracts=50,    
...     n_phrases_per_algorithm=50,
...     root_dir=root_dir,
... )
--INFO-- The file 'data/regtech/reports/extractive_summarization.txt' was created

"""

import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer

# from ...utils import records_utils
# from .abstracts_report import _sort_by_custom_terms, _write_report


def extractive_summarization(
    criterion,
    custom_topics,
    file_name="extractive_summarization.txt",
    n_abstracts=50,
    n_phrases_per_algorithm=1000,
    root_dir="./",
    database="main",
    start_year=None,
    end_year=None,
    **filters,
):
    """Abstract extractive summarization using sumy."""

    records = records.read_records(
        root_dir=root_dir,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )
    records = records.dropna(subset=["abstract"])

    selected_records = _select_records(
        criterion, custom_topics, n_abstracts, records
    )
    document = _create_document(selected_records)
    summary = _generate_summary(n_phrases_per_algorithm, document)
    summary = _get_article(selected_records, summary)
    records.index = records.article
    article = summary.article.drop_duplicates().tolist()
    records = records.loc[article, :]

    records = _sort_criterion_field(
        records=records, criterion=criterion, custom_topics=custom_topics
    )
    records = _sort_summary(
        records=records, criterion=criterion, custom_topics=custom_topics
    )

    _write_report(
        criterion=criterion,
        file_name=file_name,
        use_textwrap=True,
        directory=root_dir,
        records=records,
    )


def _sort_summary(records, criterion, custom_topics):
    records["TOPICS"] = records[criterion].copy()
    records["TOPICS"] = records["TOPICS"].str.split(";")
    records["TOPICS"] = records["TOPICS"].map(lambda x: [y.strip() for y in x])

    records["POINTS"] = ""
    for topic in custom_topics:
        records["POINTS"] += records["TOPICS"].map(
            lambda x: "1" if topic in x else "0"
        )

    records = records.sort_values(
        by=["POINTS", "global_citations", "local_citations"],
        ascending=[False, False, False],
    )

    records["RNK"] = records.groupby("POINTS")["global_citations"].rank(
        ascending=False, method="dense"
    )

    records = records.sort_values(
        by=["POINTS", "RNK"], ascending=[False, True]
    )

    records = records[records["RNK"] < 10]

    return records


def _sort_criterion_field(records, criterion, custom_topics):
    records["TERMS"] = records[criterion].str.split(";")
    records["TERMS"] = records["TERMS"].map(lambda x: [y.strip() for y in x])
    records["TERMS_1"] = records["TERMS"].map(
        lambda x: [
            "(*) " + custom_topic
            for custom_topic in custom_topics
            if custom_topic in x
        ],
        na_action="ignore",
    )
    records["TERMS_2"] = records["TERMS"].map(
        lambda x: [y for y in x if y not in custom_topics], na_action="ignore"
    )
    records["TERMS"] = records["TERMS_1"] + records["TERMS_2"]
    records[criterion] = records["TERMS"].str.join("; ")
    return records


def _get_article(records, summary):
    summarization = pd.DataFrame({"phrase": summary})
    summarization["article"] = pd.NA
    for record in records.itertuples():
        summarization.loc[
            summarization["phrase"].map(
                lambda x: x[:50] in record.abstract, na_action="ignore"
            ),
            "article",
        ] = record.article

    summarization = summarization.dropna(subset=["article"])

    # records.index = records.article

    return summarization


def _select_phrases_with_keywords(custom_topics, summary):
    final_summary = []
    for topic in custom_topics:
        for sentence in summary:
            if topic in sentence:
                final_summary.append(sentence)
    final_summary = list(set(final_summary))
    return final_summary


def _generate_summary(n_phrases_per_algorithm, document):
    summary_with_lexrank = _summarize_with_lexrank(
        document, n_phrases_per_algorithm
    )
    summary_with_lsasummarizer = _summarize_with_lsasummarizer(
        document, n_phrases_per_algorithm
    )
    summary_with_luhn = _summarize_with_luhn(document, n_phrases_per_algorithm)
    summary_with_klsummarizer = _summarize_with_klsummarizer(
        document, n_phrases_per_algorithm
    )

    summary = (
        summary_with_lexrank
        + summary_with_lsasummarizer
        + summary_with_luhn
        + summary_with_klsummarizer
    )

    # summary = [phrase[:-1] for phrase in summary if phrase[-1] == "."]
    # summary = [text for phrase in summary for text in phrase.split(".")]

    summary = list(set(summary))
    return summary


def _summarize_with_klsummarizer(document, n_phrases_per_algorithm):
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = KLSummarizer()
    summary = summarizer(parser.document, n_phrases_per_algorithm)
    summary = [str(sentence) for sentence in summary]
    return summary


def _summarize_with_luhn(document, n_phrases_per_algorithm):
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, n_phrases_per_algorithm)
    summary = [str(sentence) for sentence in summary]
    return summary


def _summarize_with_lsasummarizer(document, n_phrases_per_algorithm):
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, n_phrases_per_algorithm)
    summary = [str(sentence) for sentence in summary]
    return summary


def _summarize_with_lexrank(document, n_phrases_per_algorithm):
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, n_phrases_per_algorithm)
    summary = [str(sentence) for sentence in summary]
    return summary


def _create_document(records):
    abstracts = records["abstract"]
    abstracts = abstracts.dropna()
    document = "\n".join(abstracts.tolist())
    return document


def _select_records(criterion, custom_topics, n_abstracts, records):
    records = _sort_by_custom_terms(criterion, custom_topics, records)
    records = records.head(n_abstracts)
    return records
