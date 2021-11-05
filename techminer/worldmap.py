"""
Worldmap
===============================================================================
"""
import json
from os.path import dirname, join

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .items_report import terms_table
from .utils import load_filtered_documents

TEXTLEN = 40


def _worldmap_plot(
    series,
    cmap="Pastel2",
    figsize=(6, 6),
    fontsize=9,
):

    """Worldmap plot with the number of documents per country.

    Examples
    ----------------------------------------------------------------------------------------------

    >>> import pandas as pd
    >>> x = pd.Series(
    ...    data = [1000, 900, 800, 700, 600, 1000],
    ...    index = ["China", "Taiwan", "United States", "United Kingdom", "India", "Colombia"],
    ... )
    >>> x
    China             1000
    Taiwan             900
    United States      800
    United Kingdom     700
    India              600
    Colombia          1000
    dtype: int64

    >>> fig = worldmap(x, figsize=(15, 6))
    >>> fig.savefig('/workspaces/techminer/sphinx/images/worldmap.png')

    .. image:: images/worldmap.png
        :width: 2000px
        :align: center


    """
    matplotlib.rc("font", size=fontsize)
    fig = plt.Figure(figsize=figsize)
    ax = fig.subplots()
    cmap = plt.cm.get_cmap(cmap)

    df = series.to_frame()

    df["color"] = series.map(
        lambda w: 0.1 + 0.9 * (w - series.min()) / (series.max() - series.min())
    )

    module_path = dirname(__file__)
    with open(join(module_path, "config/worldmap.data"), "r", encoding="utf-8") as file:
        countries = json.load(file)

    for country in countries.keys():
        data = countries[country]
        for item in data:
            ax.plot(item[0], item[1], "-k", linewidth=0.5)
            if country.lower() in df.index.tolist():
                ax.fill(item[0], item[1], color=cmap(df.color[country.lower()]))
    #
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xleft = xmax - 0.02 * (xmax - xmin)
    xright = xmax
    xbar = np.linspace(xleft, xright, 10)
    ybar = np.linspace(ymin, ymin + (ymax - ymin), 100)
    xv, yv = np.meshgrid(xbar, ybar)
    z = yv / (ymax - ymin) - ymin
    ax.pcolormesh(xv, yv, z, cmap=cmap)
    #
    pos = np.linspace(ymin, ymin + (ymax - ymin), 11)
    value = [
        round(series.min() + (series.max() - series.min()) * i / 10, 0)
        for i in range(11)
    ]
    for i in range(11):
        ax.text(
            xright + 0.4 * (xright - xleft),
            pos[i],
            str(int(value[i])),
            ha="left",
            va="center",
        )

    ax.plot(
        [xleft - 0.1 * (xright - xleft), xleft - 0.1 * (xright - xleft)],
        [ymin, ymax],
        color="gray",
        linewidth=1,
    )
    for i in range(11):
        ax.plot(
            [xleft - 0.0 * (xright - xleft), xright],
            [pos[i], pos[i]],
            linewidth=2.0,
            color=cmap((11 - i) / 11),
        )

    ax.set_aspect("equal")
    ax.axis("on")
    ax.set_xticks([])
    ax.set_yticks([])

    ax.spines["bottom"].set_color("gray")
    ax.spines["top"].set_color("gray")
    ax.spines["right"].set_color("gray")
    ax.spines["left"].set_color("gray")

    fig.set_tight_layout(True)

    return fig


def _worldmap_from_records(
    records,
    metric,
    cmap,
    figsize,
    fontsize,
):
    table = terms_table(records, column="countries", sep="; ")
    return _worldmap_plot(
        series=table[metric],
        cmap=cmap,
        figsize=figsize,
        fontsize=fontsize,
    )


def _worldmap_from_directory(
    dirpath,
    metric,
    cmap,
    figsize,
    fontsize,
):
    return _worldmap_from_records(
        records=load_filtered_documents(dirpath),
        metric=metric,
        cmap=cmap,
        figsize=figsize,
        fontsize=fontsize,
    )


def worldmap(
    dirpath_or_records,
    metric="num_documents",
    cmap="Pastel2",
    figsize=(6, 6),
    fontsize=9,
):
    """Worldmap plot with the number of documents per country.

    Examples
    ----------------------------------------------------------------------------------------------

    >>> import pandas as pd
    >>> x = pd.Series(
    ...    data = [1000, 900, 800, 700, 600, 1000],
    ...    index = ["China", "Taiwan", "United States", "United Kingdom", "India", "Colombia"],
    ... )
    >>> x
    China             1000
    Taiwan             900
    United States      800
    United Kingdom     700
    India              600
    Colombia          1000
    dtype: int64

    >>> fig = worldmap(x, figsize=(15, 6))
    >>> fig.savefig('/workspaces/techminer/sphinx/images/worldmap.png')

    .. image:: images/worldmap.png
        :width: 2000px
        :align: center


    """
    if isinstance(dirpath_or_records, str):
        return _worldmap_from_directory(
            dirpath=dirpath_or_records,
            metric=metric,
            cmap=cmap,
            figsize=figsize,
            fontsize=fontsize,
        )
    elif isinstance(dirpath_or_records, pd.DataFrame):
        return _worldmap_from_records(
            records=dirpath_or_records,
            metric=metric,
            cmap=cmap,
            figsize=figsize,
            fontsize=fontsize,
        )
    else:
        raise TypeError("dirpath_or_records must be a string or a pandas.DataFrame")
