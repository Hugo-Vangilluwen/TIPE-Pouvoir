# -*- coding: utf-8 -*-
"""
Calcul de l'indice de pouvoir réaliste
"""

def coalitions_realistes(l):
    """Calcule l'ensemble des coalitions réalistes de l triée"""
    n = len(l)
    res = [[]]

    for i in range(n+1):
        for j in range(i+1, n+1):
            res.append(l[i:j])

    return res

def nb_realistes(n):
    """Calcule le nombre de coalitions réalistes"""
    return 1 + n*(n+1)/2


def indice_Banzhaf_brut(quota, poids):
    """Calcule l'indice de pouvoir réaliste de Banzhaf
    Algorithme naïf"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    votants = list(poids.keys())

    gagnantes = []
    # itérer dans les coalitions réalistes
    for coalition in coalitions_realistes(votants):
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
    return decisif


def indice_Banzhaf(quota, poids):
    """Calcule l'indice de Banzhaf réaliste"""
    ibb = indice_Banzhaf_brut(quota, poids)
    somme_d = sum(ibb.values())

    if somme_d == 0:
        return {v: 0 for v in ibb}
    return {v: d/somme_d for v, d in ibb.items()}


def indice_Banzhaf_absolu(quota, poids):
    """Calcule l'indice de Banzhaf absolu réaliste"""
    assert isinstance(quota, int)
    assert isinstance(poids, dict)
    ibb = indice_Banzhaf_brut(quota, poids) # indice de Banzhaf brut
    votants = list(poids.keys)
    nb_votants = len(poids)

    if nb_votants == 0:
        return {v: 0 for v in ibb.keys()}
    return {v: i/( votants.index(v) * (nb_votants - votants.index(v) + 1) ) for v, i in ibb.items()}
