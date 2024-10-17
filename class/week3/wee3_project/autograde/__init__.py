import sys
import os
import signal

import check50
import check50.py


# Define a timeout handler
def handler(signum, frame):
    raise TimeoutError("The function took too long to complete.")


@check50.check()
def exists():
    """Warehouse.py exists"""
    check50.exists("Warehouse.py")
    if not os.path.exists("util.py"):
        check50.include("util.py")

@check50.check(exists)
def imports():
    """Warehouse.py imports"""
    sys.path = [""] + sys.path
    check50.py.import_("Warehouse.py")


@check50.check(imports)
def test_neighbor0():
    """Neighbor function: instruction demonstration succeeds"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse.txt"), 'A', 'CE')
    expected = set([('down', (5, 5)), ('up', (1, 5)), ('left', (3, 3))])
    result = set(m.neighbors((3,5)))
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))

@check50.check(imports)
def test_neighbor1():
    """Neighbor function: finds the neighbors when changing to another warehouse map"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse1.txt"), 'A', 'CE')
    expected = [('right', (1, 3))]
    result = m.neighbors((1,1))
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))

@check50.check(imports)
def test_neighbor2():
    """Neighbor function: finds the neighbors for locations with walls nearby"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse1.txt"), 'A', 'CE')
    expected = set([ ('right', (3, 7)),('up', (1, 5))])
    result = set(m.neighbors((3,5)))
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(imports)
def test_solve0():
    """Solve function: instruction demonstration succeeds"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse.txt"), 'A', 'BJ')
    m.solve()
    expected = ([None, 'right', 'left', 'down', 'down', 'right'], ['A', 'B', 'A', 'E', 'I', 'J'], [(1, 1), (1, 3), (1, 1), (3, 1), (5, 1), (5, 3)])
    result = m.solution
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))



@check50.check(imports)
def test_solve1():
    """Solve function: finds the path that contains repeated location"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse1.txt"), 'A', 'CE')
    m.solve()
    expected = ([None,'right', 'right', 'left', 'down', 'down', 'left', 'up'], ['A','B', 'C', 'B', 'F', 'J', 'I', 'E'], [(1, 1),(1, 3), (1, 5), (1, 3), (3, 3), (5, 3), (5, 1), (3, 1)])
    result = m.solution
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(imports)
def test_solve2():
    """Solve function: finds the shortest path"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse1.txt"), 'A', 'HE')
    m.solve()
    expected = ([None, 'right', 'right', 'down', 'right', 'down', 'left', 'left', 'left', 'up'], ['A', 'B', 'C', 'G', 'H', 'L', 'K', 'J', 'I', 'E'], [(1, 1), (1, 3), (1, 5), (3, 5), (3, 7), (5, 7), (5, 5), (5, 3), (5, 1), (3, 1)])
    result = m.solution
    if expected != result:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(imports)
def test_solve3():
    """Solve function: results raise exception when there is no solution"""
    sys.path = [""] + sys.path
    student = check50.py.import_("Warehouse.py")
    m = student.WareHouse(os.path.join(check50.internal.check_dir, "Warehouse.txt"), 'D', 'HL')
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    try:
        m.solve()
        signal.alarm(0)
    except TimeoutError:
        check50.Failure("expected exception, none caught")
    except Exception:
        signal.alarm(0)
        return
    raise check50.Failure("expected exception, none caught")