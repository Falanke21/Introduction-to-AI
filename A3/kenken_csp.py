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


def construct_variables(n):
    variables = []
    two_d_array = []

    # construct variables
    for i in range(n):
        two_d_array.append([])
        for j in range(n):
            var = Variable(str(i + 1) + str(j + 1), range(1, n + 1))
            variables.append(var)
            two_d_array[i].append(var)
    return variables, two_d_array


def all_diff(t):
    """
    Helper for nary_ad_grid
    """
    if len(set(t)) == len(t):
        return True
    return False


def get_sat_tuples(curr_variables, n):
    return list(itertools.permutations(range(1, n+1), r=len(curr_variables)))


def binary_ne_grid(kenken_grid):
    n = kenken_grid[0][0]
    variables, two_d_array = construct_variables(n)

    csp = CSP("kenken", variables)

    # for each variable from i, j = 1 to n - 1(inclusive),
    # constrains diff with all cells below and all cells to the right.
    for i in range(n):
        for j in range(n):
            for k in range(i+1, n):
                curr_variables = [two_d_array[i][j], two_d_array[k][j]]
                verti_con = Constraint(str(i+1) + str(j+1) + " and " + str(k+1) + str(j+1), curr_variables)
                sat_tuples = get_sat_tuples(curr_variables, n)
                verti_con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(verti_con)

            for k in range(j+1, n):
                curr_variables = [two_d_array[i][j], two_d_array[i][k]]
                hori_con = Constraint(str(i+1) + str(j+1) + " and " + str(i+1) + str(k+1), curr_variables)
                sat_tuples = get_sat_tuples(curr_variables, n)
                hori_con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(hori_con)
    return csp, two_d_array


def nary_ad_grid(kenken_grid):
    n = kenken_grid[0][0]
    variables, two_d_array = construct_variables(n)

    csp = CSP("kenken", variables)

    # add row constrains
    for i in range(n):
        row_con = Constraint("Row " + str(i + 1), two_d_array[i])
        sat_tuples = get_sat_tuples(two_d_array[i], n)
        row_con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(row_con)

    # add column constrains
    for j in range(n):
        curr_variables = []
        for i in range(n):
            curr_variables.append(two_d_array[i][j])

        col_con = Constraint("Col " + str(j + 1), curr_variables)
        sat_tuples = get_sat_tuples(curr_variables, n)
        col_con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(col_con)

    return csp, two_d_array


def get_cage_sat_tuples(requirement, current_variables, goal_value):
    varDoms = []
    for v in current_variables:
        varDoms.append(v.domain())

    sat_tuples = []
    for t in itertools.product(*varDoms):
        # NOTICE use of * to convert the list v to a sequence of arguments to product
        if requirement(t, goal_value):
            sat_tuples.append(t)
    return sat_tuples


def addition(t, goal_value):
    if sum([item for item in t]) == goal_value:
        return True
    return False


def subtraction(t, goal_value):
    # while len(t) != 1:
    #     temp = (t[0] - t[1],) + (t[2:])
    #     t = temp
    # return t[0] == goal_value
    largest = max(t)
    temp = largest

    t = list(t)
    t.remove(largest)

    for value in t:
        temp -= value
    return temp == goal_value


def multiplication(t, goal_value):
    acc = 1
    for item in t:
        acc *= item
    return acc == goal_value


def division(t, goal_value):
    # while len(t) != 1:
    #     temp = (t[0] / t[1],) + (t[2:])
    #     t = temp
    # return t[0] == goal_value
    largest = max(t)
    temp = largest

    t = list(t)
    t.remove(largest)

    for value in t:
        temp /= value
    return temp == goal_value


def kenken_csp_model(kenken_grid):
    csp, two_d_array = binary_ne_grid(kenken_grid)
    kenken_cages = kenken_grid[1:]
    for cage in kenken_cages:
        operation = cage[-1]
        curr_variables = []
        for number in cage[0:-2]:
            number = str(number)
            i = int(number[0]) - 1
            j = int(number[1]) - 1
            curr_variables.append(two_d_array[i][j])

        sat_tuples = []
        con_name = ""
        if operation == 0:  # +
            sat_tuples = get_cage_sat_tuples(addition, curr_variables, cage[-2])
            con_name = "Add"
        elif operation == 1:  # -
            sat_tuples = get_cage_sat_tuples(subtraction, curr_variables, cage[-2])
            con_name = "Sub"
        elif operation == 2:  # /
            sat_tuples = get_cage_sat_tuples(division, curr_variables, cage[-2])
            con_name = "Div"
        elif operation == 3:  # *
            sat_tuples = get_cage_sat_tuples(multiplication, curr_variables, cage[-2])
            con_name = "Multi"

        con = Constraint(con_name, curr_variables)
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    return csp, two_d_array
