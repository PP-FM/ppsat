
#pragma once
#include "emp-sh2pc/emp-sh2pc.h"
#include <memory> // unique_ptr
using namespace emp;
using namespace std;

// TODO: merge this class with bi_literal calss.
class Literal
{

public:
	int nvar;
	Literal(int _nvar)
	{
		nvar = _nvar;
	}
	virtual unique_ptr<Literal> default_value() const = 0;
	virtual void set_index_s(Integer index, Bit is_pos, Bit real = Bit(1, PUBLIC)) = 0;
	virtual void set_index_p(int index, bool is_pos) = 0;
	virtual void set_index(int index, bool is_pos, Bit real) = 0;
	virtual unique_ptr<Literal> flip() const = 0;
	virtual unique_ptr<Literal> copy() const = 0;
	virtual void print(bool test) const = 0;
  virtual string toString() const = 0;
	virtual Bit isIndex(int index, bool is_pos) const = 0;
	virtual tuple<Integer, Bit> get_index() const = 0;
	//virtual unique_ptr<literal> select(Bit b) const = 0;
	virtual unique_ptr<Literal> select(Bit b, unique_ptr<Literal> const &rhs) const = 0;

  // TODO: delete me
  unique_ptr<Literal> operator|(const Literal &rhs) const;


	// virtual unique_ptr<literal> operator&(const literal& rhs) const {
	// 	auto res = rhs.copy();
	// 	for(int i = 0; i < nvar; ++i){
	// 		res->set_index(i, 1, res->isIndex(i, 1) & isIndex(i, 1));
	// 		res->set_index(i, 0, res->isIndex(i, 0) & isIndex(i, 0));
	// 	}
	// 	return res;
	// };
	//virtual literal* mux(Bit b, literal* ell1, literal* ell2) const = 0;
	virtual ~Literal() = default;
	//virtual literal operator^(const literal &ref) = 0;
};



/**
 * Store a literal in bitmap format.
 * Only one or zero bit in pos_vars and neg_vars can be 1, others are zero.
 * When there's no 1 in the bitmap, the computation involving it will still
 * be executed, but will not have meaning effect.
 */
class BILiteral : public Literal
{

private:
  Bit *pos_vars;
  Bit *neg_vars;

  void update_index(int index, bool is_pos, Bit real);

public:
  /** Create an empty bitmap. */
  BILiteral(int nvar);

  BILiteral(Bit *_pos_var, Bit *_neg_var, int _nvar);

  BILiteral(Bit **_ind, int _nvar);

  BILiteral(int nvar, int index, bool is_pos);

  BILiteral(int nvar, Integer index, Bit is_pos);

  /** Construct from a string. Only for test purpose. */
  BILiteral(int nvar, string text);

  /** Construct an empty bitmap. */
  virtual unique_ptr<Literal> default_value() const;

  /** Deep copy */
  virtual unique_ptr<Literal> copy() const;

  /** Return rhs when use_rhs is true, otherwise return this. */
  virtual unique_ptr<Literal> select(Bit use_rhs, unique_ptr<Literal> const &rhs) const;

  /** Set this as a new literal when real is true. */
  virtual void set_index(int index, bool is_pos, Bit real);
  // TODO: rename this two methods into set_index
  virtual void set_index_s(Integer index, Bit is_pos, Bit real);
  /** Set this to a new literal. */
  virtual void set_index_p(int index, bool is_pos);

  /** Check equality. */
  virtual Bit isIndex(int index, bool is_pos) const;

  virtual tuple<Integer, Bit> get_index() const;

  /** Negate this literal. (Effectly make no change when this is default value.) */
  unique_ptr<Literal> flip() const;

  virtual void print(bool test) const;

  virtual string toString() const;

  ~BILiteral();
};
