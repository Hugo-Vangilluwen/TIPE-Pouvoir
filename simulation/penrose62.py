# -*- coding: utf-8 -*-
"""
Teste le système de vote Penrose-62
"""


import math
import matplotlib.pyplot as plt
import numpy as np

import utils
import parlement as prl
import indice_pouvoir as ip


def EU_Penrose(coef=8, pays_candidats=False, passer_sigma=False, qf=0.62, comparer62=False):
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
        "République\ntchèque": 10.9,
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

    if pays_candidats:
        # Sources pour les pays :
        # https://fr.wikipedia.org/wiki/Union_europ%C3%A9enne
        # https://european-union.europa.eu/principles-countries-history/eu-enlargement_en
        # Source pour le nombre d'hbitants :
        # Wikipédia
        population.update({
            "Albanie": 2.4,
            "Bosnie-\nHerzégovine": 3.2,
            "Géorgie": 4.0,
            "Macédoine\ndu Nord": 1.8,
            "Moldavie": 2.7,
            "Monténégro": 0.6,
            "Serbie": 6.7,
            "Turquie": 85.4,
            "Ukraine": 38.7
            })

    total_pop = sum(population.values())
    pourcent_pop = {k: v/total_pop for k, v in population.items()}
    utils.print_dictionnaire(pourcent_pop, "Part de la population européenne par pays")

    sqrt_pop = prl.Parlement({}, "Penrose")
    for p in population:
        sqrt_pop.sieges[p] = round(math.sqrt(population[p]) * coef)
    sum_sqrt = sum(sqrt_pop.sieges.values())
    pop_normalise = prl.Parlement({k: v / sum_sqrt for k, v in sqrt_pop.sieges.items()}, "Penrose")

    utils.print_dictionnaire(sqrt_pop.sieges, "Sièges au parlement par états", True)
    print("Quota : ", math.ceil(sum_sqrt*qf) )

    if not passer_sigma:
        quota_arr = [ i/100 for i in range(50, 71) ]
        pourvoir_arr = list( map(
                lambda i :
                    ( lambda d :
                        sum([
                            (pop_normalise.sieges[v] - d[v])**2
                        for v in d.keys() ])
                    )
                    ( ip.indice_Banzhaf( math.ceil(sum_sqrt * i), sqrt_pop.sieges) ),
                quota_arr
            ))
        print(pourvoir_arr)

        plt.plot(quota_arr, pourvoir_arr, marker='o')
        plt.xticks([0.5, 0.55, 0.6, 0.65, 0.7])
        plt.xlabel("quota relatif")
        plt.ylabel(r'$\sigma$   ', rotation=0).set_fontsize(15)
        plt.show()

    pouvoir = prl.indice_parlement(sqrt_pop, qf)

    proportionnalite = {}
    for p in population:
        proportionnalite[p] = pouvoir[p] / math.sqrt(population[p])

    utils.plot_bar(proportionnalite.keys(), proportionnalite.values(), "Rapport de l'indice de pouvoir par rapport la racine carrée de la population", ndigits=1)

    if comparer62:
        pouvoir62 = ip.indice_Banzhaf(math.ceil(sum_sqrt*0.62), sqrt_pop.sieges)

        y_pos = np.array(range(len(pop_normalise.sieges)))
        bar_size = 0.2

        plt.bar(y_pos-bar_size, pouvoir62.values(), color='b', width=bar_size)
        plt.bar(y_pos, pouvoir.values(), color='g', width=bar_size)
        plt.bar(y_pos+bar_size, pop_normalise.sieges.values(), color='r', width=bar_size)
        plt.xticks(y_pos, pop_normalise.sieges.keys(), rotation=60)

        plt.subplots_adjust(bottom=0.15)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.show()
