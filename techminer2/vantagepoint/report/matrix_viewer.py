"""
Matrix Viwer
===============================================================================



**Matrix view for a occurrence matrix.**


>>> directory = "data/regtech/"

>>> file_name = "sphinx/_static/vantagepoint__matrix_viewer-0.html"

>>> from techminer2 import vantagepoint
>>> matrix = vantagepoint.analyze.matrix.occ_matrix_list(
...    criterion_for_columns='author_keywords',
...    criterion_for_rows='authors',
...    topic_min_occ=3,
...    directory=directory,
... )
>>> matrix.head()
                row                       column  OCC
0    Arner DW 3:185               regtech 28:329    2
1    Arner DW 3:185               fintech 12:249    1
2    Arner DW 3:185    financial services 04:168    1
3    Arner DW 3:185  financial regulation 04:035    2
4  Buckley RP 3:185               regtech 28:329    2


>>> vantagepoint.report.matrix_viewer(
...     matrix,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../_static/vantagepoint__matrix_viewer-0.html" height="600px" width="100%" frameBorder="0"></iframe>


**Matrix view for a co-occurrence matrix.**

>>> file_name = "sphinx/_static/vantagepoint__matrix_viewer-1.html"

>>> matrix = vantagepoint.analyze.matrix.co_occ_matrix_list(
...    criterion='author_keywords',
...    topic_min_occ=8,
...    directory=directory,
... )
>>> matrix.head()
              row          column  OCC
0  regtech 28:329  regtech 28:329   28
1  regtech 28:329  fintech 12:249   12
2  fintech 12:249  regtech 28:329   12
3  fintech 12:249  fintech 12:249   12

>>> vantagepoint.report.matrix_viewer(
...     matrix,
...     nx_k=0.5,
...     nx_iteratons=5,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../_static/vantagepoint__matrix_viewer-1.html" height="600px" width="100%" frameBorder="0"></iframe>



"""
import networkx as nx
import numpy as np
import plotly.graph_objects as go


def matrix_viewer(
    matrix_list,
    nx_k=0.5,
    nx_iteratons=10,
    delta=1.0,
):
    """Makes cluster map from a ocurrence flooding matrix."""

    column = matrix_list["column"].drop_duplicates().sort_values()
    row = matrix_list["row"].drop_duplicates().sort_values()
    if row.equals(column):
        return _matrix_viewer_for_co_occ_matrix(matrix_list, nx_k, nx_iteratons, delta)
    return _matrix_viewer_for_occ_matrix(matrix_list, nx_k, nx_iteratons, delta)


def _matrix_viewer_for_co_occ_matrix(matrix_list, nx_k, nx_iteratons, delta):
    graph = nx.Graph()
    graph = _create_nodes(graph, matrix_list, 0)
    graph = _create_edges(graph, matrix_list)
    graph = _make_layout(graph, nx_k, nx_iteratons)
    edge_trace, node_trace = _create_traces(graph)
    node_trace = _color_node_points(graph, node_trace)
    fig = _create_network_graph(edge_trace, node_trace, delta)
    return fig


def _matrix_viewer_for_occ_matrix(matrix_list, nx_k, nx_iteratons, delta):
    graph = nx.Graph()
    graph = _create_nodes(graph, matrix_list, 0)
    graph = _create_nodes(graph, matrix_list, 1)
    graph = _create_edges(graph, matrix_list)
    graph = _make_layout(graph, nx_k, nx_iteratons)
    edge_trace, node_trace = _create_traces(graph)
    node_trace = _color_node_points(graph, node_trace)
    fig = _create_network_graph(edge_trace, node_trace, delta)
    return fig


def _make_layout(G, k=0.2, iteratons=50):
    pos = nx.spring_layout(G, k=k, iterations=iteratons)
    for node in G.nodes():
        G.nodes[node]["pos"] = pos[node]
    return G


def _create_network_graph(edge_trace, node_trace, delta=1.0):
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="",
            titlefont=dict(size=16),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=0),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                    align="left",
                    font=dict(size=10),
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_family="monospace",
        )
    )
    fig.update_xaxes(range=[-1 - delta, 1 + delta])
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig


def _color_node_points(G, node_trace):
    node_adjacencies = []
    node_hove_text = []
    for _, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        text = "<b>" + adjacencies[0] + "</b>"
        max_len = list(adjacencies[1].keys())
        max_len = max([len(x) for x in max_len])
        fmt = "<br> {:>" + str(max_len) + "} {}"
        for key, value in adjacencies[1].items():
            text += fmt.format(key, value["weight"])
        node_hove_text.append(text)

    # node_trace.marker.color = node_adjacencies
    node_trace.hovertext = node_hove_text
    return node_trace


def _create_traces(G):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1.2, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    text = []
    colors = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)
        text.append(node)
        # if G.nodes[node]["group"] == 0:
        #     colors.append("#F1948A")
        # else:
        #     colors.append("#5DADE2")

        if G.nodes[node]["group"] == 0:
            colors.append("#1f77b4")
        else:
            colors.append("#FF7F0E")

    x_mean = np.mean(node_x)
    y_mean = np.mean(node_y)
    textposition = []
    for x_pos, y_pos in zip(node_x, node_y):
        if x_pos >= x_mean and y_pos >= y_mean:
            textposition.append("top right")
        if x_pos <= x_mean and y_pos >= y_mean:
            textposition.append("top left")
        if x_pos <= x_mean and y_pos <= y_mean:
            textposition.append("bottom left")
        if x_pos >= x_mean and y_pos <= y_mean:
            textposition.append("bottom right")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=text,
        marker=dict(
            color=colors,
            size=25,
            line_width=1,
            line_color="white",
        ),
        textposition=textposition,
    )

    return edge_trace, node_trace


def _create_edges(G, flood_matrix):
    edges = []
    for _, row in flood_matrix.iterrows():
        edges.append((row[0], row[1], row[2]))
    G.add_weighted_edges_from(edges)
    return G


def _create_nodes(G, flood_matrix, col_index):
    nodes = []

    col = flood_matrix[flood_matrix.columns[col_index]]
    value_counts = col.value_counts()
    nodes += [
        (item, dict(size=value_counts[item], group=col_index))
        for item in value_counts.index
    ]

    G.add_nodes_from(nodes)
    return G
