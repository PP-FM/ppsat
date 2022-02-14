#include "gtest/gtest.h"
#include "clause.hpp"
#include "parser.hpp"
#include <vector>
#include <memory>


TEST(BI_CLAUSE, toString)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar);
    vector<int> pos_vars{1,2};
    vector<int> neg_vars{3};
    c->set(pos_vars, neg_vars, PUBLIC);
    EXPECT_EQ(c->toString(), "(1 2 -3)");
}

TEST(BI_CLAUSE, constuctors)
{
    int nvar = 4;
    auto c1 = make_unique<BIClause>(nvar, "-1 2");
    EXPECT_EQ(c1->toString(), "(-1 2)");
}

TEST(BI_CLAUSE, default_value)
{
    int nvar = 4;
    auto c1 = make_unique<BIClause>(nvar, "-1 2");
    auto c2 = c1->default_value();
    EXPECT_EQ(c2->toString(), "()");
}

TEST(BI_CLAUSE, set)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar);
    vector<int> pos_vars{1,2};
    vector<int> neg_vars{3};
    c->set(pos_vars, neg_vars, PUBLIC);
    EXPECT_EQ(c->toString(), "(1 2 -3)");
}

TEST(BI_CLAUSE, contain)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar, "-1 2");
    auto l1 = make_unique<BILiteral>(nvar, "1");
    auto l2 = make_unique<BILiteral>(nvar, "2");
    auto l3 = make_unique<BILiteral>(nvar, "-3");
    EXPECT_FALSE(c->contain(1, true).reveal<bool>());
    EXPECT_FALSE(c->contain(*l1).reveal<bool>());
    EXPECT_TRUE(c->contain(2, true).reveal<bool>());
    EXPECT_TRUE(c->contain(*l2).reveal<bool>());
    EXPECT_FALSE(c->contain(*l3).reveal<bool>());
}

TEST(BI_CLAUSE, remove)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar, "-1 2");
    auto l1 = make_unique<BILiteral>(nvar, "1");
    auto l2 = make_unique<BILiteral>(nvar, "2");
    c->remove(*l1);
    EXPECT_EQ(c->toString(), "(-1 2)");
    c->remove(*l2);
    EXPECT_EQ(c->toString(), "(-1)");
}

TEST(BI_CLAUSE, remove_model)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar, "-1 2 3");
    auto m = make_unique<Model>(nvar, "1 2");
    c->remove_model(*m);
    EXPECT_EQ(c->toString(), "(-1 3)");
}

TEST(BI_CLAUSE, contain_model)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar, "-1 2 3");
    auto m = make_unique<Model>(nvar, "1 2");
    Bit res = c->contain_model(*m);
    EXPECT_TRUE(res.reveal<bool>());
}

TEST(BI_CLAUSE, select)
{
    int nvar = 4;
    unique_ptr<Clause> c1 = make_unique<BIClause>(nvar, "-1 2 3");
    unique_ptr<Clause> c2 = make_unique<BIClause>(nvar, "1 2");
    auto res1 = c1->select(Bit(false, PUBLIC), c2);
    auto res2 = c1->select(Bit(true, PUBLIC), c2);
    EXPECT_EQ(res1->toString(), c1->toString());
    EXPECT_EQ(res2->toString(), c2->toString());
}

TEST(BI_CLAUSE, copy)
{
    int nvar = 4;
    auto c1 = make_unique<BIClause>(nvar, "-1 2 3");
    auto c2 = c1->copy();
    EXPECT_EQ(c2->toString(), "(-1 2 3)");
}

TEST(BI_CLAUSE, isUnit)
{
    int nvar = 4;
    auto c1 = make_unique<BIClause>(nvar, "-1 2 3");
    EXPECT_FALSE(c1->isUnit().reveal<bool>());
    auto c2 = make_unique<BIClause>(nvar, "2");
    EXPECT_TRUE(c2->isUnit().reveal<bool>());
}

TEST(BI_CLAUSE, get_unit_literal)
{
    int nvar = 4;
    auto c = make_unique<BIClause>(nvar, "2");
    auto l = c->get_unit_literal();
    EXPECT_EQ(l->toString(), "2");
}
