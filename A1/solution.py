# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
from search import *  # for search engines
from lunarlockout import LunarLockoutState, Direction, \
    lockout_goal_state  # for LunarLockout specific classes and problems


# LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return 0


def heur_manhattan_distance(state):
    # OPTIONAL
    '''Manhattan distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
    # Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
    center = int((state.width - 1) / 2)
    result = 0
    for xanadu in state.xanadus:
        result += abs(xanadu[0] - center)
        result += abs(xanadu[1] - center)
    return result


def heur_L_distance(state):
    # IMPLEMENT
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    # Your function should return a sum of the L distances between each xanadu and the escape hatch.
    center = int((state.width - 1) / 2)
    result = 0
    for xanadu in state.xanadus:
        if xanadu[0] != center:
            result += 1
        if xanadu[1] != center:
            result += 1
    return result


def check_dead_corner(xanadu, other_objs):
    """
    Check whether the xanadu is position at the dead corner which it can never escape
    :param xanadu: the xanadu to check
    :param other_objs: the objects that the xanadu could potentially collide onto
    :return: True if it's in dead corner
    """
    # check whether the xanadu is at top right
    is_dead = True
    for other_obj in other_objs:
        if xanadu[0] < other_obj[0] or xanadu[1] < other_obj[1]:
            is_dead = False
            break
    if is_dead:
        return True

    # check whether the xanadu is at top left
    is_dead = True
    for other_obj in other_objs:
        if xanadu[0] > other_obj[0] or xanadu[1] < other_obj[1]:
            is_dead = False
            break
    if is_dead:
        return True

    # check whether the xanadu is at bottom right
    is_dead = True
    for other_obj in other_objs:
        if xanadu[0] < other_obj[0] or xanadu[1] > other_obj[1]:
            is_dead = False
            break
    if is_dead:
        return True

    # check whether the xanadu is at top right
    is_dead = True
    for other_obj in other_objs:
        if xanadu[0] > other_obj[0] or xanadu[1] > other_obj[1]:
            is_dead = False
            break
    if is_dead:
        return True


def check_row_col(xanadu, other_objs):
    """
    Check whether the xanadu has an object of same row or column
    :param xanadu: the xanadu to check
    :param other_objs: the objects that the xanadu could potentially collide onto
    :return: True if there is such object
    """
    for other_obj in other_objs:
        if xanadu[0] == other_obj[0] or xanadu[1] == other_obj[1]:
            return True
    return False


def heur_alternate(state):
    # IMPLEMENT
    '''a better lunar lockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.
    
    This heuristic function check for several heuristics: 
    1. Check whether the xanadu is position at the dead corner which it can never escape. If so, return infinity since there is no solution.
    2. Sum of manhattan distance is one of the key factors. We divide it by 2 to reduce its weight since it can grow large easily. We add manhattan distance / 2 to the result.
    3. If there is no object on the same row/column as a xanadu, it's consider a bad state, add 1 to the result.
    4. If there is a robot covering the escape hatch, it is consider a bad state, add 1 to the result.
    4. If there is no robot adjacent to the hatch, consider a bad state, add 1 to the result.
    5. If there is no robot adjacent on the four diagonal points next to the hatch, consider a bad state, add 1 to the result.
    
    '''
    # Your function should return a numeric value for the estimate of the distance to the goal.
    center = int((state.width - 1) / 2)
    collide_objs = state.xanadus + state.robots
    for xanadu in state.xanadus:
        # remove xanadu from this tuple
        other_objs = list(collide_objs)
        other_objs.remove(xanadu)

        if check_dead_corner(xanadu, other_objs):
            return float("inf")

    result = heur_manhattan_distance(state) / 2

    # check whether each xanadu has a piece on the same row or column, if not add 1 to result
    for xanadu in state.xanadus:
        # remove xanadu from this tuple
        other_objs = list(collide_objs)
        other_objs.remove(xanadu)

        if not check_row_col(xanadu, other_objs):
            result += 1

    # check whether there's a robot covering the hatch
    # also check whether there is a robot adjacent to the hatch
    # also check whether there is a robot on the four diagonal points next to the hatch
    is_adjacent = False
    is_diagonal = False
    for robot in state.robots:
        if robot[0] == center and robot[1] == center:
            result += 1
        if (abs(robot[0] - center) == 1) != (abs(robot[1] - center) == 1):  # the '!=' stands for xor
            is_adjacent = True
        if (abs(robot[0] - center) == 1) and (abs(robot[1] - center) == 1):
            is_diagonal = True
    if not is_adjacent:
        result += 1
    if not is_diagonal:
        result += 1

    return result


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a LunarLockoutState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound=2):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    se = SearchEngine("custom", "full")
    solution = False
    while weight > 1 and timebound > 0:
        wrapped_fval_function = (lambda sN: fval_function(sN, weight))
        se.init_search(initial_state, lockout_goal_state, heur_fn, wrapped_fval_function)

        start_time = os.times()[0]
        result = se.search(timebound)
        end_time = os.times()[0]

        if result:
            solution = result

        timebound -= end_time - start_time
        weight -= 1
    return solution


def anytime_gbfs(initial_state, heur_fn, timebound=2):
    # OPTIONAL
    '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
    '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
    '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
    '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    return 0


PROBLEMS = (
    # 5x5 boards: all are solveable
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 2),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 3),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 2),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 3),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 4),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 0),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2), (0, 4), (2, 0), (4, 0)), ((4, 4),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 0),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 3),)),
    # 7x7 BOARDS: all are solveable
    LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6, 3), (5, 4)), ((6, 2),)),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2, 6)), ((4, 6),)),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2, 6), (4, 6)), ((2, 0), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((1, 2), (0, 2), (2, 3), (4, 4), (2, 5)), ((2, 4), (3, 1), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((3, 2), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((3, 1), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (0, 2), (1, 2), (6, 4), (2, 5)), ((2, 0), (3, 0), (4, 0))),
)

if __name__ == "__main__":

    # # TEST CODE
    # solved = 0;
    # unsolved = [];
    # counter = 0;
    # percent = 0;
    timebound = 2;  # 2 second time limit for each problem
    # print("*************************************")
    # print("Running A-star")
    #
    # for i in range(len(
    #         PROBLEMS)):  # note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.
    #
    #     print("*************************************")
    #     print("PROBLEM {}".format(i))
    #
    #     s0 = PROBLEMS[i]  # Problems will get harder as i gets bigger
    #
    #     print("*******RUNNING A STAR*******")
    #     se = SearchEngine('astar', 'full')
    #     se.init_search(s0, lockout_goal_state, heur_alternate)
    #     final = se.search(timebound)
    #
    #     if final:
    #         final.print_path()
    #         solved += 1
    #     else:
    #         unsolved.append(i)
    #     counter += 1
    #
    # if counter > 0:
    #     percent = (solved / counter) * 100
    #
    # print("*************************************")
    # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    # print("*************************************")

    solved = 0;
    unsolved = [];
    counter = 0;
    percent = 0;
    print("Running Anytime Weighted A-star")

    for i in range(len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        weight = 4
        final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

        if final:
            final.print_path()
            solved += 1
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")
    #
    # solved = 0;
    # unsolved = [];
    # counter = 0;
    # percent = 0;
    # print("Running Anytime GBFS")
    #
    # for i in range(len(PROBLEMS)):
    #     print("*************************************")
    #     print("PROBLEM {}".format(i))
    #
    #     s0 = PROBLEMS[i]
    #     final = anytime_gbfs(s0, heur_alternate, timebound)
    #
    #     if final:
    #         final.print_path()
    #         solved += 1
    #     else:
    #         unsolved.append(i)
    #     counter += 1
    #
    # if counter > 0:
    #     percent = (solved / counter) * 100
    #
    # print("*************************************")
    # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    # print("*************************************")
