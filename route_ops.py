# route_ops.py

def reverse_segment(route, start, end):
    """
    Reverse the segment of the route between indices start and end (inclusive).
    """
    while start < end:
        route[start], route[end] = route[end], route[start]
        start += 1
        end -= 1
