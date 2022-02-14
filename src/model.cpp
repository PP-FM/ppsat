#include "model.hpp"
#include "parser.hpp"

Model::Model(int _nvar) : nvar(_nvar)
{
    pos_vars = new Bit[nvar];
    neg_vars = new Bit[nvar];
}

Model::Model(Bit *_pos_var, Bit *_neg_var, int _nvar) : nvar(_nvar)
{
    pos_vars = new Bit[nvar];
    neg_vars = new Bit[nvar];
    for (int j = 0; j < _nvar; j++)
    {
        pos_vars[j] = _pos_var[j];
        neg_vars[j] = _neg_var[j];
    }
}

Model::Model(int nvar, string text) : nvar(nvar)
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

void Model::update_index(int index, bool is_pos, Bit real)
{
    if (is_pos) pos_vars[index] = real;
    else neg_vars[index] = real;
}

unique_ptr<Model> Model::default_value() const
{
    return make_unique<Model>(nvar);
}

// void Model::set_index(int index, bool is_pos, Bit real)
// {
// 	for (int i = 0; i < nvar; i++)
// 	{
// 		Bit is_vari = index == i;
// 		neg_vars[i] = (is_vari & !is_pos) & real;
// 		pos_vars[i] = (is_vari & is_pos) & real;
// 	}
// }

unique_ptr<Model> Model::copy() const
{

    return make_unique<Model>(pos_vars, neg_vars, nvar);
}

string Model::toString() const
{
    string res = "{";
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
    res += "}";
    return res;
}

void Model::print(bool test) const
{
    if (test) {
        cout << toString() << endl;
    }
}

Bit Model::hasIndex(int index, bool is_pos) const
{
    if (is_pos) return pos_vars[index];
    else return neg_vars[index];
}

unique_ptr<Model> Model::select(Bit use_rhs, unique_ptr<Model> const &rhs) const
{
    unique_ptr<Model> res = make_unique<Model>(pos_vars, neg_vars, nvar);
    for (int j = 0; j < nvar; j++)
    {
        Bit b_neg = (hasIndex(j, 0) & !use_rhs) | (rhs->hasIndex(j, 0) & use_rhs);
        Bit b_pos = (hasIndex(j, 1) & !use_rhs) | (rhs->hasIndex(j, 1) & use_rhs);
        res->update_index(j, 0, b_neg);
        res->update_index(j, 1, b_pos);
    }

    return res;
}

unique_ptr<Model> Model::operator|(const Literal &rhs) const
{
    auto res = copy();
    for (int i = 0; i < nvar; ++i)
    {
        //cout <<"------enter loop-----"<<endl;

        res->update_index(i, 1, res->hasIndex(i, 1) | rhs.isIndex(i, 1));
        res->update_index(i, 0, res->hasIndex(i, 0) | rhs.isIndex(i, 0));
    }
    return res;
}

unique_ptr<Model> Model::flip() const
{
	auto res = make_unique<Model>(nvar);
	for (int i = 0; i < nvar; i++)
	{
		res->neg_vars[i] = pos_vars[i];
		res->pos_vars[i] = neg_vars[i];
	}

	return res;
}

Model::~Model()
{
    delete[] pos_vars;
    delete[] neg_vars;
}
