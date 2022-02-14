#!/usr/bin/env python3.8
from __future__ import annotations
from typing import List, Set, Iterator, Union, Tuple
import copy
import re
import random
import sys



re_Literal_capture = r"(-?)([0-9]+)"
re_Literal = r"(?:-?)(?:[0-9]+)"
re_Clause = r"\([^\(\)]+\)" # matches with anything inside parentheses

class Literal:
    def __init__(self, var:int, is_neg:bool=False):
        self.var = var
        self.is_neg = is_neg
    
    @staticmethod
    def default() -> Literal:
        return Literal(var=0, is_neg=False)
    
    def select(self, use_other:bool, other:Literal) -> Literal:
        return other if use_other else self
    
    def opp(self) -> Literal:
        return Literal(self.var, not self.is_neg)
    
    def is_opp(self, other:Literal) -> bool:
        return self.var == other.var and self.is_neg == (not other.is_neg)

    def __hash__(self) -> int:
        return hash( (self.is_neg, self.var) )
    
    def __eq__(self, other:Literal) -> bool:
        return self.var == other.var and self.is_neg == other.is_neg
    
    def __lt__(self, other:Literal) -> bool:
        return self.var < other.var or (self.var == other.var and self.is_neg and not other.is_neg)

    def __repr__(self) -> str:
        sign_str = "-" if self.is_neg else ""
        return "{sign}{var}".format(sign=sign_str, var=self.var)
    
    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def parse(text:str) -> Literal:
        match = re.match(re_Literal_capture, text)
        groups = match.groups()
        sig = groups[0]
        var = groups[1]
        return Literal(int(var), sig == "-")
    


class LiteralSet:
    def __init__(self, literals:Set[Literal]):
        # assume there's no conflit in literals
        self.literals = literals

    def select(self, use_other:bool, other:LiteralSet) -> LiteralSet:
        return other if use_other else self

    def contains(self, literal:Literal) -> bool:
        return literal in self.literals
    
    def __eq__(self, other:LiteralSet) -> bool:
        return self.literals == other.literals
    
    def repr_list(self) -> List[str]:
        return [repr(l) for l in sorted(self.literals)]

    @staticmethod
    def parse_set(text:str) -> Set[Literal]:
        matches = re.findall(re_Literal, text)
        return set([Literal.parse(match) for match in matches])



class Clause(LiteralSet):
    def remove(self, literal:Literal) -> Clause:
        if literal in self.literals:
            res = copy.deepcopy(self)
            res.literals.remove(literal)
            return res
        else:
            return self
    
    def unit(self) -> bool:
        return len(self.literals) == 1

    def get_unit_literal(self) -> Literal:
        if not self.unit():
            raise Exception("Clause {c} is not unit".format(c=self))
        # get the first element (which is the only element) from set
        l = next(iter(self.literals))
        return l

    def __iter__(self) -> Iterator[Literal]:
        return iter(self.literals)
    
    def __repr__(self) -> str:
        return "(" + " ".join(self.repr_list()) + ")"
    
    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def parse(text:str) -> Clause:
        literals = Clause.parse_set(text)
        return Clause(literals)



class Model(LiteralSet):
    @staticmethod
    def default() -> Model:
        return Model(set())
    
    def add(self, literal:Literal) -> None:
        if self.contains(literal.opp()):
            raise Exception("Model {m} already contains the negation of {l}".format(m=self, l=literal))
        self.literals.add(literal)
    
    def __iter__(self) -> Iterator[Literal]:
        return iter(self.literals)
    
    def __repr__(self) -> str:
        return "{" + " ".join(self.repr_list()) + "}"
    
    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def parse(text:str) -> Model:
        literals = Model.parse_set(text)
        return Model(literals)



class State:
    def __init__(self, ell:Literal, model:Model):
        self.ell = ell
        self.model = model
    
    def select(self, use_other:bool, other:State) -> State:
        return other if use_other else self
    
    @staticmethod
    def default():
        return State(Literal.default(), Model.default())
    
    def __eq__(self, other: State) -> bool:
        return self.ell == other.ell and self.model == other.model

    def __repr__(self) -> str:
        return "<{ell}, {model}>".format(ell=self.ell, model=self.model)
    
    def __str__(self) -> str:
        return repr(self)



