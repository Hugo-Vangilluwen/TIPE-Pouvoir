#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toutes les petites fonctions utiles

@author: hugo
"""

import matplotlib.pyplot as plt


def print_dictionnaire(d, nom=None, print_total=False):
    """Affiche un dictionnaire"""

    if print_total:
        total = 0

    if nom is not None:
        print(nom, " : ", end="")
    print("{")
    for clef, valeur in d.items():
        print(f"\t{clef} : {valeur}")
        if print_total:
            total += valeur
    if print_total:
        print(f"\tTOTAL : {total}")
    print("}")

def plot_bar(x, y, titre):
    assert len(x) == len(y), "x et y doivent être de la même taille"

    y_pos = range(len(x))
    plt.bar(y_pos, y)
    plt.xticks(y_pos, x, rotation=60)
    plt.title(titre)
    plt.subplots_adjust(bottom=0.15)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
