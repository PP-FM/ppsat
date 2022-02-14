#pragma once

#include "emp-sh2pc/emp-sh2pc.h"
using namespace emp;
using namespace std;
#include <iostream>
#include <fstream>
#include <vector>
#include <memory> // unique_ptr
#include "literal.hpp"
#include "clause.hpp"
#include "model.hpp"

/**
 * Store a list of clauses.
 * Using a bitmap to indicate which clause is still active.
 */
class Formula
{
public:
	vector<unique_ptr<Clause>> cls;
	Bit *active = nullptr;

	Formula(vector<unique_ptr<Clause>> const &_cls, bool create_default = false);
	/** Construct from a string. Only for test purpose. */
	Formula(int nvar, string text);

	/** Construct a list of default clauses. The length is still cls.size() */
	unique_ptr<Formula> default_value() const;

	/** if use_rhs then return rhs, else return this. Note rhs and this must be of the same length. */
	unique_ptr<Formula> select(Bit use_rhs, unique_ptr<Formula> const &rhs) const;

	/** Count all alive variables.
	 * Here "alive" means the variable exists in at least one active clause.
	 */
	Integer num_of_alive_variables(int nvar) const;

	/** Return the random-th alive variable. Here random ranges from 0 to #(alive variables - 1). */
	Integer get_random_alive_variable(int nvar, Integer random) const;

	/** Return the max number of clauses. */
	int get_ncls() const;

	/**
	 * Scan all clauses, for each clause "cl":
	 * * If cl contains ell, deactivate it;
	 * * If cl contains -ell, remove -ell from cl;
	 * * Otherwise do nothing.
	 * Note: The algorithm guarantees there won't exist a unit clause -ell.
	 */
	void resolve_l(const Literal &ell);

	/** Call resolve_l for each literal in model. */
	void simplify(const Model &model);

	/** Check if all clauses are deactivated. */
	Bit empty() const;

	/** Check if there exists a unit clause -ell. */
	Bit conflict(const Literal &ell) const;

	void print(bool test) const;

	string toString() const;

	// formula copy() {
	// 	formula res(ncls, cls);
	// 	for (int i = 0; i < ncls; i++) res.active[i] = active[i];
	// 	return res;
	// }

	unique_ptr<Formula> copy() const;

	// TODO: delete me.
	void operator=(const Formula &f);

    tuple<Integer, Bit> get_target_literal(Integer target) const;

	~Formula();
};