class ConditionalStack:
    def __init__(self):
        self.stack = []
    
    def push(self, is_real:bool, v:State) -> None:
        if is_real:
            self.stack.append(copy.deepcopy(v))
        # otherwise do nothing
    
    def pop(self, is_real:bool) -> State:
        if is_real:
            # if stack is empty, let it raise exception
            return self.stack.pop()
        else:
            return State.default()
    
    def empty(self) -> bool:
        return len(self.stack) == 0
    
    def __repr__(self) -> str:
        return repr(self.stack)
    
    def __str__(self) -> str:
        return repr(self)




class Formula:
    def __init__(self, clauses:List[Clause]):
        self.clauses = clauses
    
    def select(self, use_other:bool, other:Formula) -> Formula:
        return other if use_other else self

    def remove(self, clause:Clause) -> None:
        self.clauses = [c for c in self.clauses if c != clause]

    FORMULA_EMPTY = 0
    HAS_NEGATION = 1
    UNDETERMINED = 2
    @staticmethod
    def check_result_str(res:int) -> str:
        if res == Formula.FORMULA_EMPTY:
            return "FORMULA_EMPTY"
        elif res == Formula.HAS_NEGATION:
            return "HAS_NEGATION"
        else:
            return "UNDETERMINED"

    def check(self, literal:Literal) -> int:
        '''
        return FORMULA_EMPTY if formula contains no clause.
        return HAS_NEGATION if argument is the negation of one unit clause in this formula.
        return UNDETERMINED otherwise.
        '''
        if len(self.clauses) == 0:
            return Formula.FORMULA_EMPTY
        for clause in self.clauses:
            if clause.unit():
                l = clause.get_unit_literal()
                if literal.is_opp(l):
                    return Formula.HAS_NEGATION
        return Formula.UNDETERMINED
    
    def propagation(self, literal:Literal) -> None:
        literal_opp = literal.opp()
        new_clauses = []
        for clause in self.clauses:
            if clause.contains(literal):
                continue
            if clause.contains(literal_opp):
                new_clause = clause.remove(literal_opp)
                # assume new_clause is not empty
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        self.clauses = new_clauses
    
    def simplify(self, model:Model) -> None:
        for literal in model:
            self.propagation(literal)
    
    def unit_search(self) -> Tuple[bool, Literal]:
        '''
        Return the last unit clause if there's any.
        Otherwise return default Literal.
        '''
        found = False
        literal = Literal.default()
        for clause in self.clauses:
            is_unit = clause.unit()
            if is_unit:
                found = True
                literal = clause.get_unit_literal()
        return (found, literal)
    
    def decision(self) -> Literal:
        """
        Find most occurring literal in the formula.
        """
        if len(self.clauses) == 0:
            return Literal.default()
        counter = {}
        for clause in self.clauses:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 0
        return max(counter, key=lambda k:counter[k])

    def __eq__(self, other:Formula) -> bool:
        return self.clauses == other.clauses

    def __repr__(self) -> str:
        return "\n".join([repr(c) for c in self.clauses])
    
    def __str__(self) -> str:
        return repr(self)
    
    @staticmethod
    def parse(text:str) -> Formula:
        matches = re.findall(re_Clause, text)
        return Formula([Clause.parse(match) for match in matches])



class Heuristic:
    @staticmethod
    def decision(formula:Formula) -> Literal:
        raise NotImplemented

class DetHeuristic(Heuristic):
    @staticmethod
    def decision(formula:Formula) -> Literal:
        """
        Find most occurring literal in the formula.
        """
        if len(formula.clauses) == 0:
            return Literal.default()
        counter = {}
        for clause in formula.clauses:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 0
        return max(counter, key=lambda k:counter[k])

class RandHeuristic(Heuristic):
    @staticmethod
    def decision(formula:Formula) -> Literal:
        """
        Randomly choose from existing literals.
        """
        if len(formula.clauses) == 0:
            return Literal.default()
        literals = set()
        for clause in formula.clauses:
            for literal in clause:
                literals.add(literal)
        return random.choice(list(literals))

class WeightedRandHeuristic(Heuristic):
    @staticmethod
    def decision(formula:Formula) -> Literal:
        """
        Randomly choose from existing literals.
        """
        if len(formula.clauses) == 0:
            return Literal.default()
        literals = []
        for clause in formula.clauses:
            for literal in clause:
                literals.append(literal)
        return random.choice(literals)



