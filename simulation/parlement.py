#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitaire et données de différents parlements

@author: Hugo
"""


import math
import matplotlib.pyplot as plt

import utils
import indice_pouvoir as ip
import realiste


def indice_parlement(parlement, quota_relatif=1/2, verbose=False, plotted=True, r=False, ndigits=1, normalise=True):
    """Calcule l'indice de pouvoir des différents groupes dans une assemblée
    Le quota s'exprime en pourcentage
    Mettre verbose à true pour afficher les résultats détaillés
    r indique si les indices doivent réalistes ou non (par défaut non)"""
    assert isinstance(parlement, Parlement)


    total = parlement.total
    quota = math.ceil(total*quota_relatif)

    ratio = {pays: s/total for pays, s in parlement.sieges.items()}
    if normalise:
        pouvoir = ip.indice_Banzhaf(quota, parlement.sieges)
    else:
        pouvoir = ip.indice_Banzhaf_absolu(quota, parlement.sieges)
    if r:
        if normalise:
            pouvoir_realiste = realiste.indice_Banzhaf(quota, parlement.sieges)
        else:
            pouvoir_realiste = realiste.indice_Banzhaf_absolu(quota, parlement.sieges)

    difference = {}
    difference_realiste = {}
    for groupe in parlement.sieges.keys():
        difference[groupe] = (pouvoir[groupe] - ratio[groupe]) / ratio[groupe]
        if r:
            difference_realiste[groupe] = (pouvoir_realiste[groupe]  - ratio[groupe]) / ratio[groupe]

    if verbose:
        utils.print_dictionnaire(ratio, "ratio")
        utils.print_dictionnaire(difference, "différence")
        if normalise:
            utils.print_dictionnaire(pouvoir, "pouvoir")
        else:
            utils.print_dictionnaire(pouvoir, "pouvoir absolu")
        if r:
            if normalise:
                utils.print_dictionnaire(pouvoir_realiste, "pouvoir réaliste")
            else:
                utils.print_dictionnaire(pouvoir_realiste, "pouvoir réaliste absolu")
            utils.print_dictionnaire(difference_realiste, "différence réaliste")
    print("sensibilité : ", ip.sensibilite(quota, parlement.sieges))

    if plotted:
        data_pouvoir = [
            (ratio, "Ratio de sièges"),
            (pouvoir, "Indice de pouvoir de Banzhaf")
        ]
        if r:
            data_pouvoir.append((pouvoir_realiste, "Indice de pouvoir\nréaliste de Banzhaf"))
        utils.plot_pie(data_pouvoir, couleurs=parlement.couleurs)

        utils.plot_bar(difference.keys(), difference.values(), "", couleurs=parlement.couleurs, ndigits=ndigits) # "Écart relatif entre le pouvoir et la représentation"

        if r:
            utils.plot_bar(difference_realiste.keys(), difference_realiste.values(), "Écart relatif entre le pouvoir réaliste et la représentation", couleurs=parlement.couleurs, ndigits=ndigits)

    return pouvoir


class Parlement:
    def __init__(self, _sieges, _source, _couleurs=None):
        self.sieges = _sieges
        self.source = _source
        self.couleurs = _couleurs

    @property
    def total(self):
        """Nombre total de parlementaires"""
        return sum(self.sieges.values())


parlements = {
    "UE pays": Parlement( # total = 720
        {
            "Allemagne": 96,
            "France": 81,
            "Italie": 76,
            "Espagne": 60,
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
        },
        "https://www.europarl.europa.eu/meps/fr/search/table"
        ),
    "UE groupe": Parlement(
        {
            "GUE/NGL": 46,
            "S&D": 136,
            "Verts/ALE": 53,
            "RE": 75,
            "PPE": 188,
            "CRE": 80,
            "PfE": 86,
            "ENS": 26
        },
        "https://www.europarl.europa.eu/meps/fr/search/chamber",
        {
            "GUE/NGL": "#460000",
            "S&D": "#c80000",
            "Verts/ALE": "#32c800",
            "RE": "#ffaa00",
            "PPE": "#003c78",
            "CRE": "#0082ff",
            "PfE": "#9b20a9",
            "ENS": "#808080"
        }
        ),
    "français": Parlement( # total = 577 - 1 Vacant
        {
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
        },
        "https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif",
        {
            "GDR": "#830e21",
            "LFI-NFP": "#c00d0d",
            "ECO": "#77aa79",
            "SOC": "#f5b4ce",
            "DEM": "#f07e26",
            "EPR": "#7b4591",
            "HOR": "#b5e2f9",
            "LIOT": "#ffd96f",
            "DR": "#8cb0dc",
            "UDR": "#3367a7",
            "RN": "#313567",
            "NI": "#8d949a"
        },
        ),
    "français alliance": Parlement(
        {
            "NFP": 192,
            "LIOT": 22,
            "ENS": 164,
            "DR": 47,
            "RN": 141,
            "NI": 10
        },
        "https://fr.wikipedia.org/wiki/Parlement_europ%C3%A9en"
        )
    }
