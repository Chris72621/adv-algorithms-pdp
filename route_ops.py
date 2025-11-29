# -------------------------------------------------------------
# From "word doc pseudocode"
#
# // Helper: Reverse the segment of the route between
# // indices 'start' and 'end' (inclusive)
#
# REVERSE_SEGMENT(route, start, end):
#     while start < end:
#         Temp = route[start]
#         route[start] = route[end]
#         route[end] = Temp
#
#         start = start + 1
#         end   = end - 1
# -------------------------------------------------------------


def reverse_segment(route, start, end):
    """
    Reverse the elements of 'route' between indices start and end (inclusive).
    This function modifies the list in-place.

    Direct translation of pseudocode:
        while start < end:
            swap(route[start], route[end])
            start += 1
            end   -= 1
    """
    while start < end:
        _swap(route, start, end)
        start += 1
        end -= 1


def _swap(lst, i, j):
    """
    Small helper to swap two elements in a list.
    """
    lst[i], lst[j] = lst[j], lst[i]