def solve(starting_formula:Formula, h, max_steps:int):
    stack = ConditionalStack()
    i = 0
    current_literal = Literal.default()
    current_model = Model.default()
    current_formula = copy.deepcopy(starting_formula)
    conflict = False
    while True:
        #logging.debug("=={}=================================".format(i))
        #logging.debug("loop head: {} {} {}".format(current_formula, current_literal, current_model))
        if i != 0:
            check_result = current_formula.check(current_literal)
            #logging.debug("check_result={}".format(Formula.check_result_str(check_result)))
            if check_result == Formula.FORMULA_EMPTY:
                # print("SAT", current_model)
                return i
            elif check_result == Formula.HAS_NEGATION:
                # print("XXXXXXXXXXXXXXXXXXXXXXX")
                conflict = True
                if stack.empty():
                    return i
                state = stack.pop(conflict)
                current_literal = state.ell.opp()
                current_model = state.model
                current_formula = copy.deepcopy(starting_formula)
                current_formula.simplify(current_model)
            else: # check_result == Formula.UNDETERMINED
                conflict = False
                current_formula.propagation(current_literal)
                current_model.add(current_literal)
        #logging.debug("conflict={}".format(conflict))
        #logging.debug("current_formula={}".format(current_formula))
        b_unit, l0 = current_formula.unit_search()
        #logging.debug("b_unit={} l0={}".format(b_unit, l0))
        l1 = h.decision(current_formula)
        #logging.debug("l1={}".format(l1))
        stack.push(not b_unit and not conflict, State(l1, current_model))
        if conflict == False:
            if b_unit == True:
                current_literal = l0
            else:
                current_literal = l1
        # otherwise, current_literal remains unchanged
        #logging.debug("after_model={}".format(current_model))
        # print(i, len(current_formula.clauses), len(stack.stack), len(current_model.literals))
        if (i >= max_steps):
            return -1
        i += 1


def generate_random_set(range:int, length:int) -> Set[int]:
    s = set()
    while len(s) < length:
        x = random.randint(1, range-1) # x in [1, range-1]
        if x not in s:
            s.add(x)
    return s

def generate_case(nvar:int, ncls:int, nltr:int) -> Formula:
    cls_list = []
    for i in range(0, ncls):
        ltr_set = set()
        for var in generate_random_set(nvar, nltr):
            is_neg = bool(random.getrandbits(1))
            ltr = Literal(var, is_neg)
            ltr_set.add(ltr)
        cls = Clause(ltr_set)
        cls_list.append(cls)
    return Formula(cls_list)

def read_formula_from_file(filename:str):

    with open(filename, "r") as infile:
        first_line = infile.readline().split()
        nvar = int(first_line[2])
        ncls = int(first_line[3])
        cls_list = []
        for i in range(0, ncls):
            line = infile.readline().split()
            cls = Clause.parse(" ".join(line[:-1]))
            cls_list.append(cls)
        return nvar, ncls, Formula(cls_list)


if __name__ == "__main__":
    #logging.basicConfig(level=#logging.INFO)

    # nvar = int(sys.argv[1])
    # ncls = int(sys.argv[2])
    # nltr = int(sys.argv[3])
    # h = RandHeuristic if sys.argv[4] == "rand" else DetHeuristic
    # f = generate_case(nvar=nvar, ncls=ncls, nltr=nltr)
    # steps = solve(f, h)
    # print(nvar, ncls, nltr, steps)

    filename = sys.argv[1]
    genotype = sys.argv[2]
    casenum = sys.argv[3]
    htype = sys.argv[4]
    nvar, ncls, f = read_formula_from_file(filename)

    if htype == "rand":
        h = RandHeuristic
        steps_length = (nvar * ncls * 0.48)/100000
    elif htype == "det":
        h = WeightedRandHeuristic
        steps_length = (nvar * ncls * 0.43)/100000
    elif htype == "wrand":
        h = DetHeuristic
        steps_length = (nvar * ncls * 1.05)/100000
    else:
        raise Exception("Unknown heuristic type " + htype)
    steps = solve(f, h, int(100000/steps_length))
    # print(nvar, ncls, steps)
    if steps == -1:
        print(genotype, casenum, htype, -1)
    else:
        print(genotype, casenum, htype, steps * steps_length)
