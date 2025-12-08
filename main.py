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

    # ------------------------------
    # Load the instance
    # ------------------------------
    instance_basic = get_instance()

    # ------------------------------
    # SLIDE 1: Algorithm Inputs
    # ------------------------------
    print("\n=== INPUT INSTANCE ===")
    print("Start depot:", instance_basic["s"])
    print("End depot:", instance_basic["e"])

    print("Requests (R):", instance_basic["R"])
    print("Pickup nodes:", instance_basic["pickup"])
    print("Delivery nodes:", instance_basic["delivery"])

    print("Node set V:", instance_basic["V"])

    print("Time windows:", {
        i: (instance_basic["open"][i], instance_basic["close"][i])
        for i in instance_basic["V"]
    })

    print("Paired sets:", instance_basic["paired_sets"])


    # ------------------------------
    # Call solver
    # ------------------------------
    start = time.time()
    greedy, final = PDP_GREEDY_INSERT_2OPT(instance_basic)
    end = time.time()

    # ------------------------------
    # SLIDE 5: Final Output
    # ------------------------------
    print("\n=== FINAL OUTPUT ===")
    print(f"Runtime: {end - start:.6f} seconds")

    print("Route after greedy (before 2-opt):", greedy)
    print("Route after 2-opt:", final)

    print("Order (pickup→delivery pairs):")
    print(route_to_dictionary(final, instance_basic))

if __name__ == "__main__":
    main()
