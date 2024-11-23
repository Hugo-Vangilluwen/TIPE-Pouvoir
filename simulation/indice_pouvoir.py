#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calcul de l'indice de pouvoir

@author: Hugo
"""


import math
import matplotlib.pyplot as plt

import polynome as poly


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


def indice_Banzhaf_naif(quota, poids):
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

    for coalition, somme in gagnantes:
        for v in coalition:
            if (somme - poids[v]) < quota:
                decisif[v] += 1

    somme_d = 0
    for v in votants:
        somme_d += decisif[v]

    if somme_d == 0:
        return {v: 0 for v in decisif}
    return {v: d/somme_d for v, d in decisif.items()}


def indice_Banzhaf(quota, poids):
    """Calcule l'indice de Banzhaf
    Algorithme de Brams-Affuso avec les séries génératrices"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    iba = {} # indice de Banzhaf absolu
    votants = poids.keys()

    for v in votants:
        g = poly.Polynome([1]) # génératrice
        for w in votants:
            if v != w:
                g *= poly.Polynome([1]) + poly.monome(poids[w])

        iba[v] = 0
        for i in range(quota - poids[v], min(quota, g.degre + 1)):
            iba[v] += g.coef[i]

    somme_iba = 0
    for v in votants:
        somme_iba += iba[v]

    if somme_iba == 0:
        return{v: 0 for v in iba}
    return {v: i/somme_iba for v, i in iba.items()}


def indice_parlement(total, sieges, quota_relatif=1/2, verbose=False):
    """Calcule l'indice de pouvoir des différents groupes dans une assemblée
    Le quota s'exprime en pourcentage
    Mettre verbose à true pour afficher les résultats détaillés"""
    assert sum(sieges.values()) == total, f"{sum(sieges.values())} != {total}"

    ratio = {pays: s/total for pays, s in sieges.items()}
    pouvoir = indice_Banzhaf(math.ceil(total*quota_relatif), sieges)

    difference = {}
    for groupe in sieges.keys():
        difference[groupe] = (pouvoir[groupe] - ratio[groupe]) / ratio[groupe]

    if verbose:
        print(f"ratio : {ratio}")
        print(f"pouvoir : {pouvoir}")
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
        "Croatie": 12,
        "Lituanie": 11,
        "Lettonie": 9,
        "Slovénie": 9,
        "Estonie": 7,
        "Chypre": 6,
        "Luxembourg": 6,
        "Malte": 6
    }

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


def indice_parlement_francais_alliance():
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

