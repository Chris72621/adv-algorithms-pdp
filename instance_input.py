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


# -------------------------------------------------------------
# MULTIPLE REQUESTS → SAME DELIVERY NODE
# This instance tests:
#   • multiple requests delivering to the SAME node
#   • time windows forcing different pickup times
#   • solver handling shared delivery feasibility
# -------------------------------------------------------------
def get_instance_multi_same_delivery():
    """
    Multiple requests share the SAME delivery node, but time windows
    force them to arrive at different times.
    """

    # Requests:
    # r1: pickup=1 → delivery=5
    # r2: pickup=2 → delivery=5
    # r3: pickup=3 → delivery=5

    instance = {
        "s": 0,
        "e": None,

        "R": {1, 2, 3},

        "pickup":   {1: 1, 2: 2, 3: 3},
        "delivery": {1: 5, 2: 5, 3: 5},   # ALL requests deliver to SAME node 5

        "V": [0, 1, 2, 3, 5],

        # Distance matrix
        "c": [
            [0, 2, 4, 6, 10],
            [2, 0, 3, 4,  8],
            [4, 3, 0, 2,  6],
            [6, 4, 2, 0,  4],
            [10,8, 6, 4,  0]
        ],

        "T": [
            [0, 2, 4, 6, 10],
            [2, 0, 3, 4,  8],
            [4, 3, 0, 2,  6],
            [6, 4, 2, 0,  4],
            [10,8, 6, 4,  0]
        ],

        "service": {i: 0 for i in [0,1,2,3,5]},

        # Time windows enforce different pickup times & delayed delivery
        "open":  {
            0: 0,
            1: 0,   # r1 pickup
            2: 3,   # must pick up r2 later
            3: 6,   # r3 pickup latest
            5: 8    # delivery node opens AFTER all pickups are possible
        },
        "close": {
            0: 100,
            1: 5,   # ensures solver visits pickup 1 early
            2: 8,
            3: 12,
            5: 25   # delivery must be between t=8 and t=25
        },

        "paired_sets": []
    }

    return instance


# -------------------------------------------------------------
# LARGE INSTANCE: 10 requests, mixed constraints, runtime test
# -------------------------------------------------------------
def get_instance_large():
    """
    Large stress-test instance:
    10 requests, time windows, some pairing constraints.
    Designed to observe O(n^3) runtime behavior.
    """

    # 10 requests → 10 pickups (1–10), 10 deliveries (11–20)
    R = set(range(1, 11))
    pickup = {r: r for r in R}
    delivery = {r: r + 10 for r in R}

    # Node set
    V = [0] + list(pickup.values()) + list(delivery.values())  # depot + pickups + deliveries

    # Distance matrix (all distances 1–20)
    size = len(V)
    c = [[abs(i - j) + 1 for j in range(size)] for i in range(size)]
    T = c  # Same for travel time

    # Service time
    service = {v: 0 for v in V}

    # Time windows: pickups early, deliveries later
    open_tw = {}
    close_tw = {}

    for r in R:
        # pickups allowed early
        open_tw[pickup[r]] = 0
        close_tw[pickup[r]] = 20

        # deliveries must be later
        open_tw[delivery[r]] = 15
        close_tw[delivery[r]] = 100

    # depot
    open_tw[0] = 0
    close_tw[0] = 999

    # Pairing constraints: group them
    paired_sets = [
        {1, 2},
        {3, 4, 5},   # triple-pairing: all pickups before any delivery
        {6, 7},
        {8, 9, 10}
    ]

    return {
        "s": 0,
        "e": None,
        "R": R,
        "pickup": pickup,
        "delivery": delivery,
        "V": V,
        "c": c,
        "T": T,
        "service": service,
        "open": open_tw,
        "close": close_tw,
        "paired_sets": paired_sets
    }

# -------------------------------------------------------------
# COMPLEX TIME WINDOWS + PAIRING (Feasible Hard Case)
# -------------------------------------------------------------
def get_instance_complex_tw_pairing():
    """
    Hard feasible instance:
    Tight time windows, combined pairing constraints,
    requires careful ordering.
    """

    R = {1, 2, 3, 4}

    pickup = {1: 1, 2: 2, 3: 3, 4: 4}
    delivery = {1: 10, 2: 11, 3: 12, 4: 13}

    V = [0, 1, 2, 3, 4, 10, 11, 12, 13]

    # Distances
    c = [
        [0, 2, 3, 4, 5, 8, 9, 10, 12],
        [2, 0, 1, 2, 3, 7, 8,  9, 10],
        [3, 1, 0, 2, 3, 9, 6,  7, 10],
        [4, 2, 2, 0, 1, 6, 7,  8,  9],
        [5, 3, 3, 1, 0, 4, 5,  6,  7],
        [8, 7, 9, 6, 4, 0, 2,  3,  5],
        [9, 8, 6, 7, 5, 2, 0,  1,  2],
        [10,9, 7, 8, 6, 3, 1,  0,  2],
        [12,10,10,9,7,5,2,  2,  0]
    ]

    T = c

    service = {v: 0 for v in V}

    # Tight, staggered pickups
    open_tw = {
        0: 0,
        1: 0,   2: 3,   3: 6,   4: 10,
        10: 12, 11: 15, 12: 18, 13: 22
    }
    close_tw = {
        0: 999,
        1: 4,   2: 7,   3: 12,  4: 16,
        10: 25, 11: 28, 12: 32, 13: 35
    }

    # Pairing rules
    paired_sets = [
        {1, 2},   # both pickups first
        {3, 4}
    ]

    return {
        "s": 0,
        "e": None,
        "R": R,
        "pickup": pickup,
        "delivery": delivery,
        "V": V,
        "c": c,
        "T": T,
        "service": service,
        "open": open_tw,
        "close": close_tw,
        "paired_sets": paired_sets
    }


# -------------------------------------------------------------
# INFEASIBLE INSTANCE (Impossible Time Windows)
# -------------------------------------------------------------
def get_instance_infeasible():
    """
    Infeasible test case:
    Delivery time window opens BEFORE pickup window.
    The solver should correctly return 'instance infeasible'.
    """

    R = {1, 2}

    pickup = {1: 1, 2: 2}
    delivery = {1: 5, 2: 6}

    V = [0, 1, 2, 5, 6]

    c = [
        [0, 1, 2, 5, 6],
        [1, 0, 1, 4, 5],
        [2, 1, 0, 4, 4],
        [5, 4, 4, 0, 1],
        [6, 5, 4, 1, 0]
    ]

    T = c
    service = {v: 0 for v in V}

    # INFEASIBLE: deliveries open BEFORE pickups
    open_tw = {
        0: 0,
        1: 10,  # pickup 1 opens at 10
        2: 12,  # pickup 2 opens at 12
        5: 0,   # delivery opens at 0 (impossible)
        6: 0
    }
    close_tw = {
        0: 100,
        1: 15,
        2: 16,
        5: 2,   # must deliver BEFORE pickup opens
        6: 2
    }

    paired_sets = []

    return {
        "s": 0,
        "e": None,
        "R": R,
        "pickup": pickup,
        "delivery": delivery,
        "V": V,
        "c": c,
        "T": T,
        "service": service,
        "open": open_tw,
        "close": close_tw,
        "paired_sets": paired_sets
    }
