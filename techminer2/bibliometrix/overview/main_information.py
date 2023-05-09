"""Main information
===============================================================================


>>> directory = "data/regtech/"

>>> from techminer2 import bibliometrix
>>> r = bibliometrix.overview.main_information(directory)
>>> r.table_
                                                            Value
Category       Item                                              
GENERAL        Timespan                                 2016:2023
               Documents                                       52
               Annual growth rate %                         63.87
               Document average age                          2.77
               References                                    2968
               Average citations per document               10.83
               Average citations per document per year       1.35
               Average references per document              59.36
               Sources                                         46
               Average documents per source                  1.13
DOCUMENT TYPES article                                         31
               book                                             1
               book_chapter                                     9
               conference_paper                                11
AUTHORS        Authors                                      102.0
               Authors of single-authored documents          19.0
               Single-authored documents                     19.0
               Multi-authored documents                      33.0
               Authors per document                          2.29
               Co-authors per document                       3.03
               International co-authorship %                23.08
               Author appearances                           119.0
               Documents per author                          0.44
               Collaboration index                            1.0
               Organizations                                 80.0
               Organizations (1st author)                    44.0
               Countries                                     29.0
               Countries (1st author)                        25.0
KEYWORDS       Raw author keywords                            149
               Cleaned author keywords                        144
               Raw index keywords                             155
               Cleaned index keywords                         150


            
               
>>> file_name = "sphinx/_static/bibliometrix__main_info_plot.html"               
>>> r.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../_static/bibliometrix__main_info_plot.html" height="600px" width="100%" frameBorder="0"></iframe>


    
>>> print(r.prompt_)
<BLANKLINE>
Act as a researcher and write a clear paragraph describing the 
main characteristics of the dataset with no more than 250 words. Use the
following table as a guide.
<BLANKLINE>
|                                                        | Value     |
|:-------------------------------------------------------|:----------|
| ('GENERAL', 'Timespan')                                | 2016:2023 |
| ('GENERAL', 'Documents')                               | 52        |
| ('GENERAL', 'Annual growth rate %')                    | 63.87     |
| ('GENERAL', 'Document average age')                    | 2.77      |
| ('GENERAL', 'References')                              | 2968      |
| ('GENERAL', 'Average citations per document')          | 10.83     |
| ('GENERAL', 'Average citations per document per year') | 1.35      |
| ('GENERAL', 'Average references per document')         | 59.36     |
| ('GENERAL', 'Sources')                                 | 46        |
| ('GENERAL', 'Average documents per source')            | 1.13      |
| ('DOCUMENT TYPES', 'article')                          | 31        |
| ('DOCUMENT TYPES', 'book')                             | 1         |
| ('DOCUMENT TYPES', 'book_chapter')                     | 9         |
| ('DOCUMENT TYPES', 'conference_paper')                 | 11        |
| ('AUTHORS', 'Authors')                                 | 102.0     |
| ('AUTHORS', 'Authors of single-authored documents')    | 19.0      |
| ('AUTHORS', 'Single-authored documents')               | 19.0      |
| ('AUTHORS', 'Multi-authored documents')                | 33.0      |
| ('AUTHORS', 'Authors per document')                    | 2.29      |
| ('AUTHORS', 'Co-authors per document')                 | 3.03      |
| ('AUTHORS', 'International co-authorship %')           | 23.08     |
| ('AUTHORS', 'Author appearances')                      | 119.0     |
| ('AUTHORS', 'Documents per author')                    | 0.44      |
| ('AUTHORS', 'Collaboration index')                     | 1.0       |
| ('AUTHORS', 'Organizations')                           | 80.0      |
| ('AUTHORS', 'Organizations (1st author)')              | 44.0      |
| ('AUTHORS', 'Countries')                               | 29.0      |
| ('AUTHORS', 'Countries (1st author)')                  | 25.0      |
| ('KEYWORDS', 'Raw author keywords')                    | 149       |
| ('KEYWORDS', 'Cleaned author keywords')                | 144       |
| ('KEYWORDS', 'Raw index keywords')                     | 155       |
| ('KEYWORDS', 'Cleaned index keywords')                 | 150       |
<BLANKLINE>
<BLANKLINE>

"""
import datetime

import numpy as np
import pandas as pd

from ..._read_records import read_records
from dataclasses import dataclass
import plotly.graph_objects as go


