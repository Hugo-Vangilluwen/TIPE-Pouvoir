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
import indice_pouvoir as ip


def main():
    start = time.process_time()

    # print(prl.parlements.keys())
    # prl.indice_parlement(prl.parlements["UE pays"], r=False)
    # print("différence maximale absolue/relative", vp.poids_parlement_UE())
    penrose62.EU_Penrose(pays_candidats=True, coef=6, qf=0.6, passer_sigma=True)
    # penrose62.EU_Penrose(qf=0.61, passer_sigma=False)
    # vp.poids_parlement_UE()
    # ip.indice_Banzhaf_naif(360, prl.parlements["UE pays"].sieges)

    end = time.process_time()

    print(len(prl.parlements["UE pays"].sieges))
    print(f"Temps de calcul : {end - start}s")

if __name__ == "__main__":
    main()
