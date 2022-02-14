#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import sys


class Formula(object):
    def __init__(self, clauses, n_vars):

        # [clause, clause,..]
        self.simple = clauses

        # { literal : [clause, ..] , literal : [clause , ..]
        self.linked = {}

        self.n_vars = n_vars

        # [[[clause1, unit_deleted], [clause2, unit_deleted], ..],..]
        self.modified = []

        self.extra_restores = 0

        self.assignment = []
        self.has_contradiction = False

        for clause in self.simple:
            for literal in clause:
                if literal in self.linked:
                    self.linked[literal].append(clause)
                else:
                    self.linked[literal] = [clause]

        for literal in xrange(1,n_vars +1):
            if literal not in self.linked:
                self.linked[literal] = []
            if -literal not in self.linked:
                self.linked[-literal] = []


    def solution_found(self):
        return True if not sum(1 for l in self.simple if l) else False

    def restore(self):
        unit_modified = self.modified.pop()
        # Undo the last modifications
        for clause, variable in unit_modified:
            clause.append(variable)
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
        clauses.append(clause)
    return Formula(clauses, int(n_vars))


def bcp(formula, unit):
    formula.modified.append([])

    for clause in formula.linked[unit]:
        if unit in clause:
            for literal_index in xrange(len(clause)):
                formula.modified[-1].append([clause, clause[-1]])
                clause.pop()

    if -unit in formula.linked:

        for clause in formula.linked[-unit]:

            if -unit in clause:
                formula.modified[-1].append([clause, -unit])
                clause.remove(-unit)

                if not clause:
                    formula.has_contradiction = True
                    return
    return


def get_weighted_counter(linked,weight=2):
    counter = {}
    for literal in linked:
        for clause in linked[literal]:
            if literal in clause:
                if abs(literal) in counter:
                    counter[abs(literal)] += weight ** - len(clause)
                else:
                    counter[abs(literal)] = weight ** - len(clause)
    return counter



def unit_propagation(formula):
    unit_clauses = [c for c in formula.simple if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        bcp(formula, unit)
        formula.extra_restores += 1
        formula.assignment.append(unit)
        if formula.has_contradiction or formula.solution_found():
            return
        unit_clauses = [c for c in formula.simple if len(c) == 1]
    return


def backtracking(formula):

    unit_propagation(formula)

    if formula.has_contradiction:
        formula.has_contradiction = False
        return []
    if formula.solution_found():
        return formula.assignment

    variable = jeroslow_wang_2_sided(formula)

    bcp(formula, variable)

    formula.assignment.append(variable)
    backtracking(formula)
    if not formula.solution_found():
        formula.restore()
        for _ in xrange(formula.extra_restores):
            formula.restore()
        formula.extra_restores = 0

    if not formula.solution_found():
        bcp(formula, -variable)
        formula.assignment.append(-variable)
        backtracking(formula)
        if not formula.solution_found():
            formula.restore()
            for _ in xrange(formula.extra_restores):
                formula.restore()
            formula.extra_restores = 0
    return formula.assignment


def jeroslow_wang_2_sided(formula):
    counter = get_weighted_counter(formula.linked)
    return max(counter, key=counter.get)

# Main

def main():


    formula = parse(sys.argv[1])

    solution = backtracking(formula)

    if solution:
        solution += [x for x in range(1, formula.n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    main()
