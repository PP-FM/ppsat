#pragma once
#include <memory>
using namespace std;
#include "literal.hpp"
#include "model.hpp"

/**
 * State consists of:
 * * ell: assignment of one variable in current round.
 * * model: stores some variables' assignments.
 */
class State
{
//private:
//	unique_ptr<Literal> ell = nullptr;
//	unique_ptr<Model> model = nullptr;
public:
    unique_ptr<Literal> ell = nullptr;
    unique_ptr<Model> model = nullptr;
	State();

	/** When create_default is true, create a default state using the nvar of current ell and model. */
	State(unique_ptr<Literal> const &_ell, unique_ptr<Model> const &_model, bool create_default = false);
	/** Construct from nvar and strings. Only for test purpose. */
	State(int nvar, string ell_text, string model_text);

	/** Copy constructor. */
	State(const State &other);

	/** Copy assignment. */
	State &operator=(const State &s);

	// state& operator =(state &&s) {
	// 	phi = move(s.phi);
	// 	ell = move(s.ell);
	// 	model = move(s.model);
	// 	return *this;
	// }

	// Integer count(int nvar) const{
	// 	return phi -> alive_literal(nvar);
	// }

	/** Getters and setters. */
	unique_ptr<Literal> get_literal() const;
	unique_ptr<Model> get_model() const;
	void set_literal(unique_ptr<Literal> const &_ell);
	void set_model(unique_ptr<Model> const &_model);

	/** if use_rhs then return rhs, else return this. Note the models and ells in rhs and this must have the same nvar. */
	State select(Bit use_rhs, const State &rhs) const;

	string toString() const;
	// void print(bool test) const;

	/** Construct an empty model and a default ell. */
	// TODO: create a static version
	State default_value() const;

	/** Construct a new state whose ell is flipped. */
	State flip() const;

	State copy() const;
};