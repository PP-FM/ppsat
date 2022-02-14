#include "gtest/gtest.h"
#include "literal.hpp"
#include "parser.hpp"
#include <vector>
#include <memory>


TEST(BI_LITERAL, toString)
{
    int nvar = 4;
    auto l = make_unique<BILiteral>(nvar); 
    l->set_index_p(2, false);
    EXPECT_EQ(l->toString(), "-2");
}

TEST(BI_LITERAL, bit_map_constuctors)
{
    int nvar = 4;

    Bit pos_vars[] = {Bit(0, PUBLIC), Bit(0, PUBLIC), Bit(0, PUBLIC), Bit(0, PUBLIC)};
    Bit neg_vars[] = {Bit(0, PUBLIC), Bit(1, PUBLIC), Bit(0, PUBLIC), Bit(0, PUBLIC)};
    auto l1 = make_unique<BILiteral>(pos_vars, neg_vars, 4);
    EXPECT_EQ(l1->toString(), "-1");

    Bit **ind = new Bit*[2];
    ind[0] = neg_vars;
    ind[1] = pos_vars;
    auto l2 = make_unique<BILiteral>(ind, nvar);
    EXPECT_EQ(l2->toString(), "-1");

    auto l3 = make_unique<BILiteral>(nvar, "2");
    EXPECT_EQ(l3->toString(), "2");
}

TEST(BI_LITERAL, simple_constuctors)
{
    int nvar = 4;

    auto l1 = make_unique<BILiteral>(nvar, 2, false);
    EXPECT_EQ(l1->toString(), "-2");

    auto l2 = make_unique<BILiteral>(nvar, Integer(12, 2, PUBLIC), true);
    EXPECT_EQ(l2->toString(), "2");
}

TEST(BI_LITERAL, default_value)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar);
    auto l2 = l1->default_value();
    EXPECT_EQ(l2->toString(), "_");
}

TEST(BI_LITERAL, select)
{
    int nvar = 4;
    unique_ptr<Literal> l1 = make_unique<BILiteral>(nvar, "-1");
    unique_ptr<Literal> l2 = make_unique<BILiteral>(nvar, "2");
    auto res1 = l1->select(Bit(false, PUBLIC), l2);
    auto res2 = l1->select(Bit(true, PUBLIC), l2);
    EXPECT_EQ(res1->toString(), l1->toString());
    EXPECT_EQ(res2->toString(), l2->toString());
}

TEST(BI_LITERAL, copy)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar, "1");
    auto l2 = l1->copy();
    EXPECT_EQ(l2->toString(), "1");
}

TEST(BI_LITERAL, set_index)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar, "2");

    l1->set_index(1, true, Bit(true, PUBLIC));
    EXPECT_EQ(l1->toString(), "1");
    l1->set_index_s(Integer(12, 3, PUBLIC), Bit(false, PUBLIC), Bit(true, PUBLIC));
    EXPECT_EQ(l1->toString(), "-3");
    l1->set_index_p(2, true);
    EXPECT_EQ(l1->toString(), "2");
}

TEST(BI_LITERAL, isIndex)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar, "2");

    Bit b1 = l1->isIndex(1, true);
    Bit b2 = l1->isIndex(2, true);
    Bit b2_neg = l1->isIndex(2, false);
    Bit b3 = l1->isIndex(3, true);

    EXPECT_EQ(b1.reveal<bool>(), false);
    EXPECT_EQ(b2.reveal<bool>(), true);
    EXPECT_EQ(b2_neg.reveal<bool>(), false);
    EXPECT_EQ(b3.reveal<bool>(), false);
}

TEST(BI_LITERAL, get_literal)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar, "1");
    auto res1 = l1->get_index();
    Integer var1 = get<0>(res1);
    Bit is_pos1 = get<1>(res1);
    EXPECT_EQ(var1.reveal<int>(), 1);
    EXPECT_EQ(is_pos1.reveal<bool>(), true);

    auto l2 = make_unique<BILiteral>(nvar, "-2");
    auto res2 = l2->get_index();
    Integer var2 = get<0>(res2);
    Bit is_pos2 = get<1>(res2);
    EXPECT_EQ(var2.reveal<int>(), 2);
    EXPECT_EQ(is_pos2.reveal<bool>(), false);
}

TEST(BI_LITERAL, flip)
{
    int nvar = 4;
    auto l1 = make_unique<BILiteral>(nvar, "1");
    auto l2 = l1->flip();
    EXPECT_EQ(l2->toString(), "-1");
}