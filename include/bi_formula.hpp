
#pragma once
#include "formula.hpp"

class BILiteral: public Literal {
  
  private:
  	    Bit** ind;
  	  //  int 

  public:

  	BILiteral( int nvar ): Literal(nvar){
  		ind = new Bit* [2];
        for(int i = 0; i < 2; i++)
   	          ind[i] = new Bit[nvar];   		 
  	}

  	
  	BILiteral(Bit** _ind, int _nvar): Literal(_nvar){
  		ind = new Bit* [2];
  		ind[0] = new Bit[nvar];
  		ind[1] = new Bit[nvar];
  		for (int  j = 0; j< _nvar; j++){
  			ind[0][j] = _ind[0][j];
  			ind[1][j] = _ind[1][j];
  		}  		 

  	}

  	
  	BILiteral( int nvar, int index, bool sign): Literal(nvar){
  		ind = new Bit* [2];
  		ind[0] = new Bit[nvar];  
  		ind[1] = new Bit[nvar]; 
  		
  		for(int i = 0; i < nvar; i++){
  			  bool b = (index == i);
  			//  cout << (b and (not sign)) << endl;
   	          ind[0][i] =  Bit(b and (not sign), PUBLIC); 
   	          ind[1][i] =  Bit(b and sign, PUBLIC);
   	          // cout << i << ":" << ind[1][i].reveal<bool>() <<endl;
   	    }
        		 
  	}

  	BILiteral( int nvar, Integer index, Bit sign): Literal(nvar){
  		ind = new Bit* [2];
  		ind[0] = new Bit[nvar];  
  		ind[1] = new Bit[nvar]; 
  		for(int i = 0; i < nvar; i++){
  			// cout<<"test???"<< i << endl;
  			  Bit b = (index.equal(Integer(12, i, PUBLIC)));
   	          ind[0][i] =  b & !sign; 
   	          ind[1][i] =  b & sign;

   	    }
  	}

  	virtual unique_ptr<Literal> default_value() const {
  		return make_unique<BILiteral>(nvar);
  	}

  	virtual unique_ptr<Literal> copy() const {
  		
  		return make_unique<BILiteral>(ind, nvar);		 

  	}


  	virtual void set_index(int index, bool sign, Bit real) {
  		ind[sign][index] = real ;
  	}


  	
  	unique_ptr<Literal> select(Bit b) const {
  		Bit** res = new Bit* [2];
  		res[0] = new Bit[nvar];
  		res[1] = new Bit[nvar];
  		for (int j = 0; j< nvar; j++){
  			res[0][j] = ind[0][j] & b;
  			res[1][j] = ind[1][j] & b;
  		}

  		auto res_literal = make_unique<BILiteral>(res, nvar);	
  		delete[] res[0];
  		delete[] res[1];
  		delete[] res;
  		return res_literal;
  	}



  	virtual void set_index_s(Integer index, Bit sign, Bit real = Bit(1, PUBLIC)){
  		for(int i = 0; i < nvar; i++){
  			// cout<<"test???"<< i << endl;
  			  Bit b = (index .equal(Integer(12, i, PUBLIC)));
   	          ind[0][i] =  (b & !sign) & real; 
   	          ind[1][i] =  (b & sign) & real;

   	    }

  	
  	}


  	virtual Bit isIndex(int index, bool sign) const{
  		return ind[sign][index];

  	}


  	virtual void set_index_p(int index, bool sign){
  		for(int i = 0; i < nvar; i++){
  			  bool b = (index == i);
  			//  cout << (b and (not sign)) << endl;
   	          ind[0][i] =  Bit(b and not sign,PUBLIC); 
   	          ind[1][i] =  Bit(b and sign,PUBLIC);
   	          // cout << i << ":" << ind[1][i].reveal<bool>() <<endl;
   	    }
  	
  	}

  	unique_ptr<Literal> flip() const {
  		auto res = make_unique<BILiteral>(nvar);
  		for(int i = 0; i < nvar; i++){
  			res -> ind[0][i] =  ind[1][i];
  			res -> ind[1][i] =  ind[0][i];
  		}

  		return res;

  	}

  

  	virtual void print(bool test) const {
  		//if(not test) return; 
  		cout <<  "-------\n";

  		for(int i = 0; i < nvar; i++){
  			if (ind[0][i].reveal<bool>()){
  				cout << -i << " "; 
  			} 
  			if (ind[1][i].reveal<bool>()){
  				cout << i  << " "; 
  			}
  		}
  	//	cout <<  "-------\n";
  		cout << endl;
  	}

    virtual tuple<Integer, Bit> get_index()  const {
      Integer index(12, 0, PUBLIC);
      Bit sign(0, PUBLIC);
      
      for(int i = 0; i < nvar; i++){
         index = index.select(ind[0][i] | ind[1][i], Integer(12, i, PUBLIC));
        // index = index.select(ind[1][i], Integer(12, i, PUBLIC));
         sign = ind[1][i]| sign;
      }

      return make_tuple(index, sign);

    }



  	~BILiteral(){
  		for(int i = 0; i < 2; i++)
   	         delete[] ind[i];
   	    delete ind;
    }

}; 



