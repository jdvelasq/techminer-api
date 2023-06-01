"""Clusters summarization"""
import glob
import os

from .create_directory import create_directory
from .techminer.reports.abstracts_report import abstracts_report


def cluster_abstracts_report(
    criterion,
    communities,
    directory_for_abstracts,
    n_keywords=10,
    # n_abstracts=50,
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Clusters summarization."""

    create_directory(
        base_dir=directory,
        target_dir=directory_for_abstracts,
    )

    communities = communities.head(n_keywords)
    for community_name in communities:
        community = communities[community_name].tolist()
        community = [x for x in community if x != ""]
        community = [" ".join(x.split()[:-1]) for x in community]

        file_name = os.path.join(
            directory_for_abstracts, community_name + ".txt"
        )

        abstracts_report(
            field=criterion,
            custom_topics=community,
            file_name=file_name,
            # n_abstracts=n_abstracts,
            use_textwrap=True,
            root_dir=directory,
            database=database,
            year_filter=start_year,
            cited_by_filter=end_year,
            **filters,
        )
