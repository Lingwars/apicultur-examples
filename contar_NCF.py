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


def count_NCC(filename):
    # Read file
    lines = []
    for line in open(filename).readlines():
        lines.append(line.decode("utf-8"))
    print(u"%d lines" % len(lines))

    # Tokenize words
    punctuation = u"""¡,.;:!"#$%&'()*+-/<=>¿?@[\]^_`{|}~"""
    words = [word.strip(punctuation) for line in lines for word in line.split()]
    print(u"%d words" % len(words))

    # APICULTUR
    apiculture = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")  # create API proxy
    #apiculture.set_throttle(60, 60)  # 20 messages every 60 seconds (~bronze suscription)

    # Lemmatize -- APICULTUR ;D
    counter = Counter()
    for word in words:
        lemmas = apiculture.lematiza2(word=word)
        if not lemmas:
            print(u"No he sabido lematizar %s" % word)
            continue

        for lemma in lemmas['lemas']:
            categoria = lemma['categoria']
            print(u"%s --> %s" % (lemma['lema'], lemma['categoria']))
            if categoria[0:3] == 'NCF':
                print(u'%s => %s' % (word, lemma['lema']))
                counter[lemma['lema']] += 1
    return counter


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(u"Usage: 'python %s filename.txt'" % sys.argv[0])
        sys.exit()

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(u"File '%s' not accesible" % filename)
        sys.exit()

    print(u"\t- Processing file: '%s'" % filename)
    counter = count_NCC(filename)

    print(u"\n\t\tLEMMA\t\t\tCATEGORY\t\tCOUNT")
    print(u"  \t\t=====\t\t\t========\t\t=====")
    common_words = counter.most_common(100)
    for lemma, count in common_words:
        print(u"\t\t%-15s\t\t%-10s\t\t%s" % (lemma, "NCF", count))




