#!/usr/bin/env python3

import sys
from english_words import english_words_set
import simple, markov

dictionary = sorted(english_words_set)
complete = simple.complete

if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
        exit(1)

    s = sys.argv[1].split().pop()

    for w in complete(s, dictionary):
        print(w)
