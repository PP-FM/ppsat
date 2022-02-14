#!/usr/bin/python
#######################################################################
# Copyright 2013 Josep Argelich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# Libraries

import sys
import random


# Classes

class Clause(object):
    """A Boolean clause randomly generated"""

    def __init__(self, num_vars, clause_length):
        """
		Initialization
		length: Clause length
		lits: List of literals
		"""
        self.length = clause_length
        self.lits = None
        self.gen_random_clause(num_vars)

    def gen_random_clause(self, num_vars):
        self.lits = []
        while len(self.lits) < self.length:  # Set the variables of the clause
            new_lit = random.randint(1, num_vars)  # New random variable
            if new_lit not in self.lits:  # If the variable is not already in the clause
                self.lits.append(new_lit)  # Add it to the clause
        for i in xrange(len(self.lits)):  # Sets a negative sense with a 50% probability
            if random.random() < 0.5:
                self.lits[i] *= -1  # Change the sense of the literal

    def show(self):
        """Prints a clause to the stdout"""

        sys.stdout.write("%s 0\n" % " ".join(map(str, self.lits)))


class CNF(object):
    """A CNF formula randomly generated"""

    def __init__(self, num_vars, num_clauses, clause_length):
        """
		Initialization
		num_vars: Number of variables
		num_clauses: Number of clauses
		clause_length: Length of the clauses
		clauses: List of clauses
		"""
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.clause_length = clause_length
        self.clauses = None
        self.gen_random_clauses()

    def gen_random_clauses(self):
        self.clauses = []
        for _ in xrange(self.num_clauses):
            clause = Clause(self.num_vars, self.clause_length)
            self.clauses.append(clause)

    def show(self):
        """Prints the formula to the stdout"""

        sys.stdout.write("c Random CNF formula\n")
        sys.stdout.write("p cnf %d %d\n" % (self.num_vars, self.num_clauses))
        for clause in self.clauses:
            clause.show()


# Main

def main():
    """A random CNF generator"""

    # Check parameters
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        sys.exit("Use: %s <num-vars> <num-clauses> <clause-length> [<random-seed>]" % sys.argv[0])

    try:
        num_vars = int(sys.argv[1])
    except TypeError:
        sys.exit("ERROR: Number of variables not an integer (%s)." % sys.argv[1])
    if num_vars < 1:
        sys.exit("ERROR: Number of variables must be >= 1 (%d)." % num_vars)

    try:
        num_clauses = int(sys.argv[2])
    except TypeError:
        sys.exit("ERROR: Number of clauses not an integer (%s)." % sys.argv[2])
    if num_vars < 1:
        sys.exit("ERROR: Number of clauses must be >= 1 (%d)." % num_clauses)

    try:
        clause_length = int(sys.argv[3])
    except TypeError:
        sys.exit("ERROR: Length of clauses not an integer (%s)." % sys.argv[3])
    if num_vars < 1:
        sys.exit("ERROR: Length of clauses must be >= 1 (%d)." % clause_length)

    if len(sys.argv) > 4:
        try:
            seed = int(sys.argv[4])
        except TypeError:
            sys.exit("ERROR: Seed number not an integer (%s)." % sys.argv[4])
    else:
        seed = None

    # Initialize random seed (current time)
    random.seed(seed)
    # Create a solver instance with the problem to solve
    cnf_formula = CNF(num_vars, num_clauses, clause_length)
    # Show formula
    cnf_formula.show()


if __name__ == '__main__':
    main()
