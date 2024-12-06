#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toutes les petites fonctions utiles

@author: hugo
"""

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
