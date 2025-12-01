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
from instance_input import get_instance, get_instance_tight_tw, get_instance_with_pairing, get_instance_pairing_easy


def main():
    # Load instance from separate file
    instance = get_instance()
    instanceTimeWindow = get_instance_tight_tw()
    instancePairing = get_instance_with_pairing()
    instanceEasyPairing = get_instance_pairing_easy()


    # Run the solver
    result = PDP_GREEDY_INSERT_2OPT(instance)
    resultTimeWindow = PDP_GREEDY_INSERT_2OPT(instanceTimeWindow)
    resultPairing = PDP_GREEDY_INSERT_2OPT(instancePairing)
    resultEasyPairing = PDP_GREEDY_INSERT_2OPT(instanceEasyPairing)

    # Print the resulting route or infeasibility message
    print("Result:", result)
    print("ResultTW:", resultTimeWindow)
    print("ResultP:", resultPairing)
    print("ResultEP:", resultEasyPairing)


if __name__ == "__main__":
    main()
