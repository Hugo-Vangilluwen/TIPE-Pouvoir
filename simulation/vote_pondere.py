#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée un vote pondéré pour des indices de Banzhaf donnés

@author: hugo
"""


import math
import matplotlib.pyplot as plt

import indice_pouvoir as ip


def arrondi_vote(v):
    """Arrondi les poids du système de vote"""
    res = {}
    for v, p in v.items():
        res[v] = round(p)
    return res


def vote_pondere(quota, pouvoir, iteration=30):
    """Calcule un vote pondéré
    dont les indices de pouvoir de Banzhaf sont ceux donnés en entrée
    Algorithme d'Aziz-Paterson-Leech 2007"""
    assert isinstance(pouvoir, dict)

    poids = pouvoir.copy()

    for i in range(iteration):
        tmp = ip.indice_Banzhaf(quota, arrondi_vote(poids))
        for v in pouvoir:
            poids[v] += 50*(pouvoir[v] - tmp[v])
            poids[v] = max(1, poids[v])

    poids = arrondi_vote(poids)

    # simplification des poids
    # ne fonctionne pas car le quota ne change pas
    # pgcd_poids = 0 # élément neutre du pgcd
    # for _, p in poids.items():
    #     pgcd_poids = math.gcd(pgcd_poids, p)
    #     print(pgcd_poids)
    # for v in poids:
    #     poids[v] //= pgcd_poids

    return poids


def poids_parlement(quota, quantite, verbose=False):
    """Calcule le poids des différents groupes dans une assemblée
    de manière à ce que l'indice de Banzhaf soit le plus proche possible de la quantité
    Le quota s'exprime en pourcentage
    Mettre verbose à true pour afficher les résultats détaillés"""

    total = sum(quantite.values())
    ratio_quantite = {pays: s/total for pays, s in quantite.items()}
    poids = vote_pondere(quota, ratio_quantite)
    ratio_poids = {pays: s/total for pays, s in poids.items()}
    pouvoir = ip.indice_Banzhaf(quota, poids)

    difference = {}
    difference_rel = {}
    for groupe in quantite.keys():
        difference[groupe] = pouvoir[groupe] - ratio_quantite[groupe]
        difference_rel[groupe] = difference[groupe] / ratio_quantite[groupe]

    if verbose:
        print(f"ratio : {ratio_quantite}")
        print(f"pouvoir réel: {pouvoir}")
        print(f"écart: {difference}")
    print(f"poids : {poids}")

    fig, axarr = plt.subplots(1, 3)
    axarr[0].pie(ratio_poids.values(), labels=ratio_poids.keys())
    axarr[0].set_title("Ratio de sièges")
    axarr[1].pie(ratio_quantite.values(), labels=ratio_quantite.keys())
    axarr[1].set_title("Ratio des quantités")
    axarr[2].pie(pouvoir.values(), labels=pouvoir.keys())
    axarr[2].set_title("Indice de pouvoir de Banzhaf")
    plt.show()

    plt.bar(difference.keys(), difference.values())
    plt.title("Écart entre le pouvoir et la représentation")
    plt.show()
    plt.bar(difference_rel.keys(), difference_rel.values())
    plt.title("Écart relatif entre le pouvoir et la représentation")
    plt.show()

def poids_parlement_UE():
    """Source:
    https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population"""
    quota = 300
    population = { # en million
        "Allemagne": 83.4,
        "France": 68.4,
        "Italie": 59.0,
        "Espagne": 48.6,
        "Pologne": 36.6,
        "Roumanie": 19.1,
        "Pays-Bas": 17.9,
        "Belgique": 11.8,
        "République tchèque": 10.9,
        "Portugal": 10.6,
        "Suède": 10.6,
        "Grèce": 10.4,
        "Hongrie": 9.6,
        "Autriche": 9.2,
        "Bulgarie": 6.4,
        "Danemark": 6.0,
        "Finlande": 5.6,
        "Slovaquie": 5.4,
        "Irlande": 5.3,
        "Croatie": 3.9,
        "Lituanie": 2.9,
        "Slovénie": 2.1,
        "Lettonie": 1.9,
        "Estonie": 1.4,
        "Chypre": 0.9,
        "Luxembourg": 0.7,
        "Malte": 0.6
    }
    for p in population:
        population[p] = math.sqrt(population[p])

    poids_parlement(quota, population)
