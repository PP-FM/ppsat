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


        // for (int i = 5; i < 15; i++){
        //int i = 10;
        int nvar = 4;
        int ncls = 20;
        int nltr = 3;
        CLAUSE ct = BICLAUSE;
        LITERAL lt = BILITERAL;


        unique_ptr<Formula> phi = generate(ncls, nvar, nltr, ct, lt);

        //phi -> print(true);

        chrono::steady_clock sc;


        int raw_plist[] = {1, 2};
        int raw_nlist[] = {7};
        vector<int> plist(raw_plist, raw_plist + sizeof(raw_plist) / sizeof(int));
        vector<int> nlist(raw_nlist, raw_nlist + sizeof(raw_nlist) / sizeof(int));


        phi->print(true);


        auto start = sc.now();

        Solver sv(nvar, phi);

        auto model = sv.solve(100, false);

        //model = sv.solve(100, true);

        auto end = sc.now();

        auto time_span = static_cast<chrono::duration<double>>(end - start);

        cout << "total time: " << endl;

        cout << nvar << " literals : " << ncls << " clause : " << time_span.count() << " seconds\n";

        model->print(true);


        delete io;

    }

    catch (char const *msg) {
        cout << "Main catch msg: " << msg << endl;
    }
    catch (const exception &e) {
        cout << "Main cat exception: " << e.what() << endl;
    }


}

