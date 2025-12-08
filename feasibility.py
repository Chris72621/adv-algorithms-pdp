# ============================================================
# From "word doc pseudocode"
#
# FEASIBLE(route):
#     picked = empty set
#     time = 0
#
#     for k = 0 to length(route)-1:
#         i = route[k]
#
#         if k == 0:
#             if time < open[i]:
#                 time = open[i]
#         else:
#             prev = route[k-1]
#             time = time + s[prev] + T[prev][i]
#             if time < open[i]:
#                 time = open[i]
#
#         if time > close[i]:
#             return false
#
#         if i is pickup(r): picked.add(r)
#
#         if i is delivery(r):
#             if r not in picked: return false
#
#             for each pair {r1, r2} in S:
#                 if r in pair and other not in picked:
#                     return false
#
# return true
# ============================================================


def feasible(route, instance):
    """
    Check feasibility of a route under:
    - time windows
    - precedence (pickup-before-delivery)
    - paired-pickup constraints
    """

    pickup = instance["pickup"]
    delivery = instance["delivery"]
    paired_sets = instance["paired_sets"]

    # Fast reverse lookup: node -> request
    pickup_of = {pickup[r]: r for r in pickup}
    delivery_of = {delivery[r]: r for r in delivery}

    picked = set()
    time = 0

    # Build mapping from node id -> matrix index for distance/time matrices
    # Some instances use non-contiguous node IDs (e.g. V = [0,1,2,5,6,7,8])
    # while T/c are dense matrices indexed by position in V. Create a map
    # so we can safely index into those matrices.
    node_index = {v: idx for idx, v in enumerate(instance.get("V", []))}

    for k in range(len(route)):
        i = route[k]

        time = _update_time(k, route, time, instance, node_index)

        if not _check_time_window(i, time, instance):


            return False

        _mark_pickup(i, picked, pickup_of)

        if not _check_delivery(i, picked, delivery_of):


            return False

        if not _check_pairing(i, picked, paired_sets, delivery_of):
      

            return False
    
 

    return True




# ============================================================
# Helper 1: Time propagation through the route
# ============================================================

def _update_time(k, route, current_time, instance, node_index):
    """
    Updates global time as we move along the route.
    Implements:
        - travel time
        - service time
        - waiting for time windows to open
    """
    open_time = instance["open"]
    service = instance["service"]
    T = instance["T"]

    i = route[k]

    # If first node, align with opening time
    if k == 0:
        return max(current_time, open_time[i])

    # Otherwise add:
    #   - service time at previous node
    #   - travel time from prev to current
    prev = route[k - 1]

    # Map node ids to matrix indices for service/T lookups when necessary
    # service may be a dict keyed by node id; keep using that. T is a
    # dense matrix indexed by position in instance["V"], so convert.
    prev_idx = node_index.get(prev, prev)
    i_idx = node_index.get(i, i)

    updated_time = current_time + service[prev] + T[prev_idx][i_idx]

    # Wait for time window to open if early
    updated_time = max(updated_time, open_time[i])

    return updated_time



# ============================================================
# Helper 2: Time window validation
# ============================================================

def _check_time_window(i, time, instance):
    open_time = instance["open"]
    close_time = instance["close"]

    return time <= close_time[i]



# ============================================================
# Helper 3: Mark pickup(r) when we reach a pickup node
# ============================================================

def _mark_pickup(i, picked, pickup_of):
    if i in pickup_of:
        r = pickup_of[i]
        picked.add(r)



# ============================================================
# Helper 4: Delivery validation
# ============================================================

def _check_delivery(i, picked, delivery_of):
    """
    Check delivery feasibility:
    - delivery cannot occur before pickup
    """
    if i not in delivery_of:
        return True

    r = delivery_of[i]

    # Delivery before pickup → invalid
    return r in picked



# ============================================================
# Helper 5: Paired-pickup rule
# ============================================================

def _check_pairing(i, picked, paired_sets, delivery_of):
    """
    Both pickups of a paired set {r1, r2}
    must occur before either delivery.
    """
    if i not in delivery_of:
        return True

    r = delivery_of[i]

    for pair in paired_sets:
        if r in pair:
            # find the other request in the pair
            other = (pair - {r}).pop()
            if other not in picked:
                return False

    return True
