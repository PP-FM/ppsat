#include "gtest/gtest.h"
#include "model.hpp"
#include "parser.hpp"
#include <vector>
#include <memory>

TEST(MODEL, toString)
{
    int nvar = 4;
    auto m = make_unique<Model>(nvar, "{-2 3}");
    EXPECT_EQ(m->toString(), "{-2 3}");
}

TEST(MODEL, bit_map_constuctors)
{
    int nvar = 4;

    Bit pos_vars[] = {Bit(0, PUBLIC), Bit(0, PUBLIC), Bit(1, PUBLIC), Bit(1, PUBLIC)};
    Bit neg_vars[] = {Bit(0, PUBLIC), Bit(1, PUBLIC), Bit(0, PUBLIC), Bit(0, PUBLIC)};
    auto m = make_unique<Model>(pos_vars, neg_vars, 4);
    EXPECT_EQ(m->toString(), "{-1 2 3}");
}

TEST(MODEL, default_value)
{
    int nvar = 4;
    auto m = make_unique<Model>(4, "{-1 2 3}");
    auto m0 = m->default_value();
    EXPECT_EQ(m0->toString(), "{}");
}

TEST(MODEL, update_index)
{
    int nvar = 4;
    auto m = make_unique<Model>(4, "{-1 2}");
    m->update_index(3, true, Bit(true, PUBLIC));
    EXPECT_EQ(m->toString(), "{-1 2 3}");
    m->update_index(1, true, Bit(false, PUBLIC));
    EXPECT_EQ(m->toString(), "{-1 2 3}");
    m->update_index(2, false, Bit(true, PUBLIC));
    EXPECT_EQ(m->toString(), "{-1 -2 2 3}");
}

TEST(MODEL, copy)
{
    int nvar = 4;
    auto m1 = make_unique<Model>(nvar, "{1 2}");
    auto m2 = m1->copy();
    EXPECT_EQ(m2->toString(), "{1 2}");
}

TEST(MODEL, hasIndex)
{
    int nvar = 4;
    auto m = make_unique<Model>(nvar, "{1 2 -3}");

    Bit b1 = m->hasIndex(1, true);
    Bit b2 = m->hasIndex(2, true);
    Bit b2_neg = m->hasIndex(2, false);
    Bit b3 = m->hasIndex(3, true);

    EXPECT_EQ(b1.reveal<bool>(), true);
    EXPECT_EQ(b2.reveal<bool>(), true);
    EXPECT_EQ(b2_neg.reveal<bool>(), false);
    EXPECT_EQ(b3.reveal<bool>(), false);
}

TEST(MODEL, select)
{
    int nvar = 4;
    auto m1 = make_unique<Model>(nvar, "{-1 2}");
    auto m2 = make_unique<Model>(nvar, "{1 3}");
    auto res1 = m1->select(Bit(false, PUBLIC), m2);
    auto res2 = m1->select(Bit(true, PUBLIC), m2);
    EXPECT_EQ(res1->toString(), m1->toString());
    EXPECT_EQ(res2->toString(), m2->toString());
}

TEST(MODEL, operator_or)
{
    int nvar = 4;
    auto m1 = make_unique<Model>(nvar, "{-1 2 3}");
    auto m2 = make_unique<BILiteral>(nvar, "1");
    auto m3 = *m1 | *m2;
    EXPECT_EQ(m3->toString(), "{-1 1 2 3}");
}

TEST(MODEL, flip)
{
    int nvar = 4;
    auto m1 = make_unique<Model>(nvar, "{1 -2}");
    auto m2 = m1->flip();
    EXPECT_EQ(m2->toString(), "{-1 2}");
}