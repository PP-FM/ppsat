//
// Created by Ning Luo on 5/18/21.
//

#include <math.h>
#include "formula.hpp"
#include <memory>
#include <chrono>
#include <exception>
#include <stdlib.h>
#include <ctime>
#include "clause.hpp"
#include "literal.hpp"
#include "model.hpp"
#include "utils.hpp"
#include "solver.hpp"
using namespace std;
using namespace emp;



int main(int argc, char** argv) {

    try {

        int port, party;
        //cout<<"finish" << endl;

        parse_party_and_port(argv, &party, &port);
        NetIO *io = new NetIO(party == ALICE ? nullptr : "127.0.0.1", port);
        setup_semi_honest(io, party);

        int number_of_steps = atoi(argv[3]);
        int nvar = atoi(argv[4])+1;
        auto phi_a =  make_unique<Formula>(nvar, argv[5], ALICE);
        auto phi_b =  make_unique<Formula>(nvar, argv[6], BOB);
        auto phi = phi_a -> conjunction(phi_b);
        cout << "input formula: \n";
         phi->print(true);
        Solver solver(nvar, phi);
        auto model = solver.solve(number_of_steps, false);
        cout << "model\n"; 
        cout << model->toString() << endl;
        delete io;
    }

    catch (char const *msg) {
        cout << "Main catch msg: " << msg << endl;
    }
    catch (const exception &e) {
        cout << "Main cat exception: " << e.what() << endl;
    }


}

