#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fichier principal
"""

import time

import parlement as prl
import vote_pondere as vp
import penrose62
import indice_pouvoir as ip


def main():
    start = time.process_time()

    # Décommenter une line pour effectuer un calcul
    # prl.indice_parlement(prl.parlement_UE["pays"])
    # prl.indice_parlement(prl.parlement_UE["groupe"], reel=True)
    # print("différence maximale absolue/relative", vp.poids_parlement_UE())
    # penrose62.EU_Penrose(pays_candidats=True, coef=6, qf=0.6, passer_sigma=True)
    # penrose62.EU_Penrose(qf=0.62)

    end = time.process_time()

    print(f"Temps de calcul : {end - start}s")

if __name__ == "__main__":
    main()
