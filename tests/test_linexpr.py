import pytest

from pyscipopt.scip import Model
from pyscipopt.linexpr import LinExpr, LinCons

m = Model()
x = m.addVar("x")
y = m.addVar("y")
z = m.addVar("z")

def test_variable():
    assert x == x
    assert x != y
    assert x < y or y < x

def test_operations():
    expr = x + y
    assert isinstance(expr, LinExpr)
    assert expr[x] == 1.0
    assert expr[y] == 1.0
    assert expr[z] == 0.0

    expr = -x
    assert isinstance(expr, LinExpr)
    assert expr[x] == -1.0
    assert expr[y] ==  0.0

    expr = 4*x
    assert isinstance(expr, LinExpr)
    assert expr[x] == 4.0
    assert expr[y] == 0.0

    expr = x + y + x
    assert isinstance(expr, LinExpr)
    assert expr[x] == 2.0
    assert expr[y] == 1.0

    expr = x + y - x
    assert isinstance(expr, LinExpr)
    assert expr[x] == 0.0
    assert expr[y] == 1.0

    expr = 3*x + 1.0
    assert isinstance(expr, LinExpr)
    assert expr[x] == 3.0
    assert expr[y] == 0.0
    assert expr[()] == 1.0

    expr = 1.0 + 3*x
    assert isinstance(expr, LinExpr)
    assert expr[x] == 3.0
    assert expr[y] == 0.0
    assert expr[()] == 1.0

    with pytest.raises(NotImplementedError):
        expr = x*y

    with pytest.raises(NotImplementedError):
        expr = x*(1 + y)

def test_inequality():
    expr = x + 2*y
    cons = expr <= 0
    assert isinstance(cons, LinCons)
    assert cons.lb is None
    assert cons.ub == 0.0
    assert cons.expr[x] == 1.0
    assert cons.expr[y] == 2.0
    assert cons.expr[z] == 0.0
    assert cons.expr[()] == 0.0

    cons = expr >= 5
    assert isinstance(cons, LinCons)
    assert cons.lb == 5.0
    assert cons.ub is None
    assert cons.expr[x] == 1.0
    assert cons.expr[y] == 2.0
    assert cons.expr[z] == 0.0
    assert cons.expr[()] == 0.0

    cons = 5 <= x + 2*y - 3
    assert isinstance(cons, LinCons)
    assert cons.lb == 8.0
    assert cons.ub is None
    assert cons.expr[x] == 1.0
    assert cons.expr[y] == 2.0
    assert cons.expr[z] == 0.0
    assert cons.expr[()] == 0.0
