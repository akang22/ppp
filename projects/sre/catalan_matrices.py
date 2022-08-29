import math

def print_matrix(matrix):
    print(''.join('-' * 8 for i in matrix))
    for row in matrix:
        print('\t'.join(map(str, row)))
    print(''.join('-' * 8 for i in matrix))

max_cat = 100

catalans = [math.comb(2*i, i) // (i+1) for i in range(1, max_cat)]

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

class ApCoeff:
    def __init__(self, power, coeff):
        self.power = power
        self.coeff = coeff

    def eval(self):
        return catalans[self.power // 2] * self.coeff

    def mult(self, ap):
        return ApCoeff(self.power + ap.power, self.coeff * ap.coeff)

class Equation:
    def __init__(self, apcoeffs):
        self.aps = apcoeffs

    def mult(self, aps):
        self.aps = [f.mult(s) for f in self.aps for s in aps]
        self.simplify_like()

    def simplify_like(self):
        d = {}
        for ap in self.aps:
            if ap.power in d:
                d[ap.power].coeff += ap.coeff
            else:
                d[ap.power] = ap
        self.aps = list(d.values())

    def eval(self):
        return abs(sum([ap.eval() for ap in self.aps]))


def holders_inequality_main(max_w):
    mult_eq = [ApCoeff(2, -4), ApCoeff(4, 1)]
    eq = Equation([ApCoeff(2, -4), ApCoeff(4, 1)])
    left_side = 2
    a = "["

    for i in range(1, max_w):
        a += f"({i + 1}, \\sqrt[{i}]{{\\frac{{{left_side}}}{{{eq.eval()}}}}}),"
        left_side *= 2
        eq.mult(mult_eq)

    return a + "]"

