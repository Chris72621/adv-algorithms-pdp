from distance import total_distance
from feasibility import feasible
from route_ops import reverse_segment

# =====================================================================
# PDP-GREEDY-INSERT-2OPT (main solver)
# =====================================================================

def PDP_GREEDY_INSERT_2OPT(instance):
    """
    Main solver that coordinates:
    1. Initialization
    2. Construction Phase (Greedy Feasible Insertion)
    3. Improvement Phase (2-Opt)
    """

    # ---- Phase 1: Initialization ----
    route, unserved_requests = _initialize_route(instance)

    # ---- Phase 2: Greedy Construction ----
    route_after_greedy = _construction_phase(route, unserved_requests, instance)
 
    # ---- If infeasible, stop ----
    if isinstance(route_after_greedy, str):
        return None, route_after_greedy

    # ---- Phase 3: 2-Opt Improvement ----
    route_final = _two_opt_phase(route_after_greedy, instance)


    # Return final improved route
    return route_after_greedy, route_final


# =====================================================================
# PHASE 1: INITIALIZATION
# =====================================================================

# -------------------------------------------------------------
# From "word doc pseudocode"
#
# // Initialize route with depot(s)
#     if end depot e is required:
#         route = [s, e]
#     else:
#         route = [s]
#
#     unserved_requests = R
# -------------------------------------------------------------

def _initialize_route(instance):
    s = instance["s"]
    e = instance["e"]
    R = instance["R"]

    # If an end depot is required (e is not None)
    if e is not None:
        route = [s, e]
    else:
        route = [s]

    # Requests not yet inserted into the route
    unserved_requests = set(R)

    return route, unserved_requests


# =====================================================================
# PHASE 2: CONSTRUCTION (GREEDY FEASIBLE INSERTION)
# =====================================================================

# -------------------------------------------------------------
# From "word doc pseudocode"
#
# /* CONSTRUCTION PHASE: Greedy feasible insertion
#  * Selection criterion:
#  *     At each iteration, choose the pickup-delivery request
#  *     whose best feasible insertion produces the smallest
#  *     increase in total travel distance.
#  */
#
# while unserved_requests is not empty:
#     best_route_global = null
#     best_delta_global = +infinity
#     best_request = null
#
#     for each request r in unserved_requests:
#         best_route_for_r = null
#         best_delta_for_r = +infinity
#
#         for posP = 0 to length(route) - 1:
#             for posD = posP + 1 to length(route):
#
#                 trial_route = COPY(route)
#                 insert p(r) after posP
#                 insert d(r) after posD
#
#                 if FEASIBLE(trial_route):
#                     compute delta cost
#                     update best_route_for_r
#
#     if best_route_global is null:
#         return "instance infeasible"
#
#     route = best_route_global
#     remove best_request from unserved_requests
#
# -------------------------------------------------------------

def _construction_phase(route, unserved_requests, instance):

    pickup = instance["pickup"]
    delivery = instance["delivery"]

    # Track requests whose pickup still needs insertion, and those whose
    # pickup was inserted but delivery still pending.
    remaining_pickups = set(unserved_requests)
    pending_deliveries = set()

    # Continue until all pickups inserted and all deliveries placed
    while len(remaining_pickups) > 0 or len(pending_deliveries) > 0:

        best_route_global = None
        best_delta_global = float("inf")
        best_action = None  # tuple (type, r)

        base_cost = total_distance(route, instance["c"], instance.get("V"))

        # 1) Consider inserting pickups (either with delivery or pickup-only)
        for r in list(remaining_pickups):
            p_node = pickup[r]
            d_node = delivery[r]

            # Try full insertion (pickup + delivery)
            for posP in range(len(route)):
                for posD in range(posP + 1, len(route) + 1):
                    trial_route = route.copy()
                    trial_route.insert(posP + 1, p_node)
                    trial_route.insert(posD + 1, d_node)

                    if feasible(trial_route, instance):
                        new_cost = total_distance(trial_route, instance["c"], instance.get("V"))
                        delta = new_cost - base_cost
                        if delta < best_delta_global:
                            best_delta_global = delta
                            best_route_global = trial_route
                            best_action = ("full", r)

            # Try pickup-only insertion (defer delivery)
            for posP in range(len(route)):
                trial_route = route.copy()
                trial_route.insert(posP + 1, p_node)

                if feasible(trial_route, instance):
                    new_cost = total_distance(trial_route, instance["c"], instance.get("V"))
                    delta = new_cost - base_cost
                    if delta < best_delta_global:
                        best_delta_global = delta
                        best_route_global = trial_route
                        best_action = ("pickup_only", r)

        # 2) Consider inserting pending deliveries (for requests whose pickup is already in route)
        for r in list(pending_deliveries):
            d_node = delivery[r]

            for posD in range(len(route) + 1):
                trial_route = route.copy()
                # Insert delivery AFTER posD (posD may be len(route) to insert at end)
                trial_route.insert(posD + 1, d_node)

                if feasible(trial_route, instance):
                    new_cost = total_distance(trial_route, instance["c"], instance.get("V"))
                    delta = new_cost - base_cost
                    if delta < best_delta_global:
                        best_delta_global = delta
                        best_route_global = trial_route
                        best_action = ("delivery_only", r)

        # If no feasible move anywhere → infeasible instance
        if best_route_global is None:
            return "instance infeasible (no feasible insertion found)"

        # Accept global best insertion and update sets
        route = best_route_global
        action_type, action_r = best_action

        if action_type == "full":
            # pickup+delivery inserted; remove from remaining_pickups
            if action_r in remaining_pickups:
                remaining_pickups.remove(action_r)
            # ensure it's not pending
            pending_deliveries.discard(action_r)

        elif action_type == "pickup_only":
            # pickup inserted now delivery pending
            remaining_pickups.remove(action_r)
            pending_deliveries.add(action_r)

        elif action_type == "delivery_only":
            # delivery inserted; remove from pending
            pending_deliveries.remove(action_r)

    return route



# =====================================================================
# PHASE 3: IMPROVEMENT (2-OPT LOCAL SEARCH)
# =====================================================================

# -------------------------------------------------------------
# From "word doc pseudocode"
#
# /* IMPROVEMENT PHASE: 2-opt local search
#  * Reverse route segments to eliminate crossings.
#  */
#
# improved = true
# while improved:
#     improved = false
#     current_cost = TOTAL_DISTANCE(route)
#
#     for i = 0 to len(route)-3:
#         for j = i+2 to len(route)-2:
#
#             trial_route = COPY(route)
#             REVERSE_SEGMENT(trial_route, i+1, j)
#
#             if FEASIBLE(trial_route):
#                 new_cost = TOTAL_DISTANCE(trial_route)
#                 if new_cost < current_cost:
#                     route = trial_route
#                     improved = true
#                     break both loops
#
# return route
# -------------------------------------------------------------

def _two_opt_phase(route, instance):

    c = instance["c"]

    improved = True

    while improved:
        improved = False
        current_cost = total_distance(route, c, instance.get("V"))

        # Try all edge pairs (i, i+1) and (j, j+1)
        for i in range(len(route) - 3):
            for j in range(i + 2, len(route) - 1):

                trial_route = route.copy()

                # Reverse middle segment (i+1 ... j)
                reverse_segment(trial_route, i + 1, j)

                # Only keep moves that remain feasible
                if feasible(trial_route, instance):
                    new_cost = total_distance(trial_route, c, instance.get("V"))

                    if new_cost < current_cost:
                        route = trial_route
                        improved = True
                        break

            if improved:
                break

    return route
