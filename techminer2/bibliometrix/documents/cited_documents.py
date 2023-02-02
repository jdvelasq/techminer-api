import plotly.express as px

from ...techminer.indicators.indicators_by_document import indicators_by_document


def bibiometrix_cited_documents(
    metric,
    directory="./",
    database="documents",
    top_n=20,
    title=None,
    start_year=None,
    end_year=None,
    **filters,
):
    """Most cited documents."""

    indicators = indicators_by_document(
        directory=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )
    indicators = indicators.sort_values(by=metric, ascending=False)
    indicators = indicators.head(top_n)
    indicators = indicators.rename(
        columns={col: col.replace("_", " ").title() for col in indicators.columns}
    )
    indicators = indicators.reset_index()

    indicators = indicators.rename(columns={"article": "Document"})

    fig = px.scatter(
        indicators,
        x=metric.replace("_", " ").title(),
        y="Document",
        hover_data=["Global Citations", "Local Citations"],
        title=title,
    )
    fig.update_traces(marker=dict(size=10, color="black"))
    fig.update_traces(textposition="middle right")
    fig.update_traces(line=dict(color="black"))
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    fig.update_yaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        autorange="reversed",
        griddash="dot",
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
    )

    return fig