class _MainInformation:
    def __init__(
        self,
        directory,
        database="documents",
        start_year=None,
        end_year=None,
        **filters,
    ):
        self.directory = directory
        self.records = read_records(
            directory=directory,
            database=database,
            start_year=start_year,
            end_year=end_year,
            **filters,
        )
        self.n_records = len(self.records)
        self.compute_general_information_stats()
        self.compute_document_types_stats()
        self.compute_authors_stats()
        self.compute_keywords_stats()
        self.make_report()

    def make_report(self):
        pdf = pd.concat(
            [
                self.general_information_stats,
                self.document_types_stats,
                self.authors_stats,
                self.keywords_stats,
            ]
        )
        index = pd.MultiIndex.from_arrays(
            [pdf.Category, pdf.Item], names=["Category", "Item"]
        )
        self.report_ = pd.DataFrame(pdf.Value.tolist(), columns=["Value"], index=index)

    #####################################################################################
    def compute_general_information_stats(self):
        self.general_information_stats = pd.DataFrame(
            columns=["Category", "Item", "Value"]
        )
        self.general_information_stats.loc[0] = [
            "GENERAL",
            "Timespan",
            self.compute_timespam(),
        ]
        self.general_information_stats.loc[1] = [
            "GENERAL",
            "Documents",
            self.documents(),
        ]
        self.general_information_stats.loc[2] = [
            "GENERAL",
            "Annual growth rate %",
            self.annual_growth_rate(),
        ]
        self.general_information_stats.loc[3] = [
            "GENERAL",
            "Document average age",
            self.document_average_age(),
        ]
        self.general_information_stats.loc[4] = [
            "GENERAL",
            "References",
            self.cited_references(),
        ]
        self.general_information_stats.loc[5] = [
            "GENERAL",
            "Average citations per document",
            self.average_citations_per_document(),
        ]
        self.general_information_stats.loc[6] = [
            "GENERAL",
            "Average citations per document per year",
            self.average_citations_per_document_per_year(),
        ]
        self.general_information_stats.loc[7] = [
            "GENERAL",
            "Average references per document",
            self.average_references_per_document(),
        ]
        self.general_information_stats.loc[8] = [
            "GENERAL",
            "Sources",
            self.sources(),
        ]
        self.general_information_stats.loc[9] = [
            "GENERAL",
            "Average documents per source",
            self.average_documents_per_source(),
        ]

    # -----------------------------------------------------------------------------------

    def compute_timespam(self):
        return str(min(self.records.year)) + ":" + str(max(self.records.year))

    def documents(self):
        return len(self.records)

    def annual_growth_rate(self):
        n_years = max(self.records.year) - min(self.records.year) + 1
        Po = len(self.records.year[self.records.year == min(self.records.year)])
        return round(100 * (np.power(self.n_records / Po, 1 / n_years) - 1), 2)

    def document_average_age(self):
        mean_years = self.records.year.copy()
        mean_years = mean_years.dropna()
        mean_years = mean_years.mean()
        current_year = datetime.datetime.now().year
        return round(int(current_year) - mean_years, 2)

    def cited_references(self):
        if "global_references" in self.records.columns:
            records = self.records.global_references.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            return len(records)
        else:
            return pd.NA

    def average_citations_per_document(self):
        if "global_citations" in self.records.columns:
            return round(self.records.global_citations.mean(), 2)
        else:
            return pd.NA

    def average_citations_per_document_per_year(self):
        if "global_citations" in self.records.columns:
            return round(
                self.records.global_citations.mean()
                / (self.records.year.max() - self.records.year.min() + 1),
                2,
            )
        else:
            return pd.NA

    def average_references_per_document(self):
        if "global_references" in self.records.columns:
            num_references = self.records.global_references.copy()
            num_references = num_references.dropna()
            num_references = num_references.str.split(";")
            num_references = num_references.map(len)
            return round(num_references.mean(), 2)
        else:
            return pd.NA

    def sources(self):
        if "source_title" in self.records.columns:
            records = self.records.source_title.copy()
            records = records.dropna()
            records = records.drop_duplicates()
            return len(records)
        else:
            return pd.NA

    def average_documents_per_source(self):
        if "source_title" in self.records.columns:
            sources = self.records.source_title.copy()
            sources = sources.dropna()
            n_records = len(sources)
            sources = sources.drop_duplicates()
            n_sources = len(sources)
            return round(n_records / n_sources, 2)
        else:
            return pd.NA

    #####################################################################################
    def compute_document_types_stats(self):
        self.document_types_stats = pd.DataFrame(columns=["Category", "Item", "Value"])
        records = self.records[["document_type"]].dropna()
        document_types_count = (
            records[["document_type"]].groupby("document_type").size()
        )
        for index, (document_type, count) in enumerate(
            zip(document_types_count.index, document_types_count)
        ):
            self.document_types_stats.loc[index] = [
                "DOCUMENT TYPES",
                document_type,
                count,
            ]

    #####################################################################################
    def compute_authors_stats(self):
        self.authors_stats = pd.DataFrame(columns=["Category", "Item", "Value"])
        self.authors_stats.loc[0] = [
            "AUTHORS",
            "Authors",
            self.authors(),
        ]
        self.authors_stats.loc[1] = [
            "AUTHORS",
            "Authors of single-authored documents",
            self.authors_of_single_authored_documents(),
        ]
        self.authors_stats.loc[2] = [
            "AUTHORS",
            "Single-authored documents",
            self.count_single_authored_documents(),
        ]
        self.authors_stats.loc[3] = [
            "AUTHORS",
            "Multi-authored documents",
            self.count_multi_authored_documents(),
        ]
        self.authors_stats.loc[4] = [
            "AUTHORS",
            "Authors per document",
            self.average_authors_per_document(),
        ]
        self.authors_stats.loc[5] = [
            "AUTHORS",
            "Co-authors per document",
            self.co_authors_per_document(),
        ]
        self.authors_stats.loc[6] = [
            "AUTHORS",
            "International co-authorship %",
            self.international_co_authorship(),
        ]
        self.authors_stats.loc[7] = [
            "AUTHORS",
            "Author appearances",
            self.author_appearances(),
        ]
        self.authors_stats.loc[8] = [
            "AUTHORS",
            "Documents per author",
            self.average_documents_per_author(),
        ]

        self.authors_stats.loc[9] = [
            "AUTHORS",
            "Collaboration index",
            self.collaboration_index(),
        ]
        self.authors_stats.loc[10] = [
            "AUTHORS",
            "Organizations",
            self.organizations(),
        ]
        self.authors_stats.loc[11] = [
            "AUTHORS",
            "Organizations (1st author)",
            self.organizations_1st_author(),
        ]
        self.authors_stats.loc[12] = [
            "AUTHORS",
            "Countries",
            self.countries(),
        ]
        self.authors_stats.loc[13] = [
            "AUTHORS",
            "Countries (1st author)",
            self.countries_1st_author(),
        ]

    # -----------------------------------------------------------------------------------

    def authors(self):
        records = self.records.authors.copy()
        records = records.dropna()
        records = records.str.split(";")
        records = records.explode()
        records = records.str.strip()
        records = records.drop_duplicates()
        return len(records)

    def authors_of_single_authored_documents(self):
        records = self.records[self.records["num_authors"] == 1]
        authors = records.authors.dropna()
        authors = authors.drop_duplicates()
        return len(authors)

    def count_single_authored_documents(self):
        return len(self.records[self.records["num_authors"] == 1])

    def count_multi_authored_documents(self):
        return len(self.records[self.records["num_authors"] > 1])

    def average_authors_per_document(self):
        num_authors = self.records["num_authors"].dropna()
        return round(num_authors.mean(), 2)

    def co_authors_per_document(self):
        records = self.records.copy()
        num_authors = records[records.num_authors > 1].num_authors
        return round(num_authors.mean(), 2)

    def international_co_authorship(self):
        countries = self.records.countries.copy()
        countries = countries.dropna()
        countries = countries.str.split(";")
        countries = countries.map(len)
        return round(len(countries[countries > 1]) / len(countries) * 100, 2)

    def author_appearances(self):
        records = self.records.authors.copy()
        records = records.dropna()
        records = records.str.split(";")
        records = records.explode()
        records = records.str.strip()
        return len(records)

    def average_documents_per_author(self):
        records = self.records.authors.copy()
        records = records.dropna()
        n_records = len(records)
        records = records.str.split(";")
        records = records.explode()
        n_authors = len(records)
        return round(n_records / n_authors, 2)

    def collaboration_index(self):
        records = self.records[["authors", "num_authors"]].copy()
        records = records.dropna()
        records = records[records.num_authors > 1]
        n_records = len(records)

        n_authors = records.authors.copy()
        n_authors = n_authors.str.split(";")
        n_authors = n_authors.explode()
        n_authors = len(records)
        return round(n_authors / n_records, 2)

    def organizations(self):
        if "organizations" in self.records.columns:
            records = self.records.organizations.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return pd.NA

    def organizations_1st_author(self):
        if "organization_1st_author" in self.records.columns:
            records = self.records.organization_1st_author.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return pd.NA

    def countries(self):
        if "countries" in self.records.columns:
            records = self.records.countries.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return pd.NA

    def countries_1st_author(self):
        if "country_1st_author" in self.records.columns:
            records = self.records.country_1st_author.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return pd.NA

    #####################################################################################
    def compute_keywords_stats(self):
        self.keywords_stats = pd.DataFrame(columns=["Category", "Item", "Value"])
        self.keywords_stats.loc[0] = [
            "KEYWORDS",
            "Raw author keywords",
            self.raw_author_keywords(),
        ]
        self.keywords_stats.loc[1] = [
            "KEYWORDS",
            "Cleaned author keywords",
            self.author_keywords(),
        ]
        self.keywords_stats.loc[2] = [
            "KEYWORDS",
            "Raw index keywords",
            self.raw_index_keywords(),
        ]
        self.keywords_stats.loc[3] = [
            "KEYWORDS",
            "Cleaned index keywords",
            self.index_keywords(),
        ]

    # -----------------------------------------------------------------------------------

    def raw_author_keywords(self):
        records = self.records.raw_author_keywords.copy()
        records = records.dropna()
        records = records.str.split(";")
        records = records.explode()
        records = records.str.strip()
        records = records.drop_duplicates()
        return len(records)

    def author_keywords(self):
        records = self.records.author_keywords.copy()
        records = records.dropna()
        records = records.str.split(";")
        records = records.explode()
        records = records.str.strip()
        records = records.drop_duplicates()
        return len(records)

    def raw_index_keywords(self):
        if "raw_index_keywords" in self.records.columns:
            records = self.records.raw_index_keywords.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return 0

    def index_keywords(self):
        if "index_keywords" in self.records.columns:
            records = self.records.index_keywords.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            records = records.drop_duplicates()
            return len(records)
        else:
            return 0


