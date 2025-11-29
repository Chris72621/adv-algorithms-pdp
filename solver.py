# solver.py

from distance import total_distance
from feasibility import feasible
from route_ops import reverse_segment

def PDP_GREEDY_INSERT_2OPT(instance):
    """
    Implementation of:
    PDP-GREEDY-INSERT-2OPT(instance)
    """

    s = instance["s"]
    e = instance["e"]
    R = set(instance["R"])  # unserved requests

    # Initialize route
    if e is not None:
        route = [s, e]
    else:
        route = [s]

    unserved_requests = set(R)

    # ----- CONSTRUCTION PHASE -----
    # (we will fill this in after confirming structure)

    # ----- IMPROVEMENT PHASE (2-opt) -----
    # (we will fill this in next)

    return route
