# feasibility.py

def feasible(route, instance):
    """
    Feasibility check:
    - time windows
    - precedence (pickup before delivery)
    - pairing: both pickups before either delivery
    """
    open_time = instance["open"]
    close_time = instance["close"]
    service = instance["service"]
    T = instance["T"]
    pickup = instance["pickup"]
    delivery = instance["delivery"]
    paired_sets = instance["paired_sets"]

    picked = set()
    time = 0

    for k in range(len(route)):
        i = route[k]

        if k == 0:
            if time < open_time[i]:
                time = open_time[i]
        else:
            prev = route[k - 1]
            time = time + service[prev] + T[prev][i]

            if time < open_time[i]:
                time = open_time[i]

        if time > close_time[i]:
            return False

        # Check if pickup
        for r in pickup:
            if i == pickup[r]:
                picked.add(r)

        # Check if delivery
        for r in delivery:
            if i == delivery[r]:

                # Precedence: pickup must be visited first
                if r not in picked:
                    return False

                # Pairing: both pickups before either delivery
                for pair in paired_sets:
                    if r in pair:
                        other = list(pair - {r})[0]
                        if other not in picked:
                            return False

    return True
