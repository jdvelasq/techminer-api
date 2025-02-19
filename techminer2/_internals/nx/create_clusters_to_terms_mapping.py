# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements


def internal__create_clusters_to_terms_mapping(
    params,
    nx_graph,
):
    """Gets communities from a networkx graph as a dictionary."""

    # term_counters = params.term_counters

    mapping = {}

    for node, data in nx_graph.nodes(data=True):
        cluster = data["group"]
        if cluster not in mapping:
            mapping[cluster] = []
        # if term_counters is False:
        #     node = " ".join(node.split(" ")[:-1])
        mapping[cluster].append(node)

    return mapping
