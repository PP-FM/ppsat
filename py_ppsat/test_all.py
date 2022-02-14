#!/usr/bin/env python3.8

import unittest
from ppsat import Literal, Clause, Model, State, ConditionalStack, Formula, solve



class TestLiteral(unittest.TestCase):
    def test_init(self):
        l1 = Literal(42)
        self.assertEqual(repr(l1), "42")
        l2 = Literal(100, True)
        self.assertEqual(repr(l2), "-100")
    
    def test_default(self):
        l = Literal.default()
        self.assertEqual(repr(l), "0")
    
    def test_eq(self):
        l1 = Literal(7, True)
        l2 = Literal(7, True)
        l3 = Literal(8, False)
        self.assertEqual(l1, l1)
        self.assertEqual(l1, l2)
        self.assertNotEqual(l1, l3)

    def test_select(self):
        l1 = Literal(1, True)
        l2 = Literal(2, False)
        res1 = l1.select(False, l2)
        res2 = l1.select(True, l2)
        self.assertEqual(res1, l1)
        self.assertEqual(res2, l2)
    
    def test_opp(self):
        l1 = Literal(1, True)
        l1_opp = Literal(1, False)
        self.assertEqual(l1.opp(), l1_opp)
    
    def test_parse(self):
        l1 = Literal(1, True)
        l2 = Literal(2, False)
        self.assertEqual(Literal.parse("-1"), l1)
        self.assertEqual(Literal.parse("2"), l2)



class TestClause(unittest.TestCase):
    def test_init(self):
        c1 = Clause({Literal(1), Literal(2, True)})
        self.assertEqual(repr(c1), "(1 -2)")
    
    def test_parse(self):
        c1 = Clause({Literal(1), Literal(2, True)})
        c2 = Clause({Literal(42, True)})
        self.assertEqual(Clause.parse("(1 -2)"), c1)
        self.assertEqual(Clause.parse("(-42)"), c2)

    def test_eq(self):
        c1 = Clause.parse("(1 -2)")
        c2 = Clause.parse("(-2)")
        c = Clause.parse("(-2 1)")
        self.assertEqual(c1, c)
        self.assertNotEqual(c1, c2)
    
    def test_contains(self):
        c1 = Clause.parse("(1 -2)")
        self.assertTrue(c1.contains(Literal(1)))
        self.assertFalse(c1.contains(Literal(2)))
    
    def test_remove(self):
        c1 = Clause.parse("(1 -2)")
        c2 = Clause.parse("(-2)")
        self.assertEqual(c1.remove(Literal(1)), c2)
        self.assertEqual(c1.remove(Literal(2, False)), c1)
    
    def test_select(self):
        c1 = Clause.parse("(1 -2)")
        c2 = Clause.parse("(-2)")
        self.assertEqual(c1.select(False, c2), c1)
        self.assertEqual(c1.select(True, c2), c2)
    
    def test_unit(self):
        c1 = Clause.parse("(1 -2)")
        c2 = Clause.parse("(-2)")
        self.assertFalse(c1.unit())
        self.assertTrue(c2.unit())
    
    def test_get_unit_literal(self):
        c2 = Clause.parse("(-2)")
        self.assertEqual(c2.get_unit_literal(), Literal(2, True))



class TestModel(unittest.TestCase):
    def test_init(self):
        m1 = Model({Literal(1), Literal(2, True)})
        self.assertEqual(repr(m1), "{1 -2}")
    
    def test_parse(self):
        m1 = Model({Literal(1), Literal(2, True)})
        m2 = Model({Literal(48)})
        self.assertEqual(m1, Model.parse("{1 -2"))
        self.assertEqual(m2, Model.parse("{48}"))

    # __eq__ behaves the same as Clause
    # select behaves the same as Clause
    # parse behaves the same as Clause

    def test_add(self):
        m1 = Model.parse("{1 -2}")
        m1.add(Literal(3))
        self.assertTrue(m1.contains(Literal(1)))
        self.assertTrue(m1.contains(Literal(2, True)))
        self.assertTrue(m1.contains(Literal(3)))



