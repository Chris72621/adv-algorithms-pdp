from solver import (
    PDP_GREEDY_INSERT_2OPT
)

def PDP_solver_trace(instance):
    print("\n=============================")
    print("      TRACE MODE ACTIVE")
    print("=============================\n")

    greedy, final = PDP_GREEDY_INSERT_2OPT(instance)

    print("\n=== TRACE SUMMARY ===")
    print("Greedy:", greedy)
    print("Final:", final)

    return greedy, final
