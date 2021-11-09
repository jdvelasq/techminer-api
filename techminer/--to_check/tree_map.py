"""
Tree map
===============================================================================
"""

import textwrap

import matplotlib
import matplotlib.pyplot as plt
import squarify

TEXTLEN = 40


def tree_map(
    series,
    darkness=None,
    cmap="Greys",
    figsize=(6, 6),
    fontsize=11,
    alpha=0.9,
):
    """Creates a classification plot..

    Examples
    ----------------------------------------------------------------------------------------------

    >>> import pandas as pd
    >>> x = pd.Series(
    ...     [10, 5, 2, 1],
    ...     index = "author 3,author 1,author 0,author 2".split(","),
    ... )
    >>> x
    author 3    10
    author 1     5
    author 0     2
    author 2     1
    dtype: int64
    >>> fig = treemap(x)
    >>> fig.savefig('/workspaces/techminer/sphinx/images/treeplot.png')

    .. image:: images/treeplot.png
        :width: 400px
        :align: center


    """
    darkness = series if darkness is None else darkness

    matplotlib.rc("font", size=fontsize)
    fig = plt.Figure(figsize=figsize)
    ax = fig.subplots()
    cmap = plt.cm.get_cmap(cmap)

    labels = series.index
    labels = [textwrap.shorten(text=text, width=TEXTLEN) for text in labels]
    labels = [textwrap.wrap(text=text, width=15) for text in labels]
    labels = ["\n".join(text) for text in labels]

    colors = [
        cmap(0.4 + 0.6 * (d - darkness.min()) / (darkness.max() - darkness.min()))
        for d in darkness
    ]

    squarify.plot(
        sizes=series,
        label=labels,
        color=colors,
        alpha=alpha,
        ax=ax,
        pad=True,
        bar_kwargs={"edgecolor": "k", "linewidth": 0.5},
        text_kwargs={"color": "w", "fontsize": fontsize},
    )
    ax.axis("off")

    fig.set_tight_layout(True)

    return fig