from plotly.subplots import make_subplots


def make_plot(report):
    def add_text_trace(fig, category, caption, row, col):
        text = (
            f'<span style="font-size: 8px;">{caption}</span><br>'
            f'<br><span style="font-size: 20px;">'
            f"{report.loc[(category, caption)].values[0]}</span>"
        )

        fig.add_trace(
            go.Scatter(
                x=[0.5],
                y=[0.5],
                text=[text],
                mode="text",
            ),
            row=row,
            col=col,
        )
        fig.update_xaxes(visible=False, row=row, col=col)
        fig.update_yaxes(visible=False, row=row, col=col)

    fig = make_subplots(rows=4, cols=3)

    add_text_trace(fig, "GENERAL", "Timespan", 1, 1)
    add_text_trace(fig, "GENERAL", "Sources", 1, 2)
    add_text_trace(fig, "GENERAL", "Documents", 1, 3)

    add_text_trace(fig, "GENERAL", "Annual growth rate %", 2, 1)
    add_text_trace(fig, "AUTHORS", "Authors", 2, 2)
    add_text_trace(fig, "AUTHORS", "Authors of single-authored documents", 2, 3)

    add_text_trace(fig, "AUTHORS", "International co-authorship %", 3, 1)
    add_text_trace(fig, "AUTHORS", "Co-authors per document", 3, 2)
    add_text_trace(fig, "KEYWORDS", "Raw author keywords", 3, 3)

    add_text_trace(fig, "GENERAL", "References", 4, 1)
    add_text_trace(fig, "GENERAL", "Document average age", 4, 2)
    add_text_trace(fig, "GENERAL", "Average citations per document", 4, 3)

    fig.update_layout(showlegend=False)
    fig.update_layout(title="Main Information")

    return fig


def make_chatpgt_prompt(report):
    report = report.copy()
    prompt = f"""
As a researcher, please provide a clear paragraph describing the main characteristics 
of the dataset using the following table as a guide:

{report.to_markdown()}

Limit your description to no more than 250 words.
"""

    return prompt


@dataclass(init=False)
class _Results:
    table_ = None
    plot_ = None
    prompt_ = None


def main_information(
    directory="./",
    database="documents",
    start_year=None,
    end_year=None,
    **filters,
):
    """Returns main statistics of the dataset."""

    obj = _MainInformation(
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    results = _Results()
    results.table_ = obj.report_
    results.plot_ = make_plot(obj.report_)
    results.prompt_ = make_chatpgt_prompt(obj.report_)

    return results
