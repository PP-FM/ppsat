#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import sys


class Formula(object):
    def __init__(self, clauses, n_vars):

        # [[clause,True/False],[clause,True/False],..]
        self.simple = clauses

        # { literal : [[clause, True/False], ..] , literal : [[clause, True/False], ..] , ..]
        self.linked = {}

        self.n_vars = n_vars

        # [[clause1, clause2, ..],..]
        self.false_flags = []

        # [[[clause1, unit_deleted], [clause2, unit_deleted], ..],..]
        self.modified = []

        self.extra_restores = 0

        self.assignment = []
        self.has_contradiction = False
        for clause in self.simple:
            for literal in clause[0]:
                if literal in self.linked:
                    self.linked[literal].append(clause)
                else:
                    self.linked[literal] = [clause]
        # wip
        '''
        for literal in xrange(1, n_vars + 1):
            if literal not in self.linked:
                self.linked[literal] = [[[], False]]
            if -literal not in self.linked:
                self.linked[-literal] = [[[], False]]
        '''

    def solution_found(self):
        return True if not len(self.active_clauses()) else False

    def active_clauses(self):
        return Formula.filter_active_clauses(self.simple)

    @staticmethod
    def filter_active_clauses(clauses):
        return list(filter(lambda x: x[1], clauses))

    def restore(self):
        if not self.solution_found():
            unit_modified = self.modified.pop()
            unit_false_flags = self.false_flags.pop()
            # Undo the last false flags
            for clause in unit_false_flags:
                clause[1] = True
            # Undo the last modifications
            for clause, variable in unit_modified:
                clause[0].append(variable)
            # Undo the last assignment
            return self.assignment.pop()


def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append([clause, True])
    return Formula(clauses, int(n_vars))


def bcp(formula, unit):
    formula.modified.append([])
    formula.false_flags.append([])

    for clause in Formula.filter_active_clauses(formula.linked[unit]):
        clause[1] = False
        formula.false_flags[-1].append(clause)

    if -unit in formula.linked:

        for clause in Formula.filter_active_clauses(formula.linked[-unit]):

            formula.modified[-1].append([clause, -unit])
            clause[0].remove(-unit)

            if not clause[0]:
                formula.has_contradiction = True
                return

    return

# wip
def get_weighted_counter(linked, weight=2):
    counter = {}
    for literal, clauses in linked.items():
        for clause in clauses:
            if clause[1]:
                if literal in clause[0]:
                    if literal in counter:
                        counter[literal] += weight ** - len(clause[0])
                    else:
                        counter[literal] = weight ** - len(clause[0])
    return counter

def get_weighted_abs_counter(linked, weight=2):
    counter = {}
    for literal, clauses in linked.items():
        for clause in clauses:
            if clause[1]:
                if literal or -literal in clause[0]:
                    if abs(literal) in counter:
                        counter[abs(literal)] += weight ** - len(clause[0])
                    else:
                        counter[abs(literal)] = weight ** - len(clause[0])
    return counter

# wip
def pure_literal(formula):
    pures = []

    for literal in formula.linked:
        if literal not in formula.assignment and -literal not in formula.assignment:
            if -literal not in formula.linked \
                    or not Formula.filter_active_clauses(formula.linked[-literal]):
                pures.append(literal)
    for pure in pures:
        formula.extra_restores += 1
        formula.assignment.append(pure)
        bcp(formula, pure)


def unit_propagation(formula):
    unit_clauses = [c[0] for c in formula.active_clauses() if len(c[0]) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        bcp(formula, unit[0])
        formula.extra_restores += 1
        formula.assignment.append(unit[0])
        if formula.has_contradiction or formula.solution_found():
            return
        unit_clauses = [c[0] for c in formula.active_clauses() if len(c[0]) == 1]
    return


def backtracking(formula, selection_heuristic):
    # pure_literal(formula)
    unit_propagation(formula)
    if len(list(set(formula.assignment))) != len(formula.assignment):
        sys.exit("Error")

    if formula.has_contradiction:
        formula.has_contradiction = False
        return []
    if formula.solution_found():
        return formula.assignment

    variable = selection_heuristic(formula)

    bcp(formula, variable)

    formula.assignment.append(variable)
    backtracking(formula, selection_heuristic)

    formula.restore()
    for _ in xrange(formula.extra_restores):
        formula.restore()
    formula.extra_restores = 0

    if not formula.solution_found():
        bcp(formula, -variable)
        formula.assignment.append(-variable)
        backtracking(formula, selection_heuristic)
        formula.restore()
        for _ in xrange(formula.extra_restores):
            formula.restore()
        formula.extra_restores = 0
    return formula.assignment


# Branching heuristics

def heuristics_dict(heuristic):
    heuristics = {
        'JW'    : jeroslow_wang,
        'JW2S'  : jeroslow_wang_2_sided
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Not valid heuristic.".format(heuristic) +
                 "\nValid heuristics: {}".format(heuristics.keys()))


def jeroslow_wang(formula):
    counter = get_weighted_counter(formula.linked)
    return max(counter, key=counter.get)

def jeroslow_wang_2_sided(formula):
    counter = get_weighted_abs_counter(formula.linked)
    return max(counter, key=counter.get)

# Main

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("Use: %s <cnf_file> [<branching_heuristic>]" % sys.argv[0])

    if len(sys.argv) == 3:
        heuristic = heuristics_dict(sys.argv[2])
    else:
        heuristic = jeroslow_wang

    formula = parse(sys.argv[1])

    solution = backtracking(formula, heuristic)

    if solution:
        solution += [x for x in range(1, formula.n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    main()
