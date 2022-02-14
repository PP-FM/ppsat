#!/usr/bin/env python
import sys


def test_formula(formula, solution):
    solution = set(solution)
    for clause in formula:
        if set(clause).isdisjoint(solution):
            return 'Not valid solution'
    return 'Valid solution'


def parse_formula(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses


def parse_solution(filename):
    for line in open(filename):
        if line.startswith('c'):
            continue
        elif line.startswith('s'):
            if line.split()[1] == 'SATISFIABLE':
                continue
            else:
                return []
        elif line.startswith('v'):
            return map(int, line.split()[1:-1])
    return []


def main():
    if not len(sys.argv) == 3:
        sys.exit("Use: %s <formula_file> <solution_file>" % sys.argv[0])

    solution = parse_solution(sys.argv[2])
    if solution:
        formula = parse_formula(sys.argv[1])
        print test_formula(formula, solution)

    else:
        print 'Not able to validate UNSAT'


if __name__ == '__main__':
    main()
