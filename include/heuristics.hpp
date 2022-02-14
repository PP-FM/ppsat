#pragma once

#include "state.hpp"
#include "formula.hpp"
#include <time.h>       /* time */
using namespace std;


class Heuristics {
    int nvar = 0;
    int ncls = 0;


public:
     Heuristics();

    Heuristics(int _nvar, int _ncls);
    unique_ptr<Literal> weight_random(const Formula&  input_phi,  const State& state) const;

    unique_ptr<Literal> random(const Formula&  input_phi,  const State& s) const ;


    unique_ptr<Literal> det_freq(const Formula& input_phi, const State& s) const ;

};