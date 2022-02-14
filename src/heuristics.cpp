#include "heuristics.hpp"
#include "utils.hpp"
#include <time.h>       /* time */
using namespace std;

Heuristics::Heuristics() {}

Heuristics::Heuristics(int _nvar, int _ncls){
    nvar = _nvar;
    ncls = _ncls;
    srand (time(NULL));

}


unique_ptr<Literal>  Heuristics::weight_random(const Formula&  input_phi,  const State& state) const {

    unique_ptr<Model> model = state.get_model();

    unique_ptr<Formula> phi = input_phi.copy();

    phi -> simplify(*model);

    Integer alive = get_alive_weighted_literal(*phi);

    Integer multiplexer = findbound(alive);

    int ra = rand()% (ncls*3);
    int rb = rand()% (ncls*3);
    Integer index(16,0,PUBLIC);

    Integer Ra = Integer(16,ra, ALICE);
    Integer Rb = Integer(16, rb, BOB);

    Integer R = (Ra ^ Rb) & multiplexer;

    index = index.select(alive.geq(R), R);

    auto res_raw = phi-> get_target_literal(index);
    unique_ptr<Literal> res = (state.ell) -> default_value();
    res->set_index_s(get<0>(res_raw), get<1>(res_raw));

    return res;

}


unique_ptr<Literal> Heuristics::random(const Formula&  input_phi,  const State& state) const {

    /** Simplify initial formula using model. */
    unique_ptr<Model> model = state.get_model();
    unique_ptr<Formula> phi = input_phi.copy();
    phi -> simplify(*model);
    
    Integer num_of_alive = phi->num_of_alive_variables(nvar);
    //cout << "nvar = " << nvar << endl;

   // cout << "num of alive " << num_of_alive.reveal<int>() << endl;

    Integer multiplexer = findbound(num_of_alive);


    int ra = rand()% nvar;
    int rb = rand()% nvar;
    Integer index(12,0,PUBLIC);

    Integer Ra = Integer(12,ra, ALICE);
    Integer Rb = Integer(12, rb, BOB);
    Integer R = (Ra ^ Rb) & multiplexer;

    index = index.select(num_of_alive.geq(R), R);
    index = phi->get_random_alive_variable(nvar, index);




    int neg_r_a = rand() % 2;
    int neg_r_b = rand() % 2;

    Bit sign_a(neg_r_a, ALICE);
    Bit sign_b(neg_r_b, BOB);
    Bit sign = sign_a ^ sign_b ;

    unique_ptr<Literal> res = state.get_literal() -> default_value();

    res->set_index_s(index, sign);
    return res;

}


unique_ptr<Literal> Heuristics::det_freq(const Formula& input_phi, const State& s) const {

    //  chrono::steady_clock sc;   

    // auto start = sc.now();     
    
        Integer index(12, 0, PUBLIC);
        Integer max(12, 0,PUBLIC);
        Bit neg(true,  PUBLIC);
        unique_ptr<Model> model = s.get_model();
        unique_ptr<Formula> phi = input_phi.copy();
        phi -> simplify(*model);
        for(int i = 0; i < nvar ; ++i){
            Integer freq(12, 0, PUBLIC);
            for(int j = 0; j < ncls ; ++j){
                Bit contain = (phi -> cls[j])-> contain(i,0) & phi -> active[j];
                Integer increment(12, 0, PUBLIC);
                increment.bits[0] = contain;
                freq = freq + increment;
            }
            Bit swap = freq.geq(max) ;
            max = max.select(swap, freq);
            index = index.select(swap, Integer(12, i, PUBLIC));
        }


        for(int i = 0; i < nvar ; ++i){

            //printf("i=%d\n", i);
            Integer freq(12, 0, PUBLIC);
            for(int j = 0; j < ncls ; ++j){
                // printf("j=%d\n", j);
                Bit contain = (phi -> cls[j])-> contain(i,1) & phi -> active[j];
                Integer increment(12, 0, PUBLIC);
                increment.bits[0] = contain;
                freq = freq + increment;
            }

            Bit swap = freq.geq(max);
            max = max.select(swap, freq);
            neg = !swap & neg;
            index = index.select(swap, Integer(12, i, PUBLIC));
            // printf("i=%d freq=%d max=%d\n", i, freq.template reveal<int>(), max.template reveal<int>());
        }

        unique_ptr<Literal> ell = s.get_literal()-> default_value();
        ell->set_index_s(index, !neg);
        return ell;

}
