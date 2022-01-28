#!/usr/bin/env python3

# Dictionary based completion is just search,
# meaning all we need is a list of words and a
# search algorithm.

from sys import argv
from english_words import english_words_set

# Returns a sorted list of elements of w
# that begin with s
def complete(s, w) -> list:
    p = []

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

w = list(english_words_set)
w.sort()

if __name__ == '__main__':
    if len(argv) == 1:
        exit(1)
    for s in complete(argv[1], w):
        print(s)
