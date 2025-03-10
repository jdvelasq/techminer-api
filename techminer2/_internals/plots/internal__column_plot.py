# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""Base Column Plot Class."""

import plotly.express as px  # type: ignore

MARKER_COLOR = "#7793a5"
MARKER_LINE_COLOR = "#465c6b"


def internal__column_plot(params, data_frame):

    y_col = params.terms_order_by

    hover_data = data_frame.columns.to_list()
    title_text = params.title_text
    xaxes_title_text = params.xaxes_title_text
    yaxes_title_text = params.yaxes_title_text

    fig = px.bar(
        data_frame,
        x=None,
        y=y_col,
        hover_data=hover_data,
        orientation="v",
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        title_text=title_text,
    )
    fig.update_traces(
        marker_color=MARKER_COLOR,
        marker_line={"color": MARKER_LINE_COLOR},
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
        tickangle=270,
        title_text=xaxes_title_text,
    )
    fig.update_yaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
        title_text=yaxes_title_text,
    )

    return fig
