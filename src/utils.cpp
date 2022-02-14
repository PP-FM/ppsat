#include "clause.hpp"
#include "literal.hpp"
#include "formula.hpp"
#include "utils.hpp"

/*
 * */
unique_ptr<Formula> generate( int ncls, int nvar, int nltr, CLAUSE ct, LITERAL lt){
    
    vector<unique_ptr<Clause>> cls;

    for (int i = 0; i < ncls; ++i) {
        vector<int> pos_ltrs;
        vector<int> neg_ltrs;
  

        for (int j = 0;  j < nltr; j++){
            
            int raw_literal = rand() % nvar ;
            while ( (find(pos_ltrs.begin(), pos_ltrs.end(), raw_literal) != pos_ltrs.end())
                        or  (find(neg_ltrs.begin(), neg_ltrs.end(), raw_literal) != neg_ltrs.end())
                            or (raw_literal == 0)){
                    
                    raw_literal = rand() % nvar;
            }
            int sign = rand() % 2;
            if (sign == 0) pos_ltrs.push_back(raw_literal);
            else neg_ltrs.push_back(raw_literal);       
       
        }


        unique_ptr<Clause> c = nullptr;

        switch(ct) {
             case BBCLAUSE: c = make_unique<BBClause>(nvar, nltr);
             break;
        // code block
        break;
            default: c = make_unique<BIClause>(nvar) ;
        // code block
        } 

        c->set(pos_ltrs, neg_ltrs, PUBLIC);
        cls.push_back(c->copy());
    }

    auto phi = make_unique<Formula> (cls);
    return phi;
}


Integer findbound(Integer input)
{
    int size = input.size();
    Integer res(size, 0, PUBLIC);
    //cout << size << endl;

    Bit b(0, PUBLIC);
    for (int i = size - 1; i >= 0; --i)
    {

        Bit c = input.bits[i];
        b = c | b;
        res.bits[i] = b;
    }

    return res;
}

Integer get_alive_weighted_literal(const Formula& phi)  {
    Integer c(16, 0,PUBLIC);
    for (int i =0; i < phi.cls.size(); i++){
        Integer increment = count_alive_literal(*phi.cls[i]);
        c = c + Integer(16, 0, PUBLIC).select(phi.active[i], increment);
    }
    return c;
}

Integer count_alive_literal(const Clause& c ) {
    Integer count(16, 0, PUBLIC);
    for (int i = 0; i< c.nvar; i++){
        Integer tmp(16,0, PUBLIC);
        tmp.bits[0] = c.contain(i, true) | c.contain(i, false);
        count = count + tmp;
    }
    return count;

}

/*
unique_ptr<formula> ReadFormulae(string filename){
	std::ifstream infile(filename);
  int nvar, ncls;
  string prompt0, prompt1;
  infile >> prompt0 >> prompt1 >> nvar >> ncls;
  cout << ncls << "," << nvar<< "____________"<< endl;

  // formula* phi = new formula(nvar, );
  
  vector<unique_ptr<clause>> cls;

  for (int i = 0; i < ncls; ++i) {

    vector<int> pos_ltrs;
    vector<int> neg_ltrs;

    int raw_literal;
    do {
      infile >> raw_literal;
      if (raw_literal != 0) {
        printf("clause %d literal %d\n", i, raw_literal);
        if (raw_literal > 0) {
          pos_ltrs.push_back(raw_literal);
        }
        else {
          neg_ltrs.push_back(-raw_literal);
        }
      }
    } while (raw_literal != 0);

    unique_ptr<clause> c = make_unique<int_clause>(nvar,3);
    c->set(pos_ltrs, neg_ltrs, PUBLIC);
    cls.push_back(move(c));

 	}

  printf("end loop\n");
  unique_ptr<formula> phi = make_unique<formula>(cls);
  return phi;
}
*/