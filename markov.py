#!/usr/bin/env python3

import numpy as np
import sys
import string
from english_words import english_words_set

exclude = "!\"#$%\&()*+,-./:;<=>?@[\\]^_`{|}~“”" + string.digits


class Model:
    def __init__(self):
        self.lexicon = {}
        self.weights = np.empty(0)

    def __lex__(self, data):
        i = 0
        for line in data:
            line = line.translate(str.maketrans('', '', exclude)).rstrip().split()
            for w in line:
                if self.lexicon.get(w) == None:
                    self.lexicon[w] = i
                    i += 1

        data.seek(0)
        
        return True
        

    def Train(self, file):
        try:
            data = open(file, 'r')
        except FileNotFoundError:
            print(f"error: {file}: no such file", file=sys.stderr)
            return False

        # generate lexicon from file
        self.__lex__(data)
        
        n = len(self.lexicon)

        self.weights = np.zeros((n, n))

        # load raw data
        for line in data:
            line = line.translate(str.maketrans('', '', exclude)).rstrip().split()
    
            for i,_ in enumerate(line[:-1]):
                s = line[i]
                t = line[i + 1]
                try:
                    row = self.lexicon[s]
                    col = self.lexicon[t]
                except KeyError:
                    continue
                self.weights[row][col] += 1

        # adjust probabilities
        rsum = self.weights.sum(axis=1).reshape((-1, 1)) # sum each row in raw
        scale = np.vectorize(lambda i : i if i == 0 else 1 / i)
        self.weights *= scale(rsum)

        data.close()
        return True

    def __suggest__(self, w : str):
        index = self.lexicon[w]
        t = self.weights[index]
        nz = np.nonzero(t)[0]
        u = nz[np.argsort(t[nz])[::-1]]
        keys = list(self.lexicon.keys())
        suggest = [keys[i] for i in u]
        return suggest

    # partial completion based on suggested words
    def __partial__(self, w : str, p : str):
        suggest = self.__suggest__(w)
        partial = list(filter(lambda s: s.startswith(p), suggest))
        return partial

    def Run(self, s : str) -> bool:
        if self.weights.size == 0:
            print("error: train model before running", file=sys.stderr)
            return False

        if not s:
            return False

        s = s.translate(str.maketrans('', '', exclude)).strip().split()
        word = s[-1]

        if word not in self.lexicon:
            if len(s) == 1:
                print("No suggestions :(", file=sys.stderr)
                return False
            else:
                word = s[-2]
                part = s[-1]
                possible = self.__partial__(word, part)
        else:
            possible = self.__suggest__(word)

        if not possible:
            print("No suggestions :(", file=sys.stderr)
            return False

        for i,w in enumerate(possible):
            print(w)

        return True


if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
        print('error: no training data given', file=sys.stderr)
        exit(1)

    bob = Model()
    bob.Train(sys.argv[1])
    while True:
        try:
            bob.Run(input('> '))
        except KeyboardInterrupt:
            print('\b\b  ')
            exit(1)
        except EOFError:
            print()
            exit(1)
