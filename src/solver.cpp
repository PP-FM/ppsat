#include "emp-sh2pc/emp-sh2pc.h"
using namespace emp;
using namespace std;
#include <iostream>
#include "formula.hpp"
#include <vector>
#include "private_stack.hpp"
#include "utils.hpp"
#include "heuristics.hpp"
#include <time.h> // time
#include "literal.hpp"
#include "clause.hpp"
#include "state.hpp"
#include "solver.hpp"


Solver::Solver(int _nvar, unique_ptr<Formula> const &_phi)
{
	ncls = _phi->get_ncls();
	nvar = _nvar;

	unique_ptr<Literal> _ell = make_unique<BILiteral>(nvar);
	unique_ptr<Model> _model = make_unique<Model>(nvar);

	decisions.init(nvar * 2 , State(_ell, _model, true));
/*
 * h is a set of heuristics that are used for guessing literals.
 * for now, available heuristics are weighted-random, random, deterministic. For more information please see our paper.
*/
	h = Heuristics(nvar, ncls);
	current = State(_ell, _model);
	input_phi = _phi->copy();
	current_phi = _phi->copy();
}

Bit Solver::UnitSearch()
{
	Bit has_unit(0, PUBLIC);

	for (int i = 0; i < ncls; i++)
	{
		// Check if current clause is unit.
        unique_ptr<Clause> cl = current_phi->cls[i]->copy();

		Bit cl_is_unit_and_active = cl->isUnit() & current_phi->active[i];
		unique_ptr<Literal> unit_ell = cl->get_unit_literal();

		// Update current ell if found a unit.
		unique_ptr<Literal> ell_tmp = current.get_literal()->select(cl_is_unit_and_active, unit_ell);
		current.set_literal(ell_tmp);

		has_unit = has_unit | cl_is_unit_and_active;
	}
	return has_unit;
}

void Solver::propagation()
{
	// Propagate current literal.
	current_phi->resolve_l(*(current.get_literal()));

	// Add literal to model.
	unique_ptr<Model> model = *(current.get_model()) | *(current.get_literal());
	current.set_model(model);
}

Integer Solver::check() const
{
	Integer sigma(2, 2, PUBLIC);
	Bit is_empty = current_phi->empty();
	Bit is_conflict = current_phi->conflict(*current.get_literal());

	sigma = sigma.select(is_empty, Integer(2, 0, PUBLIC));
	sigma = sigma.select(is_conflict, Integer(2, 1, PUBLIC));

	return sigma;
}

unique_ptr<Model> Solver::solve(int steps, bool giantstep_test)
{
	bool test = false;
	int i = 0;
	Bit conflict(0, PUBLIC);

    chrono::steady_clock sc;
    auto start = sc.now();
    auto end = sc.now();
    auto time_span = static_cast<chrono::duration<double>>(end - start);
    float s = 0;
    float  e = 0;


    while (i < steps)
	{

		State backtrack(current.get_literal(), current.get_model(), true);

		if (i > 0)
		{
            start  = sc.now( )  ;
			Integer sigma = check();
            end =   sc.now( );
            time_span = static_cast<chrono::duration<double>>(end - start);

            cout << "check: "<< time_span.count()  <<" seconds\n";

            Bit sat = sigma.equal(Integer(2, 0, PUBLIC));

			// Found a satisfying model, return
			if (sat.reveal<bool>() and !giantstep_test)
			{
				cout << "sat" << endl;
				cout << "round:" << i << endl;
				return current.get_model();
			}

			conflict = sigma.equal(Integer(2, 1, PUBLIC));

            start  = sc.now( );
            try
			{
				// When conflict, backtrack to last state and flip its literal.
				// Otherwise, "backtrack" is assigned with default state.
				backtrack = decisions.pop(conflict).flip();
			}
			catch (char const *msg)
			{
				// When "decisions" is empty, catch this expection and report unsat.
				cout << "unsat: " << msg << endl;
                cout << "round:" << i << endl;
                if (!giantstep_test)
					return current.get_model()->default_value();
			}

            end =   sc.now( );

            time_span = static_cast<chrono::duration<double>>(end - start);

            cout<<  "backtrack: "<< time_span.count() <<" seconds\n";

            start  = sc.now( )  ;

            propagation();

            end =   sc.now( );

            time_span = static_cast<chrono::duration<double>>(end - start);

            cout<< "propagation: "<< time_span.count() <<" seconds\n";

        }

		if (giantstep_test and i > 0)
			return current.get_model();

		// If there's a unit clause, replace current literal with it.
        start  = sc.now( )  ;
        Bit has_unit = UnitSearch();
        end =   sc.now( );
        time_span = static_cast<chrono::duration<double>>(end - start);
        cout << "unit search: "<< time_span.count() <<" seconds\n";


        start  = sc.now( )  ;

        /*
		 * Heuristically guess a literal.
		 * please change to other heuristics by replacing weight_random with the rest.
        */

		unique_ptr<Literal> guess = h.weight_random(*input_phi, current);
        // If there's no unit clause and no conflict, record the guess into "decisions".
		decisions.push(State(guess->copy(), current.get_model()), !has_unit & !conflict);
        end =   sc.now( );
        time_span = static_cast<chrono::duration<double>>(end - start);
        cout<<  "guess: "<< time_span.count() <<" seconds\n";
        s =   CircuitExecution::circ_exec->num_and();

        start  = sc.now( )  ;

		// ell1 = unit literal when there's one, otherwise use the guessed literal.
		unique_ptr<Literal> ell1 = (current.get_literal())->select(!has_unit, guess);
		current.set_literal(ell1);

		// When there's a conflict, we have already backtracked to a previous state.
		// Now recompute the current formula from initial formula and backtracked model.
		// Note: this formula is only used when conflict occurs.
		unique_ptr<Formula> backtrack_formula = input_phi->copy();
		backtrack_formula->simplify(*backtrack.get_model());

		// If conflict occurs, update current state and formula according to backtrack.
		unique_ptr<Formula> phi2 = current_phi->select(conflict, backtrack_formula);
		unique_ptr<Literal> ell2 = current.get_literal()->select(conflict, (backtrack.get_literal()));
		unique_ptr<Model> model2 = current.get_model()->select(conflict, (backtrack.get_model()));
		current_phi = phi2->copy();
		current.set_literal(ell2);
		current.set_model(model2);
        e = CircuitExecution::circ_exec->num_and();
        end =   sc.now( );
        time_span = static_cast<chrono::duration<double>>(end - start);
        cout << "mux: "<< time_span.count() <<" seconds\n";

        i = i + 1;
	}

	return current.get_model()->default_value();
}

void Solver::print(bool test)
{
	if (!test)
		return;
	cout << "formula: \n";
	current_phi->print(test);
	cout << "literal: \n";
	current.get_literal()->print(test);
	cout << "model: \n";
	current.get_model()->print(test);
};
