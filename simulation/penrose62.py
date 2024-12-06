#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste le système de vote Penrose-62

@author: hugo
"""


import math
import matplotlib.pyplot as plt

import utils
import indice_pouvoir as ip


def test_indice_Banzhaf(coef=7):
    """Calcule les indices de pouvour dans Penrose-62"""
    # Source: https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population
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

    sieges = {}
    for p in population:
        sieges[p] = round(population[p] * coef)

    utils.print_dictionnaire(sieges, "Sièges au parlement par états", True)

    pouvoir = ip.indice_parlement(sieges, 0.62)

    proportionnalite = {}
    for p in population:
        proportionnalite[p] = pouvoir[p] / population[p]

    plt.bar(proportionnalite.keys(), proportionnalite.values())
    plt.title("Rapport de l'indice de pouvoir par la racine carrée de la population")
    plt.show()
