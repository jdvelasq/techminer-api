"""
Impact analysis
================

"""

import numpy as np
import pandas as pd
from techminer.data import load_records, load_stopwords
from techminer.query import count_documents_by_term, count_global_citations_by_term
from techminer.utils import explode


def compute_h_and_g_index(records, column):
    """
    Compute the h-index of a column

    """
    citations = records[[column, "global_citations", "record_id"]].copy()
    citations = (
        records.assign(
            rn=records.sort_values("global_citations", ascending=False)
            .groupby(column)
            .cumcount()
            + 1
        )
    ).sort_values([column, "global_citations", "rn"], ascending=[False, False, True])
    citations["rn2"] = citations.rn.map(lambda w: w * w)

    h_values = citations.query("global_citations >= rn")
    h_values = h_values.groupby(column, as_index=False).agg({"rn": np.max})
    h_dict = {key: value for key, value in zip(h_values[column], h_values.rn)}

    g_values = citations.query("global_citations >= rn2")
    g_values = g_values.groupby(column, as_index=False).agg({"rn": np.max})
    g_dict = {key: value for key, value in zip(g_values[column], g_values.rn)}

    return h_dict, g_dict


def compute_impact_index(directory_or_records, column, stopwords=None):
    """
    Impact analysis

    Parameters
    ----------
    directory_or_records: str
        Directory or pandas dataframe with records.
    column: str
        Name of the column to analyze
    stopwords: list
        List of stopwords to remove from the analysis.

    Returns
    -------
    impact_analysis: pandas.DataFrame
        Impact analysis of the column
    """

    if column not in ["authors", "authors_id", "countries", "institutions"]:
        raise ValueError(
            "Impact analysis only works with 'authors', 'authors_id', 'countries' or 'institutions'."
        )

    records = load_records(directory_or_records)
    stopwords = load_stopwords(stopwords)

    columns_to_explode = [
        column,
        "global_citations",
    ]
    detailed_citations = records[columns_to_explode]
    detailed_citations = explode(detailed_citations[columns_to_explode], column)
    detailed_citations = detailed_citations.assign(
        cumcount_=detailed_citations.sort_values("global_citations", ascending=False)
        .groupby(column)
        .cumcount()
        + 1
    )
    detailed_citations = detailed_citations.sort_values(
        [column, "global_citations", "cumcount_"], ascending=[False, False, True]
    )
    detailed_citations = detailed_citations.assign(
        cumcount_2=detailed_citations.cumcount_.map(lambda w: w * w)
    )

    h_indexes = detailed_citations.query("global_citations >= cumcount_")
    h_indexes = h_indexes.groupby(column, as_index=True).agg({"cumcount_": np.max})
    h_indexes = h_indexes.rename(columns={"cumcount_": "h_index"})

    g_indexes = detailed_citations.query("global_citations >= cumcount_2")
    g_indexes = g_indexes.groupby(column, as_index=True).agg({"cumcount_": np.max})
    g_indexes = g_indexes.rename(columns={"cumcount_": "g_index"})

    age = records[
        [
            column,
            "pub_year",
        ]
    ]
    age = explode(age, column)
    age = (
        age.groupby(column, as_index=True)
        .agg({"pub_year": np.min})
        .rename(columns={"pub_year": "age"})
    )
    age = records.pub_year.max() - age.age + 1

    num_documents = count_documents_by_term(records, column)
    num_global_citations = count_global_citations_by_term(records, column)

    impact_analysis = pd.concat(
        [h_indexes, g_indexes, age, num_documents, num_global_citations],
        axis=1,
        sort=False,
    )

    impact_analysis = impact_analysis.assign(
        m_index=impact_analysis.h_index / impact_analysis.age
    )
    impact_analysis = impact_analysis.assign(
        global_citations_per_year=impact_analysis.global_citations / impact_analysis.age
    )
    impact_analysis = impact_analysis.assign(
        avg_global_citations=impact_analysis.global_citations
        / impact_analysis.num_documents
    )

    impact_analysis = impact_analysis.fillna(0)

    impact_analysis["m_index"] = impact_analysis.m_index.round(decimals=2)
    impact_analysis[
        "global_citations_per_year"
    ] = impact_analysis.global_citations_per_year.round(decimals=2)
    impact_analysis[
        "avg_global_citations"
    ] = impact_analysis.avg_global_citations.round(decimals=2)

    impact_analysis = impact_analysis.drop(columns=["age"])

    impact_analysis["h_index"] = impact_analysis["h_index"].astype(int)
    impact_analysis["g_index"] = impact_analysis["g_index"].astype(int)

    return impact_analysis

    #
    detailed_citations = records[[column, "global_citations", "record_id"]]

    agg = {
        "global_citations": np.sum,
    }
    detailed_citations = explode(detailed_citations[columns_to_explode], column)
    detailed_citations = (
        detailed_citations.assign(
            rn=detailed_citations.sort_values("global_citations", ascending=False)
            .groupby(column)
            .cumcount()
            + 1
        )
    ).sort_values([column, "global_citations", "rn"], ascending=[False, False, True])
    detailed_citations = detailed_citations.assign(
        rn2=detailed_citations.rn.map(lambda w: w * w)
    )

    h_index_values = detailed_citations.query("global_citations >= rn")
    h_index_values = h_index_values.groupby(column, as_index=True).agg({"rn": np.max})

    g_index_values = detailed_citations.query("global_citations >= rn2")
    g_index_values = g_index_values.groupby(column, as_index=True).agg({"rn": np.max})

    return h_index_values

    impact_analysis = impact_analysis.assign(first_year=impact_analysis.pub_year)
    impact_analysis = impact_analysis.assign(num_documents=1)
    columns_to_explode = [
        column,
        "num_documents",
        "global_citations",
        "first_year",
        "record_id",
    ]
    agg = {
        "num_documents": np.sum,
        "global_citations": np.sum,
        "first_year": np.min,
    }

    impact_analysis = explode(impact_analysis[columns_to_explode], column)

    records = records.copy()
    records = records.assign(first_year=records.pub_year)
    records = records.assign(num_documents=1)
    records = records.assign(
        frac_num_documents=records.frac_num_documents.map(
            lambda w: round(w, 2), na_action="ignore"
        )
    )
    if column == "authors":
        columns_to_explode = [
            column,
            "frac_num_documents",
            "num_documents",
            "global_citations",
            "first_year",
            "record_id",
        ]

        agg = {
            "frac_num_documents": np.sum,
            "num_documents": np.sum,
            "global_citations": np.sum,
            "first_year": np.min,
        }
    else:
        columns_to_explode = [
            column,
            "num_documents",
            "global_citations",
            "first_year",
            "record_id",
        ]
        agg = {
            "num_documents": np.sum,
            "global_citations": np.sum,
            "first_year": np.min,
        }
    exploded_records = explode(records[columns_to_explode], column)
    result = exploded_records.groupby(column, as_index=False).agg(agg)
    result = result.assign(last_year=records.pub_year.max())
    result = result.assign(years=result.last_year - result.first_year + 1)
    result = result.assign(
        global_citations_per_year=result.global_citations / result.years
    )
    result["global_citations_per_year"] = result.global_citations_per_year.map(
        lambda w: round(w, 2)
    )
    result = result.assign(
        avg_global_citations=result.global_citations / result.num_documents
    )
    result["avg_global_citations"] = result.avg_global_citations.map(
        lambda w: round(w, 2)
    )
    result["global_citations"] = result.global_citations.astype(int)

    #
    # Indice H
    #
    h_dict, g_dict = compute_h_and_g_index(records, column)
    result = result.assign(h_index=result[column].map(h_dict))
    result = result.assign(m_index=result.h_index / result.years)
    result["m_index"] = result["m_index"].map(lambda w: round(w, 2))
    result = result.assign(g_index=result[column].map(g_dict))

    ## limit to / exclude options
    # result = exclude_terms(data=result, axis=0)

    return result
