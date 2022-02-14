#include "emp-sh2pc/emp-sh2pc.h"
using namespace emp;
using namespace std;
#include <iostream>
#include <fstream>
#include <vector>
#include <memory> // unique_ptr
#include "utils.hpp"
//#include "obstack.hpp"
#include "literal.hpp"
#include "formula.hpp"
#include "parser.hpp"


// virtual unique_ptr<literal> operator&(const literal& rhs) const {
// 	auto res = rhs.copy();
// 	for(int i = 0; i < nvar; ++i){
// 		res->set_index(i, 1, res->isIndex(i, 1) & isIndex(i, 1));
// 		res->set_index(i, 0, res->isIndex(i, 0) & isIndex(i, 0));
// 	}
// 	return res;
// };
//virtual literal* mux(Bit b, literal* ell1, literal* ell2) const = 0;
//virtual literal operator^(const literal &ref) = 0;

Formula::Formula(vector<unique_ptr<Clause>> const &_cls, bool create_default)
{
	//nvar = _nvar;

	// cout << _cls.size() << endl;
	// cout <<_cls.size() << endl;
	for (auto &cl : _cls)
	{
		//cl -> print(true);
		if (create_default)
			cls.push_back(cl->default_value());
		else
			cls.push_back(cl->copy());
	}

	active = new Bit[cls.size()];
	//unit = new Bit[cls.size()];
	//cls = new clause[cls.size()];
	for (int i = 0; i < cls.size(); i++)
	{
		active[i] = Bit(1, PUBLIC);
		//	unit[i] = Bit(0, PUBLIC);
		//cls[i] = _cls[i];
	}
}

Formula::Formula(int nvar, string text)
{
	vector<string> raw_cls = Parser::parse_clauses(text);
	active = new Bit[raw_cls.size()];
	int i = 0;
	for (auto raw_cl : raw_cls) {
		active[i] = Bit(1, PUBLIC);
		cls.push_back(make_unique<BIClause>(nvar, raw_cl));
		i++;
	}
}

unique_ptr<Formula> Formula::default_value() const
{
	return make_unique<Formula>(cls, true);
}

unique_ptr<Formula> Formula::select(Bit use_rhs, unique_ptr<Formula> const &rhs) const
{
	unique_ptr<Formula> res = copy();
	for (int i = 0; i < cls.size(); i++)
	{
		res->cls[i] = cls[i]->select(use_rhs, rhs->cls[i]);
		res->active[i] = (res->active[i] & !use_rhs) | rhs->active[i] & use_rhs;
	}
	return res;
}

Integer Formula::num_of_alive_variables(int nvar) const
{
	Integer c(12, 0, PUBLIC);
	for (int i = 0; i < nvar; i++)
	{
		Bit alive(0, PUBLIC);
		for (int j = 0; j < cls.size(); j++)
		{
			alive = alive | ((cls[j]->contain(i, true) | cls[j]->contain(i, false)) & active[j]);
		}
		c = c + Integer(12, 0, PUBLIC).select(alive, Integer(12, 1, PUBLIC));
	}

	return c;
}

Integer Formula::get_random_alive_variable(int nvar, Integer random) const
{
	Integer c(12, 0, PUBLIC); // counter which increases after encountering each alive variable.
	Integer index(12, 0, PUBLIC); // stores the return value
	for (int i = 0; i < nvar; i++)
	{
		Bit alive(0, PUBLIC);
		for (int j = 0; j < cls.size(); j++)
		{
			alive = alive | ((cls[j]->contain(i, true) | cls[j]->contain(i, false)) & active[j]);
		}
		c = c + Integer(12, 0, PUBLIC).select(alive, Integer(12, 1, PUBLIC));
		index = index.select(c.equal(random + Integer(12, 1, PUBLIC)) & alive, Integer(12, i, PUBLIC));
	}

	return index;
	// Integer count = alive_literal(nvar);
	// Integer mux = findbound(count);
}

int Formula::get_ncls() const
{
	return cls.size();
}

void Formula::resolve_l(const Literal &ell)
{
	auto neg_ell = ell.flip();
	for (int i = 0; i < cls.size(); i++)
	{
		//cout << "before resolve\n";
		//cls[i] -> print(true);

		Bit b = cls[i]->contain(ell);
		cls[i]->remove(*neg_ell);
		active[i] = !b & active[i];

		//cls[i] -> print(true);
		//	cout << active[i].reveal<bool>() << endl;

		//cout << "end resolve\n";
	}
}

void Formula::simplify(const Model &model)
{
	auto neg_model = model.flip();
	for (int i = 0; i < cls.size(); i++)
	{
		cls[i]->remove_model(*neg_model);
		Bit b = cls[i]->contain_model(model);
		active[i] = !b & active[i];
	}
}

Bit Formula::empty() const
{
	Bit b(0, PUBLIC);
	// cout << "active[] = ";
	for (int i = 0; i < cls.size(); i++)
	{
		b = b | active[i];
		// cout << active[i].reveal<bool>() << " ";
	}
	// cout << endl;
	return !b;
};

Bit Formula::conflict(const Literal &ell) const
{
	Bit b(0, PUBLIC);
	auto neg_ell = ell.flip();
	for (int i = 0; i < cls.size(); i++)
		b = b | (cls[i]->contain(*neg_ell) & cls[i]->isUnit());
	return b;
};

void Formula::print(bool test) const
{
	if (!test)
		return;
	//cout << "print" << endl;
	for (int i = 0; i < cls.size(); i++)
	{
		cout << "print " << i << " clasue\n";
		cout << "active:" << active[i].reveal<bool>() << endl;
		cls[i]->print(test);
	}
}

string Formula::toString() const {
	string res = "";
	for (int i = 0; i < cls.size(); i++)
	{
		if (active[i].reveal<bool>()) {
			res += cls[i]->toString();
		}
	}
	return res;
}

// formula copy() {
// 	formula res(cls.size(), cls);
// 	for (int i = 0; i < cls.size(); i++) res.active[i] = active[i];
// 	return res;
// }

unique_ptr<Formula> Formula::copy() const
{
	//vector<clause*> v;
	unique_ptr<Formula> res = make_unique<Formula>(cls);
	for (int i = 0; i < cls.size(); i++)
		res->active[i] = active[i];
	return res;
}

void Formula::operator=(const Formula &f)
{
}

Formula::~Formula()
{

	// printf("delete active %p\n", active);
	delete[] active;
	// printf("after delete active\n");
	// for (clause* cl : cls) {
	// 	// printf("delete clause %p\n", cl);
	// 	delete cl;
	// }
};

tuple<Integer, Bit> Formula::get_target_literal(Integer target) const{
    Integer base(16, 0,PUBLIC);
    Integer res(12, 0,PUBLIC);
    Bit s(0, PUBLIC);

    for (int i =0; i < cls.size(); i++){
        auto tmp =  cls[i] -> find_target_literal(target, base);
        res = res + std::get<0>(tmp);
        s = s | std::get<1>(tmp);
        base = base  + count_alive_literal(*cls[i]);
    }

    return make_tuple(res, s);
}
