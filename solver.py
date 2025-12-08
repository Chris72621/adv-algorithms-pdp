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

    # If an end depot is required
    if e is not None:
        route = [s, e]
    else:
        route = [s]

    # Requests not yet inserted
    unserved_requests = set(R)

    print("\n=== TRACE: Initialization ===")
    print("Initial route:", route)
    print("Unserved requests:", unserved_requests)

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

    print("\n=== TRACE: Starting Greedy Construction Phase ===")

    pickup = instance["pickup"]
    delivery = instance["delivery"]

    remaining_pickups = set(unserved_requests)
    pending_deliveries = set()

    while len(remaining_pickups) > 0 or len(pending_deliveries) > 0:

        # --- SLIDE PRINTS ---
        print("\n--- Greedy Iteration ---")
        print("Current route:", route)
        print("Unserved requests:", remaining_pickups | pending_deliveries)
        # ---------------------

        best_route_global = None
        best_delta_global = float("inf")
        best_action = None

        base_cost = total_distance(route, instance["c"], instance.get("V"))

        # ------------------------------------------------------------
        # TEST PICKUPS
        # ------------------------------------------------------------
        for r in list(remaining_pickups):
            p_node = pickup[r]
            d_node = delivery[r]

            # Full insertion
            for posP in range(len(route)):
                for posD in range(posP + 1, len(route) + 1):
                    trial = route.copy()
                    trial.insert(posP + 1, p_node)
                    trial.insert(posD + 1, d_node)

                    if feasible(trial, instance):
                        delta = total_distance(trial, instance["c"], instance.get("V")) - base_cost
                        if delta < best_delta_global:
                            best_delta_global = delta
                            best_route_global = trial
                            best_action = ("full", r)

            # Pickup-only
            for posP in range(len(route)):
                trial = route.copy()
                trial.insert(posP + 1, p_node)

                if feasible(trial, instance):
                    delta = total_distance(trial, instance["c"], instance.get("V")) - base_cost
                    if delta < best_delta_global:
                        best_delta_global = delta
                        best_route_global = trial
                        best_action = ("pickup_only", r)

        # ------------------------------------------------------------
        # TEST DELIVERIES
        # ------------------------------------------------------------
        for r in list(pending_deliveries):
            d_node = delivery[r]

            for posD in range(len(route) + 1):
                trial = route.copy()
                trial.insert(posD + 1, d_node)

                if feasible(trial, instance):
                    delta = total_distance(trial, instance["c"], instance.get("V")) - base_cost
                    if delta < best_delta_global:
                        best_delta_global = delta
                        best_route_global = trial
                        best_action = ("delivery_only", r)

        # No feasible insertion anywhere → infeasible
        if best_route_global is None:
            print("No feasible insertion found → instance infeasible")
            return "instance infeasible (no feasible insertion found)"

        # --- SLIDE PRINT ---
        print(f"Chosen insertion: {best_action}  |  Δcost = {best_delta_global:.3f}")
        # -------------------

        # Accept chosen insertion
        route = best_route_global
        action_type, action_r = best_action

        if action_type == "full":
            remaining_pickups.discard(action_r)
            pending_deliveries.discard(action_r)

        elif action_type == "pickup_only":
            remaining_pickups.remove(action_r)
            pending_deliveries.add(action_r)

        elif action_type == "delivery_only":
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
    print("\n=== TRACE: Starting 2-Opt Improvement Phase ===")
    print("Initial route:", route)

    c = instance["c"]
    improved = True

    while improved:
        improved = False
        current_cost = total_distance(route, c, instance.get("V"))

        for i in range(len(route) - 3):
            for j in range(i + 2, len(route) - 1):

                trial = route.copy()
                reverse_segment(trial, i + 1, j)

                if feasible(trial, instance):
                    new_cost = total_distance(trial, c, instance.get("V"))

                    if new_cost < current_cost:
                        print(f"Improvement accepted: reverse {i+1}..{j}  → Δ = {current_cost - new_cost:.3f}")
                        route = trial
                        improved = True
                        break
            if improved:
                break

    print("=== TRACE: 2-Opt Complete ===")
    print("Final improved route:", route)

    return route
