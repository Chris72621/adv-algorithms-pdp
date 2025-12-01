# -------------------------------------------------------------
# From "word doc pseudocode"
#
# // Helper: Total travel distance of a route
# TOTAL_DISTANCE(route):
#     total = 0
#
#     for k = 0 to length(route) - 2:
#         i = route[k]
#         j = route[k + 1]
#         total = total + c[i][j]
#
#     return total
# -------------------------------------------------------------


def total_distance(route, c, V=None):
    """
    Compute total travel distance of a route.
    Direct translation of the pseudocode:
        sum of c[i][j] for all consecutive nodes (i, j)
    """
    total = 0

    # If a node list V is provided, c is a dense matrix indexed by the
    # position of each node in V. Build a mapping from node id -> index.
    node_index = None
    if V is not None:
        node_index = {v: idx for idx, v in enumerate(V)}

    for k in range(len(route) - 1):
        i = route[k]
        j = route[k + 1]

        if node_index is not None:
            i_idx = node_index.get(i, i)
            j_idx = node_index.get(j, j)
            total += c[i_idx][j_idx]
        else:
            total += c[i][j]

    return total
