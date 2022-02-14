from pysat.solvers import Solver, MapleChrono
from pysat.formula import CNF
import multiprocessing
import time
import sys


m = MapleChrono()

def solve(filename, return_dict):
    formula = CNF(filename)
    tic = time.time()
    m.append_formula(formula)
    m.solve()

    toc = time.time()
    return_dict["solver"] = toc - tic


if __name__ == "__main__":

    filename = sys.argv[1]
    genotype = sys.argv[2]
    casenum = sys.argv[3]
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_dict["solver"] = -1


    p = multiprocessing.Process(target = solve, args= (filename,  return_dict))
    p.start()
    p.join(timeout= 100)
    p.terminate()
    m.delete()
    print(genotype, casenum, "HEHE", return_dict["solver"])
