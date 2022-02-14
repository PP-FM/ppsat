#include "literal.hpp"
#include "parser.hpp"

/******************************************************************************
 *  literal
 *****************************************************************************/

// TODO: delete me
unique_ptr<Literal> Literal::operator|(const Literal &rhs) const
{
	auto res = copy();
	for (int i = 0; i < nvar; ++i)
	{
		//cout <<"------enter loop-----"<<endl;

		res->set_index(i, 1, res->isIndex(i, 1) | rhs.isIndex(i, 1));
		res->set_index(i, 0, res->isIndex(i, 0) | rhs.isIndex(i, 0));
	}
	return res;
}

/******************************************************************************
 *  bi_literal
 *****************************************************************************/

BILiteral::BILiteral(int nvar) : Literal(nvar)
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
}

BILiteral::BILiteral(Bit *_pos_var, Bit *_neg_var, int _nvar) : Literal(_nvar)
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
	for (int j = 0; j < _nvar; j++)
	{
		pos_vars[j] = _pos_var[j];
		neg_vars[j] = _neg_var[j];
	}
}

BILiteral::BILiteral(Bit **_ind, int _nvar) : Literal(_nvar)
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
	for (int j = 0; j < _nvar; j++)
	{
		pos_vars[j] = _ind[1][j];
		neg_vars[j] = _ind[0][j];
	}
}

BILiteral::BILiteral(int nvar, int index, bool is_pos) : Literal(nvar)
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];

	for (int i = 0; i < nvar; i++)
	{
		bool b = (index == i);
		//  cout << (b and (not is_pos)) << endl;
		neg_vars[i] = Bit(b and (not is_pos), PUBLIC);
		pos_vars[i] = Bit(b and is_pos, PUBLIC);
		// cout << i << ":" << ind[1][i].reveal<bool>() <<endl;
	}
}

BILiteral::BILiteral(int nvar, Integer index, Bit is_pos) : Literal(nvar)
{
	pos_vars = new Bit[nvar];
	neg_vars = new Bit[nvar];
	for (int i = 0; i < nvar; i++)
	{
		// cout<<"test???"<< i << endl;
		Bit b = (index.equal(Integer(12, i, PUBLIC)));
		neg_vars[i] = b & !is_pos;
		pos_vars[i] = b & is_pos;
	}
}

BILiteral::BILiteral(int nvar, string text) : Literal(nvar)
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

unique_ptr<Literal> BILiteral::default_value() const
{
	return make_unique<BILiteral>(nvar);
}

unique_ptr<Literal> BILiteral::copy() const
{

	return make_unique<BILiteral>(pos_vars, neg_vars, nvar);
}

unique_ptr<Literal> BILiteral::select(Bit use_rhs, unique_ptr<Literal> const &rhs) const
{
	unique_ptr<BILiteral> res = make_unique<BILiteral>(pos_vars, neg_vars, nvar);
	for (int j = 0; j < nvar; j++)
	{
		Bit b_neg = (isIndex(j, 0) & !use_rhs) | (rhs->isIndex(j, 0) & use_rhs);
		Bit b_pos = (isIndex(j, 1) & !use_rhs) | (rhs->isIndex(j, 1) & use_rhs);
		res->update_index(j, 0, b_neg);
		res->update_index(j, 1, b_pos);
	}

	return res;
}

void BILiteral::update_index(int index, bool is_pos, Bit real)
{
	if (is_pos) pos_vars[index] = real;
	else neg_vars[index] = real;
}

void BILiteral::set_index(int index, bool is_pos, Bit real)
{
	for (int i = 0; i < nvar; i++)
	{
		Bit is_vari = index == i;
		neg_vars[i] = (is_vari & !is_pos) & real;
		pos_vars[i] = (is_vari & is_pos) & real;
	}
}

void BILiteral::set_index_s(Integer index, Bit is_pos, Bit real)
{
	for (int i = 0; i < nvar; i++)
	{
		// cout<<"test???"<< i << endl;
		Bit is_vari = (index.equal(Integer(12, i, PUBLIC)));
		neg_vars[i] = (is_vari & !is_pos) & real;
		pos_vars[i] = (is_vari & is_pos) & real;
	}
}

Bit BILiteral::isIndex(int index, bool is_pos) const
{
	if (is_pos) return pos_vars[index];
	else return neg_vars[index];
}

void BILiteral::set_index_p(int index, bool is_pos)
{
	for (int i = 0; i < nvar; i++)
	{
		bool b = (index == i);
		neg_vars[i] = Bit(b and not is_pos, PUBLIC);
		pos_vars[i] = Bit(b and is_pos, PUBLIC);
		// cout << i << ":" << ind[1][i].reveal<bool>() <<endl;
	}
}

unique_ptr<Literal> BILiteral::flip() const
{
	auto res = make_unique<BILiteral>(nvar);
	for (int i = 0; i < nvar; i++)
	{
		res->neg_vars[i] = pos_vars[i];
		res->pos_vars[i] = neg_vars[i];
	}

	return res;
}

void BILiteral::print(bool test) const
{

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
	//	cout <<  "-------\n";
	cout << endl;
	// cout <<  "---end----\n";
}

string BILiteral::toString() const
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
	if (is_first) res = "_";
	return res;
}

tuple<Integer, Bit> BILiteral::get_index() const
{
	Integer index(12, 0, PUBLIC);
	Bit is_pos(0, PUBLIC);

	for (int i = 0; i < nvar; i++)
	{
		index = index.select(pos_vars[i] | neg_vars[i], Integer(12, i, PUBLIC));
		// index = index.select(ind[1][i], Integer(12, i, PUBLIC));
		is_pos = pos_vars[i] | is_pos;
	}

	return make_tuple(index, is_pos);
}

BILiteral::~BILiteral()
{
	delete[] pos_vars;
	delete[] neg_vars;
}
