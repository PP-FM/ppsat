#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import random
import sys


def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars)


def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def get_weighted_counter(formula, weight=2):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter


def get_weighted_abs_counter(formula, weight=2):
    counter = {}
    for clause in formula:
        for literal in clause:
            literal = abs(literal)
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter

def get_difference_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                if literal > 0:
                    counter[literal] += 1
                else:
                    counter[-literal] += - 1
            else:
                if literal > 0:
                    counter[literal] = 1
                else:
                    counter[-literal] = - 1
    return counter

def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []
    for literal, _ in counter.items():
        if -literal not in counter:
            pures.append(literal)
    for pure in pures:
        formula = bcp(formula, pure)
    assignment += pures
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def backtracking(formula, assignment, heuristic):
    # print assignment
    # formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment # + pure_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = heuristic(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable], heuristic)
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable], heuristic)

    return solution


# Branching heuristics

def heuristics_dict(heuristic):
    heuristics = {
        'JW'    : jeroslow_wang,
        'RAN'   : random_selection,
        'MO'    : most_often,
        'SPC'   : shortest_positive_clause,
        'FRE'   : freeman,
        'JW2S'  : jeroslow_wang_2_sided
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Not valid heuristic.".format(heuristic) +
                 "\nValid heuristics: {}".format(heuristics.keys()))


def random_selection(formula):
    counter = get_counter(formula)
    return random.choice(counter.keys())


def jeroslow_wang(formula):
    counter = get_weighted_counter(formula)
    return max(counter, key=counter.get)

def jeroslow_wang_2_sided(formula):
    counter = get_weighted_abs_counter(formula)
    return max(counter, key=counter.get)

def most_often(formula):
    counter = get_counter(formula)
    return max(counter, key=counter.get)


def shortest_positive_clause(formula):
    min_len = sys.maxint
    best_literal = 0
    for clause in formula:
        negatives = sum(1 for literal in clause if literal < 0)
        if not negatives and len(clause) < min_len:
            best_literal = clause[0]
            min_len = len(clause)
    if not best_literal:
        return formula[0][0]
    return best_literal

def freeman(formula):
    counter = get_difference_counter(formula)
    max_p_literal = max(counter, key=counter.get)
    max_n_literal = min(counter, key=counter.get)
    if counter[max_p_literal] >= abs(counter[max_n_literal]):
        return max_p_literal
    return max_n_literal

def max_key_value(counter):
    keys = counter.keys()
    values = counter.values()
    return keys[values.index(max(values))]

# Main

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("Use: %s <cnf_file> [<branching_heuristic>]" % sys.argv[0])

    if len(sys.argv) == 3:
        heuristic = heuristics_dict(sys.argv[2])
    else:
        heuristic = jeroslow_wang

    clauses, n_vars = parse(sys.argv[1])

    solution = backtracking(clauses, [], heuristic)

    if solution:
        solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'

if __name__ == '__main__':
    main()
