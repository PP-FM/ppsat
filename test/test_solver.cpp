#include "gtest/gtest.h"

#include "solver.hpp"
#include "utils.hpp"
#include <ctime>
#include <vector>
#include <memory>

TEST(SOLVER, UnitSearch)
{
    int nvar = 4;
    auto phi = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
    Solver solver(nvar, phi);
    Bit has_unit = solver.UnitSearch();
    EXPECT_TRUE(has_unit.reveal<bool>());
    EXPECT_EQ(solver.current.get_literal()->toString(), "-1");

}




TEST(SOLVER, Propagation)
{
    int nvar = 4;
    auto phi = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
    Solver solver(nvar, phi);
    Bit has_unit = solver.UnitSearch();
    solver.propagation();
    EXPECT_EQ(solver.current_phi->toString(), "(2 3)(-2 3)");
}




TEST(SOLVER, UnitSearch_Evaluation)
{
    int ncls = 10000;
    int nvar = 100;
    int nltr = 3;
    auto phi = generate(ncls, nvar, nltr, BICLAUSE, BILITERAL);
    Solver solver(nvar, phi);
    chrono::steady_clock sc;
    auto start = sc.now();
    Bit has_unit = solver.UnitSearch();
    auto end = sc.now();
    auto time_span = static_cast<chrono::duration<double>>(end - start);
    cout << "total time: " << time_span.count() << endl;
}

TEST(SOLVER, solve_sat)
{
    int nvar = 4;
    auto phi = make_unique<Formula>(nvar, "(1 2 3)(-1 2)(2 -3)");
    Solver solver(nvar, phi);
    auto model = solver.solve(100, false);
    cout << model->toString() << endl;
}

TEST(SOLVER, solve_unsat)
{
    int nvar = 4;
    auto phi = make_unique<Formula>(nvar, "(1 2)(-1 -2)(1 -2)(-1 2)");
    Solver solver(nvar, phi);
    auto model = solver.solve(100, false);
    cout << model->toString() << endl;
}


TEST(SOLVER, evaluation)
{
    int ncls = 10000;
    int nvar = 100;
    int nltr = 3;
    auto phi = generate(ncls, nvar, nltr, BICLAUSE, BILITERAL);
    // auto phi = generate(100,1000, 100, BICLAUSE, BILITERAL);
    cout << "finish generate\n";
    Solver solver(nvar, phi);
    chrono::steady_clock sc;
    auto start = sc.now();
    auto model = solver.solve(100, true);
    auto end = sc.now();
    auto time_span = static_cast<chrono::duration<double>>(end - start);
    cout << "total time: " << time_span.count() << endl;
  // cout << model->toString() << endl;
}

TEST(SOLVER, private_stack)
{
    int nvar = 100;
    PrivateStack<State> stack;
    unique_ptr<Literal> _ell = make_unique<BILiteral>(nvar);
	unique_ptr<Model> _model = make_unique<Model>(nvar);
	stack.init(nvar, State(_ell, _model, true));

    Bit bit0 = Bit(false, PUBLIC);
    Bit bit1 = Bit(true, PUBLIC);
    auto state1 = State(nvar, "4", "{-1 2 3}");
    auto state2 = State(nvar, "-4", "{1 2 3}");
    stack.push(state1, bit1);
    stack.pop(bit0);
}
