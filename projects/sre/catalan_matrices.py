import math
from abc import ABC, abstractmethod

def print_matrix(matrix):
    print(''.join('-' * 8 for i in matrix))
    for row in matrix:
        print('\t'.join(map(str, row)))
    print(''.join('-' * 8 for i in matrix))

max_cat = 100

catalans = [math.comb(2*i, i) // (i+1) for i in range(max_cat)]

def catalan_matrix(size):
    if 2 * size > max_cat + 1:
        raise Exception('Need to compute more catalan numbers for matrix size')
    return [catalans[i:i+size] for i in range(size)]

def row_subtract(mat, val, i, mult, edit_index):
    for j, temp in enumerate(val):
        if temp != 0:
            break

    if i > j:
        print_matrix(mat)
        print(f"Row to edit: {mat[index]}")
        print(f"Row edit value: {val}")
        raise Exception('Val has a later first zero than edit row')
    if i < j:
        return mat

    if val[i] != 1:
        print_matrix(mat)
        print(f"Row to edit: {mat[index]}")
        print(f"Row edit value: {val}")
        raise Exception('For some reason first is not 1.') 

    mat[edit_index] = [a - b*mult for a, b in zip(mat[edit_index], val)]
    return mat

def row_reduce(mat, i):
    for first_ind, val in enumerate(mat[i]):
        if val != 0:
            break
    for ind in range(i + 1, len(mat)):
        row_subtract(mat, mat[i], first_ind, mat[i][ind], ind)

def reduce(size):
    mat = catalan_matrix(size)
    print_matrix(mat)
    for i in range(len(mat) - 1):
        row_reduce(mat, i)
        print_matrix(mat)
    return mat

class Variable:
    def __init__(self, var):
        self.var = var

    def __mul__(self, var):
        var = var.var
        for k, v in var.items():
            if k not in self.var:
                self.var[k] = 0
            self.var[k] += v
        return self

    def __eq__(self, var):
        return self.var == var.var

    def __str__(self):
        return "".join([f"({{{k}}})^{{{v}}}" for k, v in self.var.items()])

    def clone(self):
        return Variable(self.var.copy())

class ApCoeff:
    def __init__(self, power, coeff, var):
        self.power = power
        self.coeff = coeff
        self.var = var

    def __str__(self):
        if self.power % 2 == 1:
            return '0'
        return f"({catalans[self.power // 2] * self.coeff}){str(self.var)}"

    def __mul__(self, ap):
        return ApCoeff(self.power + ap.power, self.coeff * ap.coeff, self.var.clone() * ap.var.clone())

    def can_add(self, ap):
        return self.var == ap.var and self.power == ap.power

    def __add__(self, ap):
        if not self.can_add(ap):
            raise Exception('youre stupid')
        self.coeff += ap.coeff
        return self

    def clone(self):
        return ApCoeff(self.power, self.coeff, self.var.clone())

class Equation:
    def __init__(self, apcoeffs):
        self.aps = apcoeffs

    def __mul__(self, eq):
        self.aps = [f * s for f in self.aps for s in eq.aps]
        self.simplify_like()
        return self.clone()

    def simplify_like(self):
        d = []
        for ap in self.aps:
            for elem in d:
                if elem.can_add(ap):
                    elem += ap
                    break
            else:
                d.append(ap)
        self.aps = d

    def __add__(self, eq):
        self.aps.extend(eq.aps)
        return self.clone()

    def __str__(self):
        return "+".join([str(ap) for ap in self.aps if str(ap) != '0'])

    def clone(self):
        return Equation([a.clone() for a in self.aps])

    def __repr__(self):
        return self.__str__()

def second_degree():
    a = Variable({'a': 1})
    b = Variable({'b': 1})
    c = Variable({'c': 1})
    x = ApCoeff(1, 1, Variable({}))

    t = Equation([x.clone(), ApCoeff(0, -1, c.clone())])
    g = t.clone() * t.clone() * t.clone() + Equation([ApCoeff(0, 1, a.clone())]) * t.clone() * t.clone() + Equation([ApCoeff(0, 1, b.clone())]) * t.clone()
    l = g.clone() * g.clone()
    print(f"\\frac{{({g})^2}}{{{l}}}")



