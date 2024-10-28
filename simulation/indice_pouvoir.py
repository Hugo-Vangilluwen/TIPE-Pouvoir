#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcul de l'indice de pouvoir

@author: Hugo
"""


import math
import multiprocessing.pool
import matplotlib.pyplot as plt
import time


def parties(ensemble):
    """Calcule l'ensemble des parties"""
    if len(ensemble) == 0:
        return [[]]
    if len(ensemble) == 1:
        return [[], ensemble]

    res = []

    e = ensemble[0]
    g = parties(ensemble[1:])
    res.extend(g)
    gg = []
    for h in g:
        gg.append(h.copy())
        gg[-1].append(e)
    res.extend(gg)

    return res


class WorkerBanzhaf:
    """Worker class"""

    def __init__(self, quota, poids, votants):
        self.quota = quota
        self.poids = poids
        self.votants = votants

    def __call__(self, gagnantes):
        decisif = dict.fromkeys(self.votants, 0)

        for coalition, somme in gagnantes:
            for v in coalition:
                if (somme - self.poids[v]) < self.quota:
                    decisif[v] += 1

        return decisif



def indice_Banzhaf(quota, poids):
    """Calcule l'indice de pouvoir de Banzhaf
    Algorithme naïf"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    votants = list(poids.keys())

    gagnantes = []
    decisif = dict.fromkeys(votants, 0)

    # tester si la coalition est gagnante
    for coalition in parties(votants):
        somme = 0
        for v in coalition:
            somme += poids[v]
        if somme >= quota:
            gagnantes.append((coalition, somme))

    # print(gagnantes)

    # Sans paraléllisme
    for coalition, somme in gagnantes:
        for v in coalition:
            if (somme - poids[v]) < quota:
                decisif[v] += 1

    # Avec paraléllisme
    # print(gagnantes)
    # g = len(gagnantes)
    # WB = WorkerBanzhaf(quota, poids, votants)
    # n = 8
    # iterable = []
    # for i in range(n):
    #     iterable.append(gagnantes[int(g*i/n):int(g*(i+1)/n)])
    # print(iterable)
    # with multiprocessing.pool.Pool(processes=4) as mypool:
    #     for sous_decisif in mypool.map(
    #             func=WB,
    #             # iterable=gagnantes
    #             iterable=iterable):
    #         for k, v in sous_decisif.items():
    #             decisif[k] += v


    somme_d = 0
    for v in votants:
        somme_d += decisif[v]

    # print(decisif)

    return {v: d/somme_d for v, d in decisif.items()}



def indice_parlement(total, sieges):
    """Calcule l'indice de pouvoir des différents groupes dans une assemblée"""
    assert sum(sieges.values()) == total, f"{sum(sieges.values())} <> {total}"

    ratio = {pays: s/total for pays, s in sieges.items()}
    pouvoir = indice_Banzhaf(math.ceil(total/2), sieges)
    print(f"ratio : {ratio}")
    print(f"pouvoir : {pouvoir}")

    difference = {}
    for pays in sieges.keys():
        difference[pays] = (pouvoir[pays] - ratio[pays]) / ratio[pays]
    print(f"écart relatif: {difference}")

    fig, axarr = plt.subplots(1, 2)
    axarr[0].pie(ratio.values(), labels=ratio.keys())
    axarr[0].set_title("Ratio de sièges")
    axarr[1].pie(pouvoir.values(), labels=pouvoir.keys())
    axarr[1].set_title("Indice de pouvoir de Banzhaf")
    plt.show()

    plt.bar(difference.keys(), difference.values())
    plt.title("Écart relatif entre le pouvoir et la représentation")
    plt.show()


def indice_parlement_UE():
    """Source:
    https://fr.wikipedia.org/wiki/Parlement_europ%C3%A9en#Composition
    """
    total = 720
    sieges = {
        "Allemagne": 96,
        "France": 81,
        "Italie": 76,
        "Espagne": 61,
        "Pologne": 53,
        "Roumanie": 33,
        "Pays-Bas": 31,
        "Belgique": 22,
        "République tchèque": 21,
        "Grèce": 21,
        "Hongrie": 21,
        "Portugal": 21,
        "Suède": 21,
        "Autriche": 20,
        "Bulgarie": 17,
        "Danemark": 15,
        "Finlande": 15,
        "Slovaquie": 15,
        "Irlande": 14,
        # "Croatie": 12,
        # "Lituanie": 11,
        # "Lettonie": 9,
        # "Slovénie": 9,
        # "Estonie": 7,
        # "Chypre": 6,
        # "Luxembourg": 6,
        # "Malte": 6
    }
    # assert sum(sieges.values()) == total
    total = sum(sieges.values())

    indice_parlement(total, sieges)


def indice_parlement_francais():
    """Source:
    https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"""
    total = 577 - 1  # 1 Vacant
    sieges = {
        "GDR": 17,
        "LFI-NFP": 71,
        "ECO": 38,
        "SOC": 66,
        "DEM": 36,
        "EPR": 95,
        "HOR": 33,
        "LIOT": 22,
        "DR": 47,
        "UDR": 16,
        "RN": 125,
        "NI": 10
    }

    indice_parlement(total, sieges)


def indice_parlement_francais2():
    """Source:
    https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"""
    total = 577 - 1  # 1 Vacant
    sieges_alliance = {
        "NFP": 192,
        "ENS": 164,
        "DR": 47,
        "RN": 141,
        "LIOT": 22,
        "NI": 10
    }

    indice_parlement(total, sieges_alliance)

start = time.process_time()

# trop long impossible à calculer avec les 27 pays
indice_parlement_UE()
# indice_parlement_francais()
# indice_parlement_francais2()
# print(indice_Banzhaf(5, {1:3,2:2,3:1,4:1,5:1}))
# print(indice_Banzhaf(5, {1: 3, 2:3}))

end = time.process_time()

print(end - start)
