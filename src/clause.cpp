#include "clause.hpp"
#include "parser.hpp"

/******************************************************************************
 *  clause
 *****************************************************************************/
Clause::Clause(int _nvar, int _nltr)
{
	nltr = _nltr;
	nvar = _nvar;
}

/******************************************************************************
 *  bi_clause
 *****************************************************************************/

tuple<Integer, Bit> BIClause::find_target_literal(Integer target, Integer base) const{

    Integer count = base;
    Integer res(12, 0, PUBLIC);
    Bit s(0, PUBLIC);
    for (int j = 0; j < nvar; j++){
        Integer increment(16, 0, PUBLIC);
        increment.bits[0] = pos_vars[j] | neg_vars[j];
        count = count + increment;
        Bit istarget = count.equal(target) & (pos_vars[j] | neg_vars[j]) ;
        res = res.select(istarget, Integer(12, j, PUBLIC));
        s = (s & !istarget) | (pos_vars[j] & istarget);
    }

    return make_tuple(res, s);
}

void BIClause::set_literal(int index, bool is_pos, Bit real)
{
	if (is_pos) pos_vars[index] = real;
	else neg_vars[index] = real;
};

BIClause::BIClause(int _nvar) : Clause(_nvar, -1) // should never use nltr
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
	//literals = new Bit[2];
	for (int i = 0; i < nvar; i++)
	{
		pos_vars[i] = Bit(0, PUBLIC);
		neg_vars[i] = Bit(0, PUBLIC);
	}
}

BIClause::BIClause(int _nvar, string text) : Clause(_nvar, -1) // should never use nltr
{
	vector<int> vars = Parser::parse_literals(text);
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
	for (int i = 0; i < nvar; i++)
	{
		bool has_pos = find(vars.begin(), vars.end(), i) != vars.end();
		bool has_neg = find(vars.begin(), vars.end(), -i) != vars.end();
		neg_vars[i] = Bit(has_neg, PUBLIC);
		pos_vars[i] = Bit(has_pos, PUBLIC);
	}
}

unique_ptr<Clause> BIClause::default_value() const
{
	// bi_clause* res = new bi_clause(nvar);
	return make_unique<BIClause>(nvar);
}

void BIClause::set(vector<int> plist, vector<int> nlist, int Party)
{
	for (int i = 0; i < nlist.size(); i++)
	{
		int index = nlist[i];
		neg_vars[index] = Bit(1, Party);
	}

	for (int i = 0; i < plist.size(); i++)
	{
		int index = plist[i];
		pos_vars[index] = Bit(1, Party);
	}
}

Bit BIClause::contain(int index, bool is_pos) const
{
	return is_pos ? pos_vars[index] : neg_vars[index];
}

Bit BIClause::contain(const Literal &ell) const
{
	//  bi_literal ell = dynamic_cast<bi_literal*>(_ell)
	Bit b0 = Bit(0, PUBLIC);
	Bit b1 = Bit(0, PUBLIC);
	for (int i = 0; i < nvar; i++)
	{
		b0 = b0 | (neg_vars[i] & ell.isIndex(i, 0));
		b1 = b1 | (pos_vars[i] & ell.isIndex(i, 1));
	}
	return b0 | b1;
};

void BIClause::remove(const Literal &ell)
{
	//bi_literal ell = dynamic_cast<bi_literal*>(_ell)
	for (int i = 0; i < nvar; i++)
	{
		neg_vars[i] = neg_vars[i] & (neg_vars[i] ^ ell.isIndex(i, 0));
		pos_vars[i] = pos_vars[i] & (pos_vars[i] ^ ell.isIndex(i, 1));
	}
};

void BIClause::remove_model(const Model &model)
{
	for (int i = 0; i < nvar; i++)
	{
		neg_vars[i] = neg_vars[i] & (neg_vars[i] ^ model.hasIndex(i, 0));
		pos_vars[i] = pos_vars[i] & (pos_vars[i] ^ model.hasIndex(i, 1));
	}
};

Bit BIClause::contain_model(const Model &model) const
{
	Bit b0 = Bit(0, PUBLIC);
	Bit b1 = Bit(0, PUBLIC);
	for (int i = 0; i < nvar; i++)
	{
		b0 = b0 | (neg_vars[i] & model.hasIndex(i, 0));
		b1 = b1 | (pos_vars[i] & model.hasIndex(i, 1));
	}
	return b0 | b1;
}

