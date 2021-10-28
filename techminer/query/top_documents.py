"""
Top Documents
============


"""
from techminer.data.records import load_records


def top_documents(
    directory_or_records,
    global_citations=True,
    normalized_citations=False,
    n_top=50,
):
    """
    Returns the top documents of the given directory or records.

    Parameters
    ----------
    directory_or_records: str
        Directory or records to be analyzed.
    global_citations: bool
        Whether to use global citations or not.
    normalized_citations: bool
        Whether to use normalized citations or not.

    Returns
    -------
    top_documents: pandas.DataFrame
        Top documents.
    """
    if isinstance(directory_or_records, str):
        records = load_records(directory_or_records)
    else:
        records = directory_or_records

    max_pub_year = records.pub_year.dropna().max()

    records["global_normalized_citations"] = records.global_citations.map(
        lambda w: round(w / max_pub_year, 3), na_action="ignore"
    )

    records["local_normalized_citations"] = records.local_citations.map(
        lambda w: round(w / max_pub_year, 3), na_action="ignore"
    )

    records["global_citations"] = records.global_citations.map(int, na_action="ignore")

    citations_column = {
        (True, True): "global_normalized_citations",
        (True, False): "global_citations",
        (False, True): "local_normalized_citations",
        (False, False): "local_citations",
    }[(global_citations, normalized_citations)]

    records = records.sort_values(citations_column, ascending=False)
    records = records.reset_index(drop=True)

    records = records[
        [
            "authors",
            "pub_year",
            "document_title",
            "publication_name",
            "record_id",
            citations_column,
        ]
    ].head(n_top)

    records = records.sort_values(by=citations_column, ascending=False)

    return records
