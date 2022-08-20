import math

def print_matrix(matrix):
    print(''.join('-' * 8 for i in matrix))
    for row in matrix:
        print('\t'.join(map(str, row)))
    print(''.join('-' * 8 for i in matrix))

max_cat = 21

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


