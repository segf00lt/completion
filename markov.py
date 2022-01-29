#!/usr/bin/env python3

import numpy as np
import sys
import string
from english_words import english_words_set

exclude = "!\"#$%\&()*+,-./:;<=>?@[\\]^_`{|}~" + string.digits


class Model:
    def __init__(self):
        self.lexicon = {}
        self.weights = np.empty(0)

    def __Lex(self, data):
        words = {}
        
        for line in data:
            line = line.translate(str.maketrans('', '', exclude)).rstrip().split()
            for w in line:
                if words.get(w) == None:
                    words[w] = None

        words = sorted(words)
        self.lexicon = { words[i]: i for i in range(len(words)) }
        data.seek(0)
        
        return True
        

    def Train(self, file):
        try:
            data = open(file, 'r')
        except FileNotFoundError:
            print(f"error: {file}: no such file", file=sys.stderr)
            return False

        # generate lexicon from file
        self.__Lex(data)
        
        lex_len = len(self.lexicon)

        raw = np.zeros((lex_len, lex_len), dtype=float)

        # load raw data
        for line in data:
            line = line.translate(str.maketrans('', '', exclude)).rstrip().split()
    
            for i in range(len(line) - 1):
                s = line[i]
                t = line[i + 1]
                try:
                    row = self.lexicon[s]
                    col = self.lexicon[t]
                except KeyError:
                    continue
                raw[row][col] += 1

        # adjust probabilities
        tmp = []
        for row in raw:
            rsum = row.sum()
            tmp.append([rsum] if rsum == 0 else [1 / rsum])
        scale = np.array(tmp, dtype=float)
        self.weights = raw * scale

        data.close()
        return True

    def Run(self, data : str) -> bool:
        if len(self.weights) == 0:
            print("error: train model before running", file=sys.stderr)
            return False

        # last word in input string
        word = data.translate(str.maketrans('', '', exclude)).strip().split()[-1]

        if word not in self.lexicon:
            print("No suggestions :(", file=sys.stderr)
            return False

        else:
            index = self.lexicon[word]
            transitions = self.weights[index]
            predict = [list(self.lexicon)[i] for i in np.argpartition(transitions, -5)[-5:]]
            for p in predict:
                print(p)
            return True


if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
        print('error: no training data given', file=sys.stderr)
        exit(1)

    bob = Model()
    bob.Train(sys.argv[1])
    while True:
        bob.Run(input('> '))
