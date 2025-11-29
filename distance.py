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


def total_distance(route, c):
    """
    Compute total travel distance of a route.
    Direct translation of the pseudocode:
        sum of c[i][j] for all consecutive nodes (i, j)
    """
    total = 0

    for k in range(len(route) - 1):
        i = route[k]
        j = route[k + 1]
        total += c[i][j]

    return total
