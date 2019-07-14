# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_mrv(csp):
    variables = csp.get_all_unasgn_vars()
    result_var = variables[0]
    for i in range(1, len(variables)):
        if variables[i].cur_domain_size() < result_var.cur_domain_size():
            result_var = variables[i]
    return result_var


def val_lcv(csp, var):
    value_score_pair = []
    domain = var.cur_domain()
    cons = csp.get_cons_with_var(var)
    for value in domain:
        rule_out_tuples = []
        var.assign(value)
        for con in cons:
            for other_var in con.get_unasgn_vars():
                for other_val in other_var.cur_domain():
                    if (not con.has_support(other_var, other_val)) and (other_var, other_val) not in rule_out_tuples:
                        rule_out_tuples.append((other_var, other_val))
        var.unassign()
        value_score_pair.append((value, len(rule_out_tuples)))

    value_score_pair.sort(key=lambda element: element[1])
    result = [item[0] for item in value_score_pair]
    return result
