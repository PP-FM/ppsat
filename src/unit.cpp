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

    srand(2);


    try {

        int port, party;
        //cout<<"finish" << endl;

        parse_party_and_port(argv, &party, &port);
        NetIO *io = new NetIO(party == ALICE ? nullptr : "127.0.0.1", port);

        setup_semi_honest(io, party);

        int nvar = 4;
        auto phi = make_unique<Formula>(nvar, "(1 2 3)(-1)(-2 3)");
        phi->print(true);
        Solver solver(nvar, phi);
        Bit has_unit = solver.UnitSearch();
        cout << "has unit: " <<  has_unit.reveal(PUBLIC) << endl;

        delete io;

    }

    catch (char const *msg) {
        cout << "Main catch msg: " << msg << endl;
    }
    catch (const exception &e) {
        cout << "Main cat exception: " << e.what() << endl;
    }


}

