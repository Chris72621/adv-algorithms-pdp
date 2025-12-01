# instance_input.py

# -------------------------------------------------------------
# From "word doc pseudocode"
#
# // instance = {s, e, R, V, c, T, open[], close[], s[], S}
#
# Inputs:
# • Start depot s (optional end depot e)
# • Set of requests R:
#     - For each request r: pickup node p(r) and delivery node d(r)
# • Node set V (includes depot(s), pickups, deliveries)
# • Travel distance c[i][j] and travel time T[i][j] for all i ≠ j in V
# • Service time s[i] and time windows [open[i], close[i]] at each node i
# • Set S of paired request sets {r1, r2} (“both pickups before either delivery”)
# -------------------------------------------------------------

def get_instance():
    """
    Returns an example instance structure.
    """

    instance = {
        "s": 0,                    # start depot
        "e": None,                # end depot (None means no return depot)

        # Set of requests
        "R": {1, 2},

        # For each request r: pickup node p(r) and delivery node d(r)
        "pickup":   {1: 1, 2: 2},
        "delivery": {1: 3, 2: 4},

        # Node set V
        "V": [0, 1, 2, 3, 4],

        # Travel distance c[i][j]
        "c": [
            [0, 2, 3, 6, 8],
            [2, 0, 4, 7, 3],
            [3, 4, 0, 5, 6],
            [6, 7, 5, 0, 2],
            [8, 3, 6, 2, 0]
        ],

        # Travel time T[i][j]
        "T": [
            [0, 2, 3, 6, 8],
            [2, 0, 4, 7, 3],
            [3, 4, 0, 5, 6],
            [6, 7, 5, 0, 2],
            [8, 3, 6, 2, 0]
        ],

        # Service time at each node
        "service": {i: 0 for i in [0, 1, 2, 3, 4]},

        # Time windows for each node
        "open":  {i: 0   for i in [0, 1, 2, 3, 4]},
        "close": {i: 100 for i in [0, 1, 2, 3, 4]},

        # Paired request sets S (empty for example)
        "paired_sets": []
    }

    return instance


# -------------------------------------------------------------
# INSTANCE 2: Two requests, tighter time windows
# -------------------------------------------------------------

def get_instance_tight_tw():
    """
    Instance with time window pressure.
    Forces route planning around arrival times.
    """

    instance = {
        "s": 0,
        "e": None,

        "R": {1, 2},
        "pickup":   {1: 1, 2: 2},
        "delivery": {1: 3, 2: 4},

        "V": [0, 1, 2, 3, 4],

        "c": [
            [0, 1, 4, 7, 8],
            [1, 0, 3, 6, 7],
            [4, 3, 0, 2, 5],
            [7, 6, 2, 0, 3],
            [8, 7, 5, 3, 0]
        ],

        "T": [
            [0, 1, 4, 7, 8],
            [1, 0, 3, 6, 7],
            [4, 3, 0, 2, 5],
            [7, 6, 2, 0, 3],
            [8, 7, 5, 3, 0]
        ],

        "service": {i: 0 for i in range(5)},

        # Tight time windows: must reach p1 and p2 early
        "open":  {0: 0, 1: 0, 2: 0, 3: 5, 4: 10},
        "close": {0: 100, 1: 5, 2: 5, 3: 25, 4: 30},

        "paired_sets": []
    }

    return instance



# -------------------------------------------------------------
# INSTANCE 3: Three requests w/ paired constraint {1,2}
# -------------------------------------------------------------

def get_instance_with_pairing():
    """
    Instance with 3 requests and a paired constraint:
    For pair {1,2} → both pickups must happen before either delivery.
    """

    instance = {
        "s": 0,
        "e": None,

        "R": {1, 2, 3},

        "pickup":   {1: 1, 2: 2, 3: 5},
        "delivery": {1: 6, 2: 7, 3: 8},

        "V": [0, 1, 2, 5, 6, 7, 8],

        # Distance matrix (7x7)
        "c": [
            [0, 2, 3, 4, 6, 8, 9],
            [2, 0, 1, 3, 5, 7, 9],
            [3, 1, 0, 2, 4, 6, 8],
            [4, 3, 2, 0, 3, 5, 7],
            [6, 5, 4, 3, 0, 2, 4],
            [8, 7, 6, 5, 2, 0, 3],
            [9, 9, 8, 7, 4, 3, 0]
        ],

        "T": [
            [0, 2, 3, 4, 6, 8, 9],
            [2, 0, 1, 3, 5, 7, 9],
            [3, 1, 0, 2, 4, 6, 8],
            [4, 3, 2, 0, 3, 5, 7],
            [6, 5, 4, 3, 0, 2, 4],
            [8, 7, 6, 5, 2, 0, 3],
            [9, 9, 8, 7, 4, 3, 0]
        ],

        "service": {i: 0 for i in [0,1,2,5,6,7,8]},

        "open":  {i: 0 for i in [0,1,2,5,6,7,8]},
        "close": {i: 100 for i in [0,1,2,5,6,7,8]},

        # Paired requirement: pickups 1 and 2 must happen before either delivery 6 or 7
        "paired_sets": [
            {1, 2}
        ]
    }

    return instance


# -------------------------------------------------------------
# EASY PAIRING INSTANCE: Greedy should find a solution
# -------------------------------------------------------------
def get_instance_pairing_hard():
    """
    Very small instance where requests 1 and 2 are paired
    and the greedy insertion should succeed.
    """

    # Harder pairing instance:
    # - Three requests, paired set {1,2} requires pickups 1 and 2 before either delivery
    # - Tight time windows force pickups to be early and deliveries later
    # - Non-trivial distance/time matrix
    instance = {
        "s": 0,
        "e": None,

        "R": {1, 2, 3},

        "pickup":   {1: 1, 2: 2, 3: 3},
        "delivery": {1: 4, 2: 5, 3: 6},

        # Node ordering matches rows/cols of c/T
        "V": [0, 1, 2, 3, 4, 5, 6],

        # Distance matrix (7x7)
        "c": [
            [0, 2, 3, 4, 8, 9, 7],
            [2, 0, 1, 3, 6, 7, 5],
            [3, 1, 0, 2, 7, 8, 6],
            [4, 3, 2, 0, 5, 6, 4],
            [8, 6, 7, 5, 0, 1, 3],
            [9, 7, 8, 6, 1, 0, 2],
            [7, 5, 6, 4, 3, 2, 0],
        ],

        "T": [
            [0, 2, 3, 4, 8, 9, 7],
            [2, 0, 1, 3, 6, 7, 5],
            [3, 1, 0, 2, 7, 8, 6],
            [4, 3, 2, 0, 5, 6, 4],
            [8, 6, 7, 5, 0, 1, 3],
            [9, 7, 8, 6, 1, 0, 2],
            [7, 5, 6, 4, 3, 2, 0],
        ],

        "service": {i: 0 for i in [0,1,2,3,4,5,6]},

        # Time windows: pickups must occur early; deliveries open later
        "open":  {0: 0, 1: 0, 2: 0, 3: 0, 4: 8, 5: 8, 6: 10},
        "close": {0: 100, 1: 5, 2: 5, 3: 6, 4: 30, 5: 30, 6: 40},

        # Paired requirement: pickups 1 and 2 must both occur before either delivery 4 or 5
        "paired_sets": [{1, 2}]
    }

    return instance