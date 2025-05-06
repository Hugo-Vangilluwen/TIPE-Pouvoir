#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calcul de l'indice de pouvoir

@author: Hugo
"""

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
    # itérer dans les coalitions
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



def indice_Banzhaf(quota, poids):
    """Calcule l'indice de Banzhaf normalisé
    Algorithme de Brams-Affuso avec les séries génératrices"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)

    # indice de Banzhaf brut
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


def sensibilite(quota, poids):
    """"Calcule la sensibilité ou pouvoir d'une collectivité à agir"""
    return sum(indice_Banzhaf_brut(quota, poids).values()) / 2**(len(poids)-1)