Bit BIClause::isUnit()
{
	Bit a(false, PUBLIC);
	Bit b(false, PUBLIC);

	//cout << "steps";
	for (int j = 0; j < nvar; ++j)
	{
		Bit exist = neg_vars[j] | pos_vars[j];
		b = (exist & a) | b;
		a = exist | a;
		//printf("%d<%d %d> ", j, a.reveal<bool>(), b.reveal<bool>());
	}
	//cout << endl;
	//out << "!!!\n";
	//printf("a=%d b=%d unit=%d\n", a.reveal<bool>(), b.reveal<bool>(), unit.reveal<bool>());
	return (!b) & a;
}

unique_ptr<Literal> BIClause::get_unit_literal() const
{
	return make_unique<BILiteral>(pos_vars, neg_vars, nvar);
}

unique_ptr<Clause> BIClause::select(Bit use_rhs, unique_ptr<Clause> const &rhs) const
{
	unique_ptr<BIClause> res = copy_impl();
	for (int j = 0; j < nvar; j++)
	{
		// cout << "j=" << j << endl;
		Bit b1 = (contain(j, 1) & !use_rhs) | (rhs->contain(j, 1) & use_rhs);
		Bit b0 = (contain(j, 0) & !use_rhs) | (rhs->contain(j, 0) & use_rhs);
		res->set_literal(j, 0, b0);
		res->set_literal(j, 1, b1);
	}

	return res;
}

void BIClause::print(bool test) const
{
	if (not test)
		return;

	for (int i = 0; i < nvar; i++)
	{
		if (neg_vars[i].reveal<bool>())
		{
			cout << -i << " ";
		}
		if (pos_vars[i].reveal<bool>())
		{
			cout << i << " ";
		}
	}
	cout << endl;
	// cout << endl;
};

string BIClause::toString() const
{
	string res = "";
	bool is_first = true;
	for (int i = 0; i < nvar; i++)
	{
		if (neg_vars[i].reveal<bool>())
		{
			res += (is_first ? "" : " ") + string("-") + to_string(i);
			is_first = false;
		}
		if (pos_vars[i].reveal<bool>())
		{
			res += (is_first ? "" : " ") + to_string(i);
			is_first = false;
		}
	}
	return "(" + res + ")";
}

unique_ptr<BIClause> BIClause::copy_impl() const
{
	unique_ptr<BIClause> res = make_unique<BIClause>(nvar);

	for (int i = 0; i < nvar; i++)
	{
		res->neg_vars[i] = neg_vars[i];
		res->pos_vars[i] = pos_vars[i];
	}
	return res;
}

unique_ptr<Clause> BIClause::copy() const
{
	return copy_impl();
}

BIClause::~BIClause()
{
	delete[] neg_vars;
	delete[] pos_vars;
};

/******************************************************************************
 *  bbclause
 *****************************************************************************/

BBClause::BBClause(int _nvar, int _nliteral, int party) : BIClause(_nvar)
{
	nliteral = Integer(5, _nliteral, party);
}

BBClause::BBClause(int _nvar, Integer _nliteral, int party) : BIClause(_nvar)
{
	nliteral = _nliteral;
}

// bbclause(int _nliteral, const bi_clause& ) : bi_clause(_nvar){
// 	nliteral =  Integer(32, _nliteral, party);
// }

void BBClause::remove(const Literal &ell)
{
	Bit b = contain(ell);
	BIClause::remove(ell);
	Integer decrement(5, 0, PUBLIC);
	decrement.bits[0] = b;
	nliteral = nliteral - decrement;
}

void BBClause::set(vector<int> Pindex, vector<int> Nindex, int Party)
{
	BIClause::set(Pindex, Nindex, Party);
	nliteral = Integer(5, Pindex.size() + Nindex.size(), Party);
}

Bit BBClause::isUnit()
{
	return (nliteral.equal(Integer(5, 1, PUBLIC)));
}

unique_ptr<Clause> BBClause::copy() const
{
	unique_ptr<BBClause> res = make_unique<BBClause>(nvar, nliteral, PUBLIC);
	for (int i = 0; i < nltr; i++)
	{
		res->neg_vars[i] = neg_vars[i];
		res->pos_vars[i] = pos_vars[i];
	}
	// unique_ptr<bbclause> res = bi_clause::copy();
	// res -> nliteral =  nliteral;
	return res;
}

unique_ptr<Clause> BBClause::select(Bit b, unique_ptr<Clause> const &rhs) const
{
	throw "TODO";
}

void BBClause::print(bool test)
{
	if (!test)
		return;
	BIClause::print(test);
	cout << nliteral.reveal<int>() << endl;
}
