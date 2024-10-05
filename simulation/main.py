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
    test.ajout_votant(vo.VotantGagnantPotentiel())

test.initialiser()
print(test)
for i in range(10):
    test.iterer()
    print(test)
