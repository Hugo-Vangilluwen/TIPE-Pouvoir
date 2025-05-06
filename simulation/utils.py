#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toutes les petites fonctions utiles

@author: hugo
"""

import math
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

def plot_bar(x, y, titre, couleurs=None, ndigits=None):
    assert len(x) == len(y), "x et y doivent être de la même taille"

    y_pos = range(len(x))
    if couleurs == None:
        couleurs_pos = None
    else:
        couleurs_pos = list(couleurs.values())
    rectarr = plt.bar(y_pos, y, color=couleurs_pos)
    for rect in rectarr:
        height = rect.get_height()
        if height < 0:
            va = "top"
        else:
            va = "bottom"
        plt.text(rect.get_x() + rect.get_width()/2, height, str(round(height*100, ndigits)) + "%", ha="center", va=va)
    plt.xticks(y_pos, x, rotation=60)
    plt.title(titre)
    plt.subplots_adjust(bottom=0.15)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()


def plot_pie(data, couleurs=None):
    """Affiche des diagrammes circulaires
    un par élément de data qui sont de la forme (dictionnaire, titre)
    couleurs donne les couleurs des données (optionel)"""
    n = len(data)
    fig, axarr = plt.subplots(1, n)

    for i in range(n):
        if couleurs == None:
            c = None
        else:
            c = [] # couleurs
        dwz = {} # data without zero
        for k, v in data[i][0].items():
            if v != 0:
                dwz[k] = v
                if couleurs != None:
                    c.append(couleurs[k])

        axarr[i].pie(dwz.values(), labels=dwz.keys(), rotatelabels=True, colors=c)
        axarr[i].set_title(data[i][1], pad=40)

    #fig.tight_layout(w_pad=90)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
