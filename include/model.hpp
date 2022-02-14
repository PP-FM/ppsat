
#pragma once
#include "emp-sh2pc/emp-sh2pc.h"
#include <memory> // unique_ptr
#include "literal.hpp"
using namespace emp;
using namespace std;

/**
 * Store a list of literals in bitmap format.
 */
class Model
{
private:
    int nvar;
    Bit *pos_vars;
    Bit *neg_vars;

public:
    /** Construct an empty bitmap. */
    Model(int _nvar);
    /** Construct from bitmap. */
    Model(Bit *_pos_var, Bit *_neg_var, int _nvar);
    /** Construct from a string. Only for test purpose. */
    Model(int nvar, string text);

    /** Construct an empty bitmap. */
    unique_ptr<Model> default_value() const;

    // virtual void set_index_s(Integer index, Bit is_pos, Bit real = Bit(1, PUBLIC)) = 0;
    // virtual void set_index_p(int index, bool is_pos) = 0;
    // void set_index(int index, bool is_pos, Bit real);

    /** Insert a literal to model when real is true. */
    void update_index(int index, bool is_pos, Bit real);

    unique_ptr<Model> copy() const;

    void print(bool test) const;
    string toString() const;
    /** Check if model has designated literal. */
    Bit hasIndex(int index, bool is_pos) const;

    // virtual tuple<Integer, Bit> get_index() const = 0;

    /** if use_rhs then return rhs, else return this. Note rhs and this must have the same nvar. */
    unique_ptr<Model> select(Bit b, unique_ptr<Model> const &rhs) const;

    /* Return the union of two models. */
    unique_ptr<Model> operator|(const Literal &rhs) const;

    /** Negate all literals. (Effectly make no change when model is empty.) */
    unique_ptr<Model> flip() const;

    // virtual unique_ptr<literal> operator&(const literal& rhs) const {
    // 	auto res = rhs.copy();
    // 	for(int i = 0; i < nvar; ++i){
    // 		res->set_index(i, 1, res->isIndex(i, 1) & isIndex(i, 1));
    // 		res->set_index(i, 0, res->isIndex(i, 0) & isIndex(i, 0));
    // 	}
    // 	return res;
    // };
    //virtual literal* mux(Bit b, literal* ell1, literal* ell2) const = 0;
    ~Model();
    //virtual literal operator^(const literal &ref) = 0;
};
