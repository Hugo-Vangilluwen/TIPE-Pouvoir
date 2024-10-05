#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation des préférences formalisé en relation de ordre
Sous la forme de classes

@author: hugo
"""

from random import sample


class Preference:
    """Les préférences sont des relations d'ordres totales."""

    def __init__(self, _choix):
        """Initialise à partir une liste de choix ordonnés"""

        assert isinstance(_choix, list), \
            "Les choix doivent être rassemblés dans une liste ordonnée"
        self.pref = _choix

    def comparer(self, a, b):
        """Compare de façon large les deux choix A et B selon cette préférence.

        retourne True si A et B ne sont pas présents dans cette préférence
        """
        for i in self.pref:
            if a == i:
                return True
            if b == i:
                return False

        return True

    @property
    def choix(self):
        """Retourne l'ensemble des choix dans un ordre."""
        return self.pref

    @property
    def choix_aléa(self):
        """Retourne l'ensemble des choix dans un ordre aléatoire."""
        return sample(self.pref, len(self.pref))

    @property
    def premier(self):
        """Renvoie le choix préféré."""
        return self.pref[0]

    @property
    def dernier(self):
        "Renvoie le choix détesté."""
        return self.pref[-1]

    def trier(self, ensemble):
        """Trie l'ensemble de choix"""
        res = []

        for p in self.pref:
            if p in ensemble:
                res.append(p)

        return res


def pref_vide():
    return Preference([])
