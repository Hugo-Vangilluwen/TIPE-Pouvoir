#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toutes les petites fonctions utiles

@author: hugo
"""

def print_dictionnaire(d, nom=None):
    """Affiche un dictionnaire"""

    if nom is not None:
        print(nom, " : ", end="")
    print("{")
    for clef, valeur in d.items():
        print(f"\t{clef} : {valeur}")
    print("}")
