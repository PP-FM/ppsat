#pragma once

#include "emp-sh2pc/emp-sh2pc.h"
using namespace emp;
using namespace std;
#include <iostream>
// #include <fstream>
#include "formula.hpp"
#include <vector>
#include "private_stack.hpp"
#include "utils.hpp"
#include "heuristics.hpp"
#include <time.h> /* time */
#include "literal.hpp"
#include "clause.hpp"
#include "model.hpp"
#include "state.hpp"

/**
 * SAT solver.
 * Initialized with a formula, invoke "solve" to check if there's a satifying assignment of variables.
 */
class Solver
{
private:
	int ncls;
	int nvar;
	Heuristics h;

public:
	State current;
	unique_ptr<Formula> input_phi;
	unique_ptr<Formula> current_phi;
	PrivateStack<State> decisions;

	/** Construct from maximum number of variables and a formula */
	Solver(int _nvar, unique_ptr<Formula> const &_phi);

	// solver copy(){
	// 	solver solver(ncls, nvar, nltr, phi, ell);

	// }

	/** Search unit clause in the current formula. If found, update the literal in current state. */
	Bit UnitSearch();

	/** Simplify the formula according to the current literal. */
	void propagation();

	/** Check the state:
	 * * Return 0: when current formula is empty.
	 * * Return 1: when current formula conflicts with current literal.
	 * * Return 2: othersie.
	 */
	Integer check() const;

	/** Main routine of solver.
	 * It iterates at most "steps" iterations.
	 * "giantstep_test" designates whether halt after 1 iteration.
	 */
	unique_ptr<Model> solve(int steps = 100, bool giantstep_test = false);

	void print(bool test);
};
