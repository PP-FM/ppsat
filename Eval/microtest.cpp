//
// Created by Ning Luo on 5/17/21.
//

#include <math.h>
#include <chrono>
#include <exception>
#include <stdlib.h>
#include <ctime>
#include "solver.hpp"
#include "utils.hpp"
using namespace std;
using namespace emp;

// this microtest will print the time for each step and its components.

int main(int argc, char** argv) {

    srand(2);
    try {
        int port, party;
        party = atoi(argv[1]);
        port = atoi(argv[2]);
        int nvar = atoi(argv[3]);
        int ncls = atoi(argv[4]);
        int nltr = atoi(argv[5]);
        bool single_step_test = true;
        int number_of_steps = atoi(argv[6]);
        /*
         * On purpose of microtest, argv[6] should be set to be 1.
         */
        single_step_test = number_of_steps== 1;

        cout<<"finish set up" << endl;
        NetIO *io = new NetIO(party == ALICE ? nullptr : "127.0.0.1", port);
        setup_semi_honest(io, party);

        /*
         * generate will return a pointer to a formula of expected size.
         * ncls -- number of clauses
         * nvar -- number of variables in the formulae
         * nltr -- number of literals in one clauses  (this parameter will not affect the performance anyway for now. We leave it here on purpose of future work.)
         */
        auto phi = generate(ncls, nvar, nltr, BICLAUSE, BILITERAL);
        cout << "finish generate\n";
        /*
         * Notice generate function will give a random formula.
         * for solving the formulae of your own, you can input replace phi  with your input of type unique_ptr<Forluma>
         * for inputing your own formulae, you could use constructor of formula that takes string as input:
         * i.e  auto phi = make_unique<Formula>(nvar, "(1 2 3)(-1) (-2 3)");
         * the syntax of input string is the (\(-?[0-9]+\))+
         */

        Solver solver(nvar, phi);
        /*
         * initiate your solver with your formulae and number of variables.
         *
         * */

        chrono::steady_clock sc;
        auto start = sc.now();
        auto model = solver.solve(number_of_steps + 1, single_step_test);
        auto end = sc.now();
        auto time_span = static_cast<chrono::duration<double>>(end - start);
        cout << "total time: " << time_span.count() << endl;
        cout << nvar << " variables, " << nltr << " literals, " << ncls << " clauses.\n";
        cout << CircuitExecution::circ_exec->num_and() << endl;
        delete io;
    }
    catch (char const *msg) {
            cout << "Main catch msg: " << msg << endl;
    }
    catch (const exception &e) {
            cout << "Main cat exception: " << e.what() << endl;
    }

}