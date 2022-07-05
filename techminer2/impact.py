"""Make impact indicators plot."""

import textwrap

from .bar_px import bar_px
from .cleveland_px import cleveland_px
from .column_px import column_px
from .impact_indicators import impact_indicators
from .line_px import line_px
from .pie_px import pie_px

TEXTLEN = 40


def impact(
    column,
    impact_measure="h_index",
    top_n=20,
    directory="./",
    title=None,
    plot="cleveland",
):
    """computes local impact by <column>"""

    if impact_measure not in [
        "h_index",
        "g_index",
        "m_index",
        "global_citations",
    ]:
        raise ValueError(
            "Impact measure must be one of: h_index, g_index, m_index, global_citations"
        )

    indicators = impact_indicators(directory=directory, column=column)
    indicators = indicators.sort_values(by=impact_measure, ascending=False)
    indicators = indicators.head(top_n)
    indicators = indicators.reset_index()
    indicators[column] = indicators[column].apply(_shorten)

    column_names = {
        column: column.replace("_", " ").title() for column in indicators.columns
    }
    indicators = indicators.rename(columns=column_names)

    plot_function = {
        "bar": bar_px,
        "column": column_px,
        "line": line_px,
        "pie": pie_px,
        "cleveland": cleveland_px,
    }[plot]

    return plot_function(
        dataframe=indicators,
        x_label=impact_measure.replace("_", " ").title(),
        y_label=column.replace("_", " ").title(),
        title=title,
    )


def _shorten(text):
    return textwrap.shorten(
        text=text,
        width=TEXTLEN,
        placeholder="...",
        break_long_words=False,
    )
