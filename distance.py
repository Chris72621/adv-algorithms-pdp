# distance.py

def total_distance(route, c):
    """
    Compute total travel distance of a route.
    route : list of node IDs
    c     : distance matrix, c[i][j]
    """
    total = 0
    for k in range(len(route) - 1):
        i = route[k]
        j = route[k + 1]
        total += c[i][j]
    return total
