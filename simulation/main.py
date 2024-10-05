#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hugo
"""

import sondage_iteratif as si
import votant as vo

c = ['A', 'B', 'C', 'D']
test = si.SondageIteratif(c)
for _ in range(100):
    test.ajout_votant(vo.VotantSeuil(0.25))

test.initialiser()
print(test)
for i in range(3):
    test.iterer()
    print(test)
