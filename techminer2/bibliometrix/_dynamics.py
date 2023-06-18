"""Bibliometrix generic dynamics plot."""

import textwrap
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px

# from ..techminer.indicators.indicators_by_field import indicators_by_field
# from ..techminer.indicators.indicators_by_field_per_year import (
#     indicators_by_field_per_year,
# )

TEXTLEN = 40


@dataclass(init=False)
class _Results:
    plot_ = None
    table_ = None


def _dynamics(
    criterion,
    topics_length=10,
    topic_min_occ=None,
    topic_min_citations=None,
    directory="./",
    plot=True,
    title=None,
    database="main",
    start_year=None,
    end_year=None,
    **filters,
):
    """Bibliometrix generic dynamics plot."""

    indicators = indicators_by_field_per_year(
        root_dir=directory,
        field=criterion,
        database=database,
        year_filter=start_year,
        cited_by_filter=end_year,
        **filters,
    )

    indicators = indicators[["OCC"]]
    indicators = indicators.reset_index()
    indicators = indicators.sort_values([criterion, "year"], ascending=True)
    indicators = indicators.pivot(
        index="year", columns=criterion, values="OCC"
    )
    indicators = indicators.fillna(0)

    # complete missing years
    year_range = list(
        range(indicators.index.min(), indicators.index.max() + 1)
    )
    missing_years = [
        year for year in year_range if year not in indicators.index
    ]
    pdf = pd.DataFrame(
        np.zeros((len(missing_years), len(indicators.columns))),
        index=missing_years,
        columns=indicators.columns,
    )
    indicators = indicators.append(pdf)
    indicators = indicators.sort_index()

    # top items
    selected_topics = indicators_by_field(
        root_dir=directory,
        field=criterion,
        database=database,
        year_filter=start_year,
        cited_by_filter=end_year,
        **filters,
    )
    selected_topics = selected_topics.sort_values(
        by=["OCC", "global_citations", "local_citations"],
        ascending=[False, False, False],
    )

    if topic_min_occ is not None:
        selected_topics = selected_topics[
            selected_topics["OCC"] >= topic_min_occ
        ]
    if topic_min_citations is not None:
        selected_topics = selected_topics[
            selected_topics["global_citations"] >= topic_min_citations
        ]
    selected_topics = selected_topics.head(topics_length)

    occ = indicators.sum(axis=0)
    occ = occ.sort_values(ascending=False)

    indicators = indicators[selected_topics.index]

    # cumsum
    indicators = indicators.cumsum()
    indicators = indicators.astype(int)
    if not plot:
        return indicators

    # plot
    indicators.columns = [col for col in indicators.columns]
    indicators = indicators.reset_index()
    indicators = indicators.rename(columns={"index": "year"})
    indicators = indicators.melt(
        id_vars="year",
        value_vars=indicators.columns,
        var_name=criterion,
        value_name="cum_OCC",
    )
    indicators[criterion] = indicators[criterion].apply(_shorten)

    #
    fig = px.line(
        indicators,
        x="year",
        y="cum_OCC",
        title=title,
        markers=True,
        hover_data=[criterion, "year", "cum_OCC"],
        color=criterion,
    )
    fig.update_traces(
        marker=dict(size=10, line=dict(color="darkslategray", width=2)),
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        # showlegend=False,
    )
    fig.update_yaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
        tickangle=270,
        dtick=1,
    )

    result = _Results()
    result.plot_ = fig
    result.table_ = indicators.reset_index(drop=True)

    return result


def _shorten(text):
    return textwrap.shorten(
        text=text,
        width=TEXTLEN,
        placeholder="...",
        break_long_words=False,
    )
