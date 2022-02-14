#include <memory>
using namespace std;
#include "state.hpp"

State::State()
{
}

State::State(unique_ptr<Literal> const &_ell, unique_ptr<Model> const &_model, bool create_default)
{
	ell = create_default ? _ell->default_value() : _ell->copy();
	model = create_default ? _model->default_value() : _model->copy();
}

State::State(int nvar, string ell_text, string model_text)
{
	ell = make_unique<BILiteral>(nvar, ell_text);
	model = make_unique<Model>(nvar, model_text);
}

// copy constructor
State::State(const State &other)
{
	ell = other.ell->copy();
	model = other.model->copy();
}

// copy assignment
State &State::operator=(const State &s)
{
	ell = s.ell->copy();
	model = s.model->copy();
	return *this;
}

// state& operator =(state &&s) {
// 	phi = move(s.phi);
// 	ell = move(s.ell);
// 	model = move(s.model);
// 	return *this;
// }

// Integer count(int nvar) const{
// 	return phi -> alive_literal(nvar);
// }

unique_ptr<Literal> State::get_literal() const
{
	return ell->copy();
}

unique_ptr<Model> State::get_model() const
{
	return model->copy();
}

void State::set_literal(unique_ptr<Literal> const &_ell)
{
	ell = _ell->copy();
}

void State::set_model(unique_ptr<Model> const &_model)
{
	model = _model->copy();
}

State State::select(Bit use_rhs, const State &rhs) const
{
	State res(ell, model);
	auto tmp_ell = ell->select(use_rhs, rhs.ell);
	auto tmp_model = model->select(use_rhs, rhs.model);
	return State(tmp_ell, tmp_model);
}

string State::toString() const
{
	return "[ell: " + ell->toString() + ", model: " + model->toString() + "]";
}

State State::default_value() const
{
	return State(ell, model, true);
}

State State::flip() const
{
	return State(ell->flip(), model);
}

State State::copy() const
{
	return State(ell, model);
}
