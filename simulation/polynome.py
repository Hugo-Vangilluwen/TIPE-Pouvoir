#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal

@author: hugo
"""

import math

class Polynome:
    """Classe modélisant un polynôme sous forme de liste"""

    def __init__(self, coef):
        """Initialise le polynôme avec la liste de ses coefficents"""
        # liste des coefficents dans l'ordre croissant des puissances
        self.coef = coef.copy()

    def est_nul(self):
        """Teste si le polynôme est le polynôme nul"""
        for c in self.coef:
            if c != 0:
                return False
        return True

    def coefficents_nuls(self):
        """Enlève les coefficents nuls"""
        while len(self.coef) != 0 and self.coef[-1] == 0:
            del self.coef[-1]

    @property
    def degre(self):
        """Degré du polynôme"""
        self.coefficents_nuls()
        if self.est_nul():
            return - math.inf
        return len(self.coef) - 1

    def __str__(self):
        """Retourne un représentation du polynôme"""
        if self.est_nul():
            return "0"
        res = str(self.coef[0])
        for i in range(1, self.degre + 1):
            res += f" + {str(self.coef[i])}*X^{i}"
        return res

    def copier(self):
        """Copie le polynôme"""
        return Polynome(self.coef.copy())

    def __iadd__(self, p):
        """Ajoute p au polynôme"""
        assert isinstance(p, Polynome)
        if p.est_nul():
            return self
        for i in range(p.degre + 1):
            if i < len(self.coef):
                self.coef[i] += p.coef[i]
            else:
                self.coef.append(p.coef[i])
        return self

    def __add__(self, p):
        """Additionne deux polynômes"""
        if self.degre >= p.degre:
            r = self.copier()
            s = p
        else:
            r = p.copier()
            s = self

        r += s
        return r

    def __mul__(self, p):
        """Multiplie deux polynômes"""
        if isinstance(p, float) or isinstance(p, int):
            res = self.copier()
            for i in range(self.degre + 1):
                res.coef[i] *= p
        elif isinstance(p, Polynome):
            res = Polynome([])
            if not p.est_nul():
                for i in range(p.degre + 1):
                    pp = self.copier()
                    pp *= p.coef[i]
                    for j in range(i):
                        pp.coef.insert(0, 0)
                    res += pp
        else:
            raise TypeError("p doit être un entier, un flottant ou un polynôme.")

        return res

    def __imul__(self, p):
        """"Multiplie ce polynôme par p"""
        self = self * p
        return self


def monome(n):
    """Calcule un monôme de degré n."""
    res = []
    for i in range(n):
        res.append(0)
    res.append(1)
    return Polynome(res)
