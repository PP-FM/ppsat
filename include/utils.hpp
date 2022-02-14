#pragma once

#include "clause.hpp"
#include "literal.hpp"
#include "formula.hpp"

enum CLAUSE {BICLAUSE, BBCLAUSE};

enum LITERAL {BILITERAL};


unique_ptr<Formula> generate( int ncls, int nvar, int nltr, CLAUSE ct, LITERAL lt);

Integer findbound(Integer input);

unique_ptr<Formula> ReadFormulae(string filename);

Integer get_alive_weighted_literal(const Formula& phi) ;

Integer count_alive_literal(const Clause& c ) ;