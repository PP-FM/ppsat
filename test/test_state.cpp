#include "gtest/gtest.h"
#include "state.hpp"
#include "parser.hpp"
#include <vector>
#include <memory>

TEST(STATE, toString)
{
    int nvar = 4;
    unique_ptr<Literal> ell = make_unique<BILiteral>(nvar, "1");
    auto model = make_unique<Model>(nvar, "{-1 2}");
    State s = State(ell, model);
    EXPECT_EQ(s.toString(), "[ell: 1, model: {-1 2}]");
}

TEST(STATE, copy)
{
    int nvar = 4;
    auto state1 = State(nvar, "1", "{-2 3}");
    auto state2 = state1.copy();
    EXPECT_EQ(state2.toString(), state1.toString());
}

// TODO: copy constructor and assignment

TEST(STATE, getter_setter)
{
    int nvar = 4;
    auto state = State(nvar, "1", "{-2 3}");
    unique_ptr<Literal> ell = make_unique<BILiteral>(nvar, "-1");
    auto model = make_unique<Model>(nvar, "{1 -3}");
    state.set_literal(ell);
    state.set_model(model);
    EXPECT_EQ(state.get_literal()->toString(), ell->toString());
    EXPECT_EQ(state.get_model()->toString(), model->toString());
}

TEST(STATE, select)
{
    int nvar = 4;
    auto state1 = State(nvar, "1", "{-2 3}");
    auto state2 = State(nvar, "-1", "{-3}");
    auto res1 = state1.select(Bit(false, PUBLIC), state2);
    auto res2 = state1.select(Bit(true, PUBLIC), state2);
    EXPECT_EQ(res1.toString(), state1.toString());
    EXPECT_EQ(res2.toString(), state2.toString());
}

TEST(STATE, default_value)
{
    int nvar = 4;
    auto state = State(nvar, "1", "{-2 3}");
    auto state0 = state.default_value();
    EXPECT_EQ(state0.toString(), "[ell: _, model: {}]");
}

TEST(STATE, flip)
{
    int nvar = 4;
    auto state1 = State(nvar, "1", "{-2 3}");
    auto state2 = state1.flip();
    EXPECT_EQ(state2.toString(), "[ell: -1, model: {-2 3}]");
}
