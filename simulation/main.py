#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal

@author: hugo
"""

import time

import indice_pouvoir as ip
import vote_pondere as vp
import penrose62


def main():
    start = time.process_time()

    # ip.indice_parlement_UE_pays()
    ip.indice_parlement_UE_groupe()
    # ip.indice_parlement_francais()
    # ip.indice_parlement_francais_alliance()
    # print("différence maximale absolue/relative", vp.poids_parlement_UE())
    # penrose62.test_indice_Banzhaf()
    # vp.poids_parlement_UE()

    end = time.process_time()

    print(f"Temps de calcul : {end - start}s")

if __name__ == "__main__":
    main()
