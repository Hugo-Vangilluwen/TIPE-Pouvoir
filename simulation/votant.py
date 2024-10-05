#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation de classes pour les votants

@author: hugo
"""


from abc import ABC, abstractmethod

from preference import Preference, pref_vide


class Votant(ABC):
    """Classe abstraite représentant n'importe quel votant"""

    def __init__(self, _prefh=pref_vide()):
        """Initialise un votant

        _prefh : préférence honnête"""
        self.set_honnete(_prefh)

    def set_honnete(self, _prefh):
        assert isinstance(_prefh, Preference), \
            "La préférence honnête doit être une préférence."
        self.pref_honnete = _prefh
        self.pref_bulletin = _prefh
        self.choix = _prefh.choix_aléa

    @property
    def bulletin(self):
        return self.pref_bulletin

    @abstractmethod
    def change(self, sondage):
        """Change le bulletin selon le sondage."""

    def __repr__(self):
        """Retourne la préférence honnête et celle du bulletin."""
        return "Honnête : " + str(self.pref_honnete) \
            + " / Bulletin : " + str(self.pref_bulletin)


class VotantSeuil(Votant):
    """Classe des votants qui votent au-dessus d'un certain seuil
    sans jamais voter pour leur pire choix."""

    def __init__(self, _seuil, _prefh=pref_vide()):
        """Initialise un votant-seuil

        _seuil : seuil du votant
        _prefh : préférence honnête"""

        super().__init__(_prefh)

        assert isinstance(_seuil, float) and 0 <= _seuil <= 1, \
            "Le seuil doit être un réel entre 0 et 1 inclus."
        self.seuil = _seuil

    def change(self, sondage):
        """Sléectionne les choix au-dessus du seuil."""
        choix_seuil = []
        choix_bas = []
        dernier = self.pref_honnete.dernier

        for c  in self.choix:
            if c != dernier and sondage[c] >= self.seuil:
                choix_seuil.append(c)
            else:
                choix_bas.append(c)


        self.pref_bulletin = Preference( self.pref_honnete.trier(choix_seuil) \
                + self.pref_honnete.trier(choix_bas) )


class VotantPartisan(Votant):
    """Classe des votants qui ne change jamais de vote."""

    def change(self, sondage):
        """Ne change pas de vote."""


class VotantGagnantPotentiel(Votant):
    """Classe des votants qui votent pour un gagnant potentiel."""

    def change(self, sondage):
        """Vote pour un gagnant potentiel."""
        dernier = self.pref_honnete.dernier
        bpremier = self.pref_bulletin.premier
        hpremier = self.pref_honnete.premier

        ga = self.choix[0] # gagnant actuel
        for c in self.choix:
            if sondage[c] > sondage[ga]:
                ga = c
        sga = sondage[ga] # score du gagnant actuel

        vs = sondage[bpremier] # pourcentage de votants similaires
        if bpremier != hpremier:
            vs += sondage[hpremier]

        gp = [] # gagnants potentiels
        pp = [] # predants potentiels
        for c in self.choix:
            if c == bpremier or c == hpremier:
                if sondage[c] >= sga:
                    gp.append(c)
                else:
                    pp.append(c)
            elif c != dernier and sondage[c] + vs >= sga:
                gp.append(c)
            else :
                pp.append(c)

        self.pref_bulletin = Preference( self.pref_honnete.trier(gp) \
                + self.pref_honnete.trier(pp) )

