from solver import PDP_GREEDY_INSERT_2OPT

def main():
    # Example placeholder instance structure
    # You will replace this with real data
    instance = {
        "s": 0,
        "e": None,
        "R": [],
        "pickup": {},
        "delivery": {},
        "V": [],
        "c": [],
        "T": [],
        "open": {},
        "close": {},
        "service": {},
        "paired_sets": []
    }

    result = PDP_GREEDY_INSERT_2OPT(instance)
    print("Result:", result)

if __name__ == "__main__":
    main()
