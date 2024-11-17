#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal

@author: hugo
"""

import time

import indice_pouvoir as ip
import polynome as poly

def main():
    start = time.process_time()

    ip.indice_parlement_UE()
    ip.indice_parlement_francais()
    ip.indice_parlement_francais_alliance()
    # print(ip.indice_Banzhaf(5, {1:3,2:2,3:1,4:1,5:1}))
    # print(ip.indice_Banzhaf(5, {1: 3, 2:3}))
    # print(ip.indice_Banzhaf(6, {1: 5, 2: 4, 3: 1}))
    # print(ip.indice_Banzhaf_naif(6, {1: 5, 2: 4, 3: 1}))

    end = time.process_time()

    print(f"Temps de calcul : {end - start}s")

if __name__ == "__main__":
    main()
