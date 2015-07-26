#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from collections import Counter

from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)


def cervantes_level(filename):
    # We are going to request Cevantes level for each lematized word

    # Read file
    lines = []
    for line in open(filename).readlines():
        lines.append(line.decode("utf-8"))
    print(u"%d lines" % len(lines))

    # Tokenize words
    punctuation = u"""¡,.;:!"#$%&'()*+-/<=>¿?@[\]^_`{|}~"""
    words = [word.strip(punctuation) for line in lines for word in line.split()]
    print(u"%d words" % len(words))

    # APICULTURE
    apiculture = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")  # create API proxy
    
    # Lemmatize -- APICULTUR ;D
    print(u"=== 1) Lematizar")
    counter = Counter()
    for word in words:
        lemmas = apiculture.lematiza2(word=word)
        if lemmas:
            lema = lemmas['lemas'][0]  # TODO: Desambiguation!
            print(u'%s => %s' % (word, lema['lema']))
            counter[(lema['lema'], lema['categoria'])] += 1

    # Get Cervantes level for each lemma -- APICULTUR
    print(u"=== 2) Nivel de cada lema")
    sum_levels = 0
    n_lemmas = 0
    for (lemma, cat), count in counter.most_common():
        level = apiculture.damenivel(word = lemma)
        if level:
            level = level['valor']
            if level != 0:  # TODO: level == 0 for non categorized words
                print(u'%s (%s) => level %s' % (lemma, cat, level))            
                sum_levels += level*count
                n_lemmas += count

    # Return medium value
    return sum_levels, n_lemmas


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(u"Usage: 'python %s filename.txt'" % sys.argv[0])
        sys.exit()

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(u"File '%s' not accesible" % filename)
        sys.exit()

    print(u"\t- Processing file: '%s'" % filename)
    sum_levels, n_lemmas = cervantes_level(filename)

    if n_lemmas != 0:
        print(u"\t- Computed media for text: %s (on %s lemmas)" % (sum_levels/n_lemmas, n_lemmas))
    else:
        print(u"No words evaluated")



