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


def realistes(l):
    """Calcule l'ensemble des coalitions réalistes de l triée"""
    n = len(l)
    res = [[]]

    for i in range(n+1):
        for j in range(i+1, n+1):
            res.append(l[i:j])

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
                g *= poly.Polynome([1]) + poly.monome(poids[w])

        ibb[v] = 0
        for i in range(max(quota - poids[v], 0), min(quota, g.degre + 1)):
            ibb[v] += g.coef[i]

    return ibb


def indice_Banzhaf_brut_realiste(quota, poids):
    """Calcule l'indice de pouvoir de Banzhaf
    Algorithme naïf"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    votants = list(poids.keys())

    gagnantes = []
    # tester si la coalition est gagnante
    for coalition in realistes(votants):
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



def indice_Banzhaf(quota, poids, r=False):
    """Calcule l'indice de Banzhaf normalisé
    Algorithme de Brams-Affuso avec les séries génératrices"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)

    # indice de Banzhaf brut
    if r:
        ibb = indice_Banzhaf_brut_realiste(quota, poids)
    else:
        ibb = indice_Banzhaf_brut(quota, poids)
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


def sensibilite(quota, poids, r=False):
    """"Calcule la sensibilité ou pouvoir d'une collectivité à agir"""
    return sum(indice_Banzhaf_brut(quota, poids).values()) / 2**(len(poids)-1)


def indice_parlement(sieges, quota_relatif=1/2, verbose=False, plotted=True, r=False):
    """Calcule l'indice de pouvoir des différents groupes dans une assemblée
    Le quota s'exprime en pourcentage
    Mettre verbose à true pour afficher les résultats détaillés"""
    total = sum(sieges.values())
    quota = math.ceil(total*quota_relatif)

    ratio = {pays: s/total for pays, s in sieges.items()}
    pouvoir = indice_Banzhaf(quota, sieges, r)

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

        utils.plot_bar(difference.keys(), difference.values(), "Écart relatif entre le pouvoir et la représentation")

    return pouvoir


def indice_parlement_UE_pays():
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
        "République\ntchèque": 21,
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


def indice_parlement_UE_groupe():
    """Source:
    https://fr.wikipedia.org/wiki/Parlement_europ%C3%A9en"""
    sieges = {
        "GUE/NGL": 46,
        "S&D": 136,
        "Verts/ALE": 53,
        "RE": 75,
        "PPE": 188,
        "CRE": 80,
        "PfE": 86,
        "ENS": 26
    }

    indice_parlement(sieges, r=True)


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
        "LIOT": 22,
        "ENS": 164,
        "DR": 47,
        "RN": 141,
        "NI": 10
    }

    indice_parlement(sieges_alliance)
    del sieges_alliance["NI"]
    indice_parlement(sieges_alliance, r=True)

