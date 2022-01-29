#!/usr/bin/env python3

# Dictionary based completion is just search,
# so all we need is a list of words and
# binary search.

# Returns a sorted list of elements of w
# that begin with s
def complete(s, d) -> list:
    p = []
    w = [t for t in d]

    end = len(w) - 1
    begin = 0

    while end >= begin:
        mid = int((begin + end) / 2)
        t = w[mid]

        if t.startswith(s):
            p.append(w.pop(mid))
            continue

        elif s < t:
            end = mid - 1
            continue

        begin = mid + 1

    p.sort(key=lambda s: len(s))

    return p
