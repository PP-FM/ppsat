#include "gtest/gtest.h"

#include "formula.hpp"
#include <vector>
#include <memory>


TEST(FORMULA, toString)
{
    int nvar = 4;
    vector<unique_ptr<Clause>> cls;
    cls.push_back(make_unique<BIClause>(nvar, "1 2 3"));
    cls.push_back(make_unique<BIClause>(nvar, "-1"));
    cls.push_back(make_unique<BIClause>(nvar, "-2 3"));
    auto f = make_unique<Formula>(cls);
    EXPECT_EQ(f->toString(), "(1 2 3)(-1)(-2 3)");
}

TEST(FORMULA, constructors)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 2 3)(-1) (-2 3)");
    EXPECT_EQ(f->toString(), "(1 2 3)(-1)(-2 3)");
}

TEST(FORMULA, default_value)
{
    int nvar = 4;
    auto f1 = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
    auto f2 = f1->default_value();
    EXPECT_EQ(f2->toString(), "()()()");
}

TEST(FORMULA, copy)
{
    int nvar = 4;
    auto f1 = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
    auto f2 = f1->copy();
    EXPECT_EQ(f2->toString(), "(1 2 3)(-1)(-2 3)");
}

TEST(FORMULA, select)
{
    int nvar = 4;
    auto f1 = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
    auto f2 = make_unique<Formula>(nvar, "(1)(-1 3)(2)");
    auto res1 = f1->select(Bit(false, PUBLIC), f2);
    auto res2 = f1->select(Bit(true, PUBLIC), f2);
    EXPECT_EQ(res1->toString(), f1->toString());
    EXPECT_EQ(res2->toString(), f2->toString());
}

TEST(FORMULA, num_of_alive_variables)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 2 3)(-1)(1 3)");
    EXPECT_EQ(f->num_of_alive_variables(nvar).reveal<int>(), 3);
    f->active[0] = Bit(false, PUBLIC);
    EXPECT_EQ(f->num_of_alive_variables(nvar).reveal<int>(), 2);
}

TEST(FORMULA, get_random_alive_variable)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 -2 3)(-1)(1 -3)");
    Integer i = f->get_random_alive_variable(nvar, Integer(12, 1, PUBLIC));
    EXPECT_EQ(i.reveal<int>(), 2);
}

TEST(FORMULA, get_ncls)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 -2 3)(-1)(1 -3)");
    EXPECT_EQ(f->get_ncls(), 3);
}

TEST(FORMULA, resolve)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 -2 3)(-1)(1 -2 -3)");
    auto ell = make_unique<BILiteral>(nvar, "3");
    f->resolve_l(*ell);
    EXPECT_EQ(f->toString(), "(-1)(1 -2)");
}

TEST(FORMULA, simplify)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 -2 3)(-1 2)(-1 -3)");
    auto model = make_unique<Model>(nvar, "3 -2");
    f->simplify(*model);
    EXPECT_EQ(f->toString(), "(-1)(-1)");
}

TEST(FORMULA, empty)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 -2 3)");
    EXPECT_FALSE(f->empty().reveal<bool>());
    f->active[0] = Bit(0, PUBLIC);
    EXPECT_TRUE(f->empty().reveal<bool>());
}

TEST(FORMULA, conflict)
{
    int nvar = 4;
    auto f = make_unique<Formula>(nvar, "(1 2 -3)(-2)(1)");
    auto ell1 = make_unique<BILiteral>(nvar, "1");
    auto ell2 = make_unique<BILiteral>(nvar, "2");
    EXPECT_FALSE(f->conflict(*ell1).reveal<bool>());
    EXPECT_TRUE(f->conflict(*ell2).reveal<bool>());
}