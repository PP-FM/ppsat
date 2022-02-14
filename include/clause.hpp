#pragma once

#include "literal.hpp"
#include "model.hpp"

class Clause
{

public:
    int nltr;
    int nvar;
    virtual void set_literal(int index, bool sign, Bit real) = 0;

    Clause(int _nvar, int _nltr);

	virtual Bit contain(int index, bool sign) const = 0;
	virtual unique_ptr<Clause> default_value() const = 0;
	virtual void remove(const Literal &ell) = 0;
	virtual Bit contain(const Literal &ell) const = 0;
	virtual void remove_model(const Model &model) = 0;
	virtual Bit contain_model(const Model &model) const = 0;
    virtual tuple<Integer, Bit> find_target_literal(Integer target, Integer base) const = 0;

	virtual void set(vector<int> Pindex, vector<int> Nindex, int Party) = 0;
	virtual void print(bool test) const = 0;
	virtual string toString() const = 0;
	virtual ~Clause() = default;
	virtual Bit isUnit() = 0;
	/**
	 * When this clause has only one literal, return this literal.
	 * Otherwise the return value is not meaning.
	 */
	virtual unique_ptr<Literal> get_unit_literal() const = 0;
	virtual unique_ptr<Clause> copy() const = 0;

	/** Return rhs when use_rhs is true, otherwise return this. */
	virtual unique_ptr<Clause> select(Bit b, unique_ptr<Clause> const &rhs) const = 0;
};
//	virtual Bit contain(Heuristics h, int index, bool sign) constt = 0;



/**
 * Store a clause in bitmap format.
 * pos_vars[i] and neg_vars[i] should never be 1 at the same time.
 */
class BIClause : public Clause
{
protected:
	Bit *pos_vars;
	Bit *neg_vars;
	// Bit **literals;
	// int nltr;
	virtual void set_literal(int index, bool is_pos, Bit real);
	unique_ptr<BIClause> copy_impl() const;
	//int nvar;
public:
	BIClause(int _nvar);

    /** Construct a clause from string. Only for test purpose. */
	BIClause(int _nvar, string text);

    /** Construct an empty bitmap. */
	virtual unique_ptr<Clause> default_value() const;

    /** Set this clause using bitmap by Party. */
	void set(vector<int> plist, vector<int> nlist, int Party);

    /** Check if this clause contains a literal. */
	virtual Bit contain(int index, bool is_pos) const;
	virtual Bit contain(const Literal &ell) const;

    /** Remove a literal.
	 * Note: If ell is not contained then it has no effect.
	 * Note: If -ell is contained then still no effect.
	 */
	virtual void remove(const Literal &ell);

    /** Remove all literals of a model.
	 * Note: Model is allowed to have something not contained in this clause.
	 */
	virtual void remove_model(const Model &model);

    /** Check if at least one literal from model is contained in this clause. */
	virtual Bit contain_model(const Model &model) const;

    /** Check if this clause has one and only one literal. */
	virtual Bit isUnit();

    /** Assume this clause is unit, return that unit literal. */
	virtual unique_ptr<Literal> get_unit_literal() const;

	virtual unique_ptr<Clause> select(Bit use_rhs, unique_ptr<Clause> const &rhs) const;

    virtual tuple<Integer, Bit> find_target_literal(Integer target, Integer base) const;

	virtual void print(bool test) const;

	virtual string toString() const;

    /** Deep copy */
	virtual unique_ptr<Clause> copy() const;

	~BIClause();
};



class BBClause : public BIClause
{

private:
	Integer nliteral;

public:
	BBClause(int _nvar, int _nliteral, int party = PUBLIC);

	BBClause(int _nvar, Integer _nliteral, int party = PUBLIC);

	// bbclause(int _nliteral, const bi_clause& ) : bi_clause(_nvar){
	// 	nliteral =  Integer(32, _nliteral, party);
	// }

	virtual void remove(const Literal &ell);

	virtual void set(vector<int> Pindex, vector<int> Nindex, int Party);

	virtual Bit isUnit();

	virtual unique_ptr<Clause> copy() const;

	virtual unique_ptr<Clause> select(Bit b, unique_ptr<Clause> const &rhs) const;

	virtual void print(bool test);

	virtual string toString() const { return "TODO"; }
};
//

// class int_clause: public clause{
// 	protected:
// 	//literal* literals;
// 	int nltr;
// 	int nvar;
// 	std::vector<Integer> literals;

// 	virtual void set_literal(int index, bool sign, Bit real){
// 	};

// public:
// 	Bit unit;
// 	clause(int _nltr, int _nvar){
// 	//	cout << "$$$$\n";
// 		nltr  = _nltr;
// 		nvar = _nvar;

// 	}

// 	virtual Bit contain(int index, bool sign) const= 0;
// 	virtual unique_ptr<clause> default_value() const = 0;
// 	virtual void remove(const literal& ell) = 0;
// 	virtual Bit contain(const literal& ell) const= 0;
// 	//
// 	virtual void set(vector<int> Pindex, vector<int> Nindex, int Party) = 0;
// 	virtual void print(bool test) const = 0;
// 	virtual ~clause() = default;
// 	virtual Bit isUnit()  = 0;
// 	virtual unique_ptr<literal> get_literal() const = 0;
// 	virtual unique_ptr<clause> copy() const = 0;

// 	virtual unique_ptr<clause> select(Bit b, const clause& rhs) const {
// 		unique_ptr<clause> res = copy();
//   		for (int  j = 0; j< nvar; j++){
//   			Bit b1 = (contain(j, 1) & !b) | (rhs.contain(j, 1) & b) ;
//   			Bit b0 = (contain(j, 0) & !b) | (rhs.contain(j, 0) & b);
//   			res->set_literal(j, 0, b0);
//   			res->set_literal(j, 1, b1);
//   	}

//   		//res ->  = bi_literal.select(b, );

//   		return res;
//   	}
// }
