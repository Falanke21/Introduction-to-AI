# Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. kenken_csp_model (worth 20/100 marks)
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools


def binary_ne_grid(kenken_grid):
    # n = kenken_grid[0][0]
    # variables = []
    # two_d_array = []
    #
    # for i in range(n):
    #     two_d_array.append([])
    #     for j in range(n):
    #         var = Variable(str(i + 1) + str(j + 1), range(1, n + 1))
    #         variables.append(var)
    #         two_d_array[i].append(var)
    #     con = Constraint("Row " + str(i), two_d_array[i])
    #
    #     varDoms = []
    #     for v in two_d_array[i]:
    #         varDoms.append(v.domain())
    #     for t in itertools.product(*varDoms):
    #         if lambda t:
    #
    # csp = CSP("kenken", variables)
    #
    #
    # return csp, two_d_array
    pass

def all_diff(t):
    """
    Helper for nary_ad_grid
    """
    if len(set(t)) == len(t):
        return True
    return False

def nary_ad_grid(kenken_grid):
    n = kenken_grid[0][0]
    variables = []
    two_d_array = []

    # construct variables
    for i in range(n):
        two_d_array.append([])
        for j in range(n):
            var = Variable(str(i + 1) + str(j + 1), range(1, n + 1))
            variables.append(var)
            two_d_array[i].append(var)

    csp = CSP("kenken", variables)

    # add row constrains
    for i in range(n):
        row_con = Constraint("Row " + str(i + 1), two_d_array[i])
        varDoms = []
        sat_tuples = []
        for v in two_d_array[i]:
            varDoms.append(v.domain())
        for t in itertools.product(*varDoms):
            if all_diff(t):
                sat_tuples.append(t)
        row_con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(row_con)

    # add column constrains
    for j in range(n):
        curr_variables = []
        for i in range(n):
            curr_variables.append(two_d_array[i][j])
        col_con = Constraint("Col " + str(j + 1), curr_variables)
        varDoms = []
        sat_tuples = []
        for v in curr_variables:
            varDoms.append(v.domain())
        for t in itertools.product(*varDoms):
            if all_diff(t):
                sat_tuples.append(t)
        col_con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(col_con)

    return csp, two_d_array


def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
    pass
