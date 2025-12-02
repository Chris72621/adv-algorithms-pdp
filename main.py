# -------------------------------------------------------------
# From "word doc pseudocode"
#
# Output:
# • A feasible route that:
#       - starts at s
#       - visits all pickups and deliveries
#       - returns to e if required
#       - respects precedence constraints
#       - respects pairing constraints
#       - satisfies all time windows
#   OR
# • A fail message: "instance infeasible"
# -------------------------------------------------------------
from solver import PDP_GREEDY_INSERT_2OPT
from instance_input import (
    get_instance,
    get_instance_tight_tw,
    get_instance_with_pairing,
    get_instance_pairing_hard,
    get_instance_multi_same_delivery,
    get_instance_large,
    get_instance_complex_tw_pairing,
    get_instance_infeasible,
)
import time

# -------------------------------------------------------------
# Convert final route into dictionary form:
# {
#     1: (pickup_node, delivery_node),
#     2: (pickup_node, delivery_node),
#     ...
# }
# -------------------------------------------------------------
def route_to_dictionary(route, instance):
    """
    Converts the final route list into a dictionary of the order in which
    requests were served.

    Example:
        route = [0, 2, 1, 4, 3]
        → {1: (2, 4), 2: (1, 3)}
    """

    pickup = instance["pickup"]
    delivery = instance["delivery"]

 
    pickup_of = {pickup[r]: r for r in pickup}
    delivery_of = {delivery[r]: r for r in delivery}

    served = []      # store tuples of (r, pickup_node, delivery_node)
    active = {}      # store currently active pickups

    for node in route:
        if node in pickup_of:
            r = pickup_of[node]
            active[r] = {"pickup": node}

        if node in delivery_of:
            r = delivery_of[node]
            if r in active:
                active[r]["delivery"] = node
                served.append((r, active[r]["pickup"], active[r]["delivery"]))
                del active[r]

    # Build final dictionary
    order_dict = {}
    for idx, (r, p, d) in enumerate(served, start=1):
        order_dict[idx] = (p, d)

    return order_dict


# MAIN SCRIPT
def main():

    # Load all test instances
    instance_basic = get_instance()
    instance_tw = get_instance_tight_tw()
    instance_pair = get_instance_with_pairing()
    instance_pair_hard = get_instance_pairing_hard()
    instance_multi_same_delivery = get_instance_multi_same_delivery()

    # New instances
    instance_large = get_instance_large()
    instance_complex = get_instance_complex_tw_pairing()
    instance_infeasible = get_instance_infeasible()

    # ---------------------------------------------------------------------
    # BASIC INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_basic)
    end = time.time()
    print("\n===== BASIC INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_basic))

    # ---------------------------------------------------------------------
    # TIGHT TIME WINDOW INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_tw)
    end = time.time()
    print("\n===== TIGHT TIME WINDOW INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_tw))

    # ---------------------------------------------------------------------
    # PAIRING INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_pair)
    end = time.time()
    print("\n===== PAIRING INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_pair))

    # ---------------------------------------------------------------------
    # HARD PAIRING + TW INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_pair_hard)
    end = time.time()
    print("\n===== HARD PAIRING + TW INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_pair_hard))

    # ---------------------------------------------------------------------
    # MULTIPLE REQUESTS SAME DELIVERY NODE - FAIL
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_multi_same_delivery)
    end = time.time()
    print("\n===== MULTIPLE REQUESTS SAME DELIVERY NODE - FAIL LOOK AT OUTPUT =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_multi_same_delivery))

    # ---------------------------------------------------------------------
    # LARGE INSTANCE (performance stress test)
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_large)
    end = time.time()
    print("\n===== LARGE COMPLEX INSTANCE (10 Requests) =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_large))

    # ---------------------------------------------------------------------
    # COMPLEX TW + PAIRING INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_complex)
    end = time.time()
    print("\n===== COMPLEX TIME WINDOWS + PAIRING INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Route after greedy construction:", greedy)
    print("Raw Route (after 2-opt):", final)
    print("Order:", route_to_dictionary(final, instance_complex))

    # ---------------------------------------------------------------------
    # INFEASIBLE INSTANCE
    # ---------------------------------------------------------------------
    start = time.time()
    result = PDP_GREEDY_INSERT_2OPT(instance_infeasible)
    end = time.time()
    print("\n===== INFEASIBLE INSTANCE =====")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Result:", result)

if __name__ == "__main__":
    main()
