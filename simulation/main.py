#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal

@author: hugo
"""

import time

import parlement as prl
import vote_pondere as vp
import penrose62


def main():
    start = time.process_time()

    # print(prl.parlements.keys())
    # prl.indice_parlement(prl.parlements["UE groupe"], r=True)
    # print("différence maximale absolue/relative", vp.poids_parlement_UE())
    # penrose62.EU_Penrose(pays_candidats=True, coef=6, qf=0.6, passer_sigma=True)
    penrose62.EU_Penrose(qf=0.61, passer_sigma=True)
    # vp.poids_parlement_UE()

    end = time.process_time()

    print(f"Temps de calcul : {end - start}s")

if __name__ == "__main__":
    main()
