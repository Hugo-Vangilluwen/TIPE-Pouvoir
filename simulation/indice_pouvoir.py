#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calcul de l'indice de pouvoir

@author: Hugo
"""


import math
import matplotlib.pyplot as plt

import utils
import polynome as poly


def parties(ensemble):
    """Calcule l'ensemble des parties"""
    if len(ensemble) == 0:
        return [[]]
    if len(ensemble) == 1:
        return [[], ensemble]

    res = []

    e = ensemble[0]
    f = parties(ensemble[1:])
    for h in f:
        res.append(h.copy())
        res.append(h.copy())
        res[-1].append(e)

    return res


def indice_Banzhaf_naif(quota, poids):
    """Calcule l'indice de pouvoir de Banzhaf
    Algorithme naïf"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    votants = list(poids.keys())

    gagnantes = []
    # tester si la coalition est gagnante
    for coalition in parties(votants):
        somme = 0
        for v in coalition:
            somme += poids[v]
        if somme >= quota:
            gagnantes.append((coalition, somme))

    decisif = dict.fromkeys(votants, 0)
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



def indice_Banzhaf_brut(quota, poids):
    """Calcule la décidabilité / l'indice de Banzhaf brut
    Algorithme avec les polynômes générateurs de Brams-Affuso"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    ibb = {} # indice de Banzhaf brut
    votants = poids.keys()

    for v in votants:
        g = poly.Polynome([1]) # polynôme générateur
        for w in votants:
            if v != w:
                P *= poly.Polynome([1]) + poly.monome(poids[w])

        ibb[v] = 0
        for i in range(max(quota - poids[v], 0), min(quota, P.degre + 1)):
            ibb[v] += P.coef[i]

    return ibb

def indice_Banzhaf(quota, poids):
    """Calcule l'indice de Banzhaf normalisé
    Algorithme de Brams-Affuso avec les séries génératrices"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    ibb = indice_Banzhaf_brut(quota, poids) # indice de Banzhaf brut
    votants = poids.keys()

    somme_ibb = 0
    for v in votants:
        somme_ibb += ibb[v]

    if somme_ibb == 0:
        return {v: 0 for v in ibb}
    return {v: i/somme_ibb for v, i in ibb.items()}


def indice_Banzhaf_relatif(quota, poids):
    """Calcule l'indice de Banzhaf relatif
    Algorithme de Brams-Affuso avec les séries génératrices"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    ibb = indice_Banzhaf_brut(quota, poids) # indice de Banzhaf brut
    nb_votants = 2**(len(poids)-1)

    if nb_votants == 0:
        return {v: 0 for v in ibb}
    return {v: i/nb_votants for v, i in ibb.items()}


def sensibilite(quota, poids):
    """"Calcule la sensibilité ou pouvoir d'une collectivité à agir"""
    return sum(indice_Banzhaf_brut(quota, poids).values()) / 2**(len(poids)-1)


def indice_parlement(sieges, quota_relatif=1/2, verbose=False, plotted=True):
    """Calcule l'indice de pouvoir des différents groupes dans une assemblée
    Le quota s'exprime en pourcentage
    Mettre verbose à true pour afficher les résultats détaillés"""
    total = sum(sieges.values())
    quota = math.ceil(total*quota_relatif)

    ratio = {pays: s/total for pays, s in sieges.items()}
    pouvoir = indice_Banzhaf(quota, sieges)

    difference = {}
    for groupe in sieges.keys():
        difference[groupe] = (pouvoir[groupe] - ratio[groupe]) / ratio[groupe]

    if verbose:
        utils.print_dictionnaire(ratio, "ratio")
        utils.print_dictionnaire(pouvoir, "pouvoir")
        utils.print_dictionnaire(difference, "différence")
    print("sensibilité : ", sensibilite(quota, sieges))

    if plotted:
        fig, axarr = plt.subplots(1, 2)
        axarr[0].pie(ratio.values(), labels=ratio.keys())
        axarr[0].set_title("Ratio de sièges")
        axarr[1].pie(pouvoir.values(), labels=pouvoir.keys())
        axarr[1].set_title("Indice de pouvoir de Banzhaf")
        plt.show()

        plt.bar(difference.keys(), difference.values())
        plt.title("Écart relatif entre le pouvoir et la représentation")
        plt.show()

    return pouvoir


def indice_parlement_UE():
    """Source:
    https://fr.wikipedia.org/wiki/Parlement_europ%C3%A9en#Composition
    """
    # total = 720
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

    indice_parlement(sieges)


def indice_parlement_francais():
    """Source:
    https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"""
    # total = 577 - 1 Vacant
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

    indice_parlement(sieges)


def indice_parlement_francais_alliance():
    """Source:
    https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"""
    # total = 577 - 1 Vacant
    sieges_alliance = {
        "NFP": 192,
        "ENS": 164,
        "DR": 47,
        "RN": 141,
        "LIOT": 22,
        "NI": 10
    }

    indice_parlement(sieges_alliance)

