#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation d'une classe pour les sondages itératifs

A faire :
    - changer initialiser
    - créer classe des votants avec change()

@author: hugo
"""


from random import sample

from preference import Preference
from votant import Votant


class SondageIteratif:
    """Classe représentant n'importe quel sondage itératif"""

    def __init__(self, _choix):
        """Initialise un sondage

        _choix : liste des choix
        _elect : électorat"""

        assert isinstance(_choix, list), \
            "Les choix doivent être rassemblés dans une liste"
        self.choix = _choix.copy()
        self.nb_choix = len(self.choix)

        # assert isinstance(_elect, Electorat)
        # self.elect = _elect
        # self.elect.init_honnete()
        self.votants = []

    def ajout_votant(self, v):
        """Ajoute le votant v."""
        assert isinstance(v, Votant) and \
            (frozenset(v.choix) == frozenset(self.choix) or len(v.choix) == 0)
        self.votants.append(v)

    def initialiser(self):
        """Initialise les préférences des électeurs dans self.pref_honnete"""
        self.pref_honnete = []
        for v in self.votants:
            v.set_honnete(Preference(sample(self.choix, self.nb_choix)))

    def sondage(self):
        """Effectue un sondage"""
        s = {c : 0 for c in self.choix}

        for v in self.votants:
            s[v.bulletin.premier] += 1

        l = len(self.votants)
        for c in self.choix:
            s[c] /= l

        return s

    def iterer(self):
        """Effectue un sondage et change les votes de électeurs selon  les résultats"""
        s = self.sondage()
        # self.elect.iterer_change(self.sondage())
        for v in self.votants:
            v.change(s)

        # for i in range(self.votants):
        #    self.pref[i] = self.change(i, s)

    def change(self, n, s):
        """Change le bulletin du n-ième électeur selon le sondage s"""
        seuil = 0.25
        choix_seuil = []
        choix_bas = []
        choix_dernier = self.pref_honnete[n].dernier

        for c  in self.choix:
            if c != choix_dernier:
                if s[c] >= seuil:
                    choix_seuil.append(c)
                else:
                    choix_bas.append(c)

        return Preference( self.pref_honnete[n].trier(choix_seuil) \
                + self.pref_honnete[n].trier(choix_bas) \
                + [choix_dernier] )

    def __repr__(self):
        """Retourne le sondage actuel."""
        return str(self.sondage())
