from ppsat import Literal, Clause, Model, State, ConditionalStack, Formula, generate_case, RandHeuristic, WeightedRandHeuristic, DetHeuristic, copy
import  time
import sys

def solve(starting_formula:Formula, h, max_steps:int):
    b = True

    stack = ConditionalStack()
    i = 0
    current_literal = Literal.default()
    current_model = Model.default()
    current_formula = copy.deepcopy(starting_formula)
    conflict = False
    t_begin = 0
    t_end = 0
    t_begin_init = time.perf_counter()
    print("finish\nconnected\nfinish generate")
    while True:
        #logging.debug("=={}=================================".format(i))
        #logging.debug("loop head: {} {} {}".format(current_formula, current_literal, current_model))
        if i != 0:
            t_begin = time.perf_counter()
            check_result = current_formula.check(current_literal)
            if check_result == Formula.FORMULA_EMPTY:
                # print("SAT", current_model)
                return i
            elif check_result == Formula.HAS_NEGATION or b:
                # print("XXXXXXXXXXXXXXXXXXXXXXX")
                conflict = True
                t_end = time.perf_counter()
                print("check:", t_end - t_begin)
                t_begin = time.perf_counter()
                if stack.empty():
                    if (not b):
                        return i
                state = stack.pop(conflict)
                current_literal = state.ell.opp()
                current_model = state.model
                t_end = time.perf_counter()
                print("backtrack:", t_end - t_begin)
                current_formula = copy.deepcopy(starting_formula)
                current_formula.simplify(current_model)


            conflict = False
            t_begin = time.perf_counter()
            current_formula.propagation(current_literal)
            current_model.add(current_literal)
            t_end = time.perf_counter()
            print("propagation:", t_end - t_begin)

        if (i >= max_steps):
            t_end_init = time.perf_counter()
            print("total time:", t_end_init - t_begin_init)
            return -1


        t_begin = time.perf_counter()
        b_unit, l0 = current_formula.unit_search()
        t_end = time.perf_counter()
        print("unit search: ", t_end - t_begin)

        t_begin = time.perf_counter()
        l1 = h.decision(current_formula)
        stack.push(not b_unit and not conflict, State(l1, current_model))
        t_end = time.perf_counter()
        print("guess: ", t_end - t_begin)
        t_begin = time.perf_counter()
        if conflict == False:
            if b_unit == True:
                current_literal = l0
            else:
                current_literal = l1
        t_end = time.perf_counter()
        print("mux: ", t_end - t_begin)
        i += 1



if __name__ == "__main__":
    nvar = int(sys.argv[1])
    ncls = int(sys.argv[2])
    nltr = int(sys.argv[3])
    htype = sys.argv[4]
    if htype == "rand":
        h = RandHeuristic
    elif htype == "det":
        h = WeightedRandHeuristic
    elif htype == "wrand":
        h = DetHeuristic
    else:
        raise Exception("Unknown heuristic type " + htype)
    f = generate_case(nvar=nvar, ncls=ncls, nltr=nltr)
    #logging.disable('DEBUG')

    # st = ConditionalStack()
    #
    # t_begin = time.perf_counter()
    # f.unit_search()
    # t_end = time.perf_counter()
    # print("unit search: ", t_end - t_begin)
    #
    # t_begin = time.perf_counter()
    # ell = h.decision(f)
    # st.push(True, ell)
    # t_end = time.perf_counter()
    # print("guess: ", t_end - t_begin)
    #
    # t_begin = time.perf_counter()
    # f.check(Literal.parse("1"))
    # t_end = time.perf_counter()
    # print("check: ", t_end - t_begin)
    #
    # t_begin = time.perf_counter()
    # res = st.pop(True)
    # t_end = time.perf_counter()
    # print("backtrack: ", t_end - t_begin)
    #
    # t_begin = time.perf_counter()
    # f.propagation(Literal.parse("1"))
    # t_end = time.perf_counter()
    # print("propagation: ", t_end - t_begin)

    t_begin = time.perf_counter()
    solve(f, h, 1)
    t_end = time.perf_counter()
    # print("total time: ", t_end - t_begin)
    print(nvar, "variables,",  nltr, "literals,", ncls, "clauses.")
    print("-1")