class TestState(unittest.TestCase):
    def test_init(self):
        s = State(Literal(1), Model.parse("{-2 3}"))
        self.assertEqual(repr(s), "<1, {-2 3}>")
    
    def test_default(self):
        s = State.default()
        self.assertEqual(repr(s), "<0, {}>")
    
    def test_select(self):
        s1 = State(Literal(1), Model.parse("{-2, 3}"))
        s2 = State(Literal(42), Model.parse("{73}"))
        self.assertEqual(s1.select(False, s2), s1)
        self.assertEqual(s1.select(True, s2), s2)

    def test_eq(self):
        s1 = State(Literal(1), Model.parse("{-2, 3}"))
        s2 = State(Literal(42), Model.parse("{73}"))
        s3 = State(Literal(1), Model.parse("{-2, 3}"))
        self.assertNotEqual(s1, s2)
        self.assertEqual(s1, s3)



class TestConditionalStack(unittest.TestCase):
    def test_init(self):
        st = ConditionalStack()
        self.assertEqual(repr(st), "[]")

    def test_push_pop(self):
        st = ConditionalStack()
        s1 = State(Literal(1), Model.parse("{64}"))
        s2 = State(Literal(2), Model.parse("{48}"))
        st.push(False, s1)
        st.push(True, s2)
        self.assertEqual(repr(st), "[<2, {48}>]")
        res1 = st.pop(False)
        self.assertEqual(res1, State.default())
        res2 = st.pop(True)
        self.assertEqual(res2, s2)
        self.assertRaises(IndexError, st.pop, True)
    


class TestFormula(unittest.TestCase):
    def test_init(self):
        c1 = Clause.parse("1 -10")
        c2 = Clause.parse("-2")
        c3 = Clause.parse("-3 99")
        f = Formula([c1, c2, c3])
        self.assertEqual(repr(f), "(1 -10) (-2) (-3 99)")
    
    def test_parse(self):
        c1 = Clause.parse("1 -10")
        c2 = Clause.parse("-1 14")
        c3 = Clause.parse("42")
        f1 = Formula([c1])
        f2 = Formula([c1, c2, c3])
        self.assertEqual(Formula.parse("(1 -10)"), f1)
        self.assertEqual(Formula.parse("(1 -10) (-1 14) (42)"), f2)

    def test_select(self):
        f1 = Formula.parse("(1 -10) (-2)")
        f2 = Formula.parse("(-3 99)")
        self.assertEqual(f1.select(False, f2), f1)
        self.assertEqual(f1.select(True, f2), f2)

    def test_eq(self):
        f1 = Formula.parse("(1 -10) (-2)")
        f2 = Formula.parse("(-2) (-3 99)")
        f3 = Formula.parse("(1 -10) (-2)")
        self.assertNotEqual(f1, f2)
        self.assertEqual(f1, f3)

    def test_remove(self):
        c1 = Clause.parse("1 -10")
        f = Formula.parse("(1 -10) (-2) (-3 99) (1 -10)")
        f.remove(c1)
        self.assertEqual(f, Formula.parse("(-2) (-3 99)"))

    def test_check(self):
        l1 = Literal.parse("1")
        l2 = Literal.parse("2")
        f0 = Formula([])
        f = Formula.parse("(1 -10) (-2)")
        self.assertEqual(f0.check(l1), Formula.FORMULA_EMPTY)
        self.assertEqual(f.check(l1), Formula.UNDETERMINED)
        self.assertEqual(f.check(l2), Formula.HAS_NEGATION)

    def test_propagation(self):
        l = Literal.parse("1")
        f = Formula.parse("(1 -10) (-1 14) (42)")
        f.propagation(l)
        self.assertEqual(f, Formula.parse("(14) (42)"))

    def test_simplify(self):
        f = Formula.parse("(1 -10) (-1 14 2) (42) (2 9)")
        m = Model.parse("{1, -2}")
        f.simplify(m)
        self.assertEqual(f, Formula.parse("(14) (42) (9)"))

    def test_unit_search(self):
        f1 = Formula.parse("(1 -10) (2) (-1 9) (10)")
        self.assertEqual(f1.unit_search(), (True, Literal.parse("10")))
        f2 = Formula.parse("(1 -10) (9 10)")
        self.assertEqual(f2.unit_search(), (False, Literal.default()))

    def test_decision(self):
        f0 = Formula([])
        self.assertEqual(f0.decision(), Literal.default())
        f1 = Formula.parse("(1 -10) (1 2) (-2 3)")
        self.assertEqual(f1.decision(), Literal.parse("1"))
        f2 = Formula.parse("(1 -10) (-1 2) (2 3)")
        self.assertEqual(f2.decision(), Literal.parse("2"))


# class TestSolver(unittest.TestCase):
#     def test_solve(self):
#         f = Formula.parse("(1 !10)")
#         solve(f)


if __name__ == "__main__":
    unittest.main()
