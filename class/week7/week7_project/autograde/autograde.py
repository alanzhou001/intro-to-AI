import sys
import os
import pytest

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate as generate

@pytest.fixture
def setup_crossword():
    def _setup_crossword(structure_file, words_file):
        return generate.Crossword(
            os.path.join(os.path.dirname(__file__), 'data', structure_file),
            os.path.join(os.path.dirname(__file__), 'data', words_file)
        )
    return _setup_crossword

def test_exists():
    """generate.py exists"""
    assert os.path.isfile(os.path.join(os.path.dirname(__file__), '..', "generate.py")), "generate.py does not exist"

def test_imports():
    """generate.py imports"""
    try:
        import generate
    except ImportError:
        pytest.fail("Unable to import generate.py")

def test_enforce_node_consistency(setup_crossword):
    """enforce_node_consistency removes node inconsistent domain values"""
    crossword = setup_crossword("test_structure0.txt", "test_words0.txt")
    creator = generate.CrosswordCreator(crossword)
    creator.enforce_node_consistency()

    Var = generate.Variable
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY"},
        Var(0, 2, "down", 3): {"ODE"},
        Var(2, 1, "across", 5): {"TODAY", "READY"}
    }
    for var in expected:
        assert expected[var] == creator.domains[var], f"enforce_node_consistency removes node inconsistent domain values"

def test_enforce_node_consistency2(setup_crossword):
    """enforce_node_consistency removes multiple node inconsistent domain values"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)
    creator.enforce_node_consistency()

    Var = generate.Variable
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    for var in expected:
        assert expected[var] == creator.domains[var], f"enforce_node_consistency removes multiple node inconsistent domain values"

def test_revise0(setup_crossword):
    """revise does nothing when no revisions possible"""
    crossword = setup_crossword("test_structure0.txt", "test_words0.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY"},
        Var(0, 2, "down", 3): {"ODE"},
        Var(2, 1, "across", 5): {"TODAY", "READY"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY"},
        Var(0, 2, "down", 3): {"ODE"},
        Var(2, 1, "across", 5): {"TODAY", "READY"}
    }
    creator.revise(Var(0, 2, "down", 3), Var(0, 1, "across", 5))
    for var in expected:
        assert expected[var] == creator.domains[var], f"revise does nothing when no revisions possible"

def test_revise1(setup_crossword):
    """revise removes value from domain when revision is possible"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    creator.revise(Var(0, 1, "across", 5), Var(0, 2, "down", 3))
    for var in expected:
        assert expected[var] == creator.domains[var], f"revise removes value from domain when revision is possible"

def test_revise2(setup_crossword):
    """revise removes multiple values from domain when revision is possible"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"READY", "HELLO", "AMAZE"}
    }
    creator.revise(Var(2, 1, "across", 5), Var(0, 2, "down", 3))
    for var in expected:
        assert expected[var] == creator.domains[var], f"revise removes multiple values from domain when revision is possible"

def test_ac3_0(setup_crossword):
    """ac3 updates domains when only one possible solution"""
    crossword = setup_crossword("test_structure0.txt", "test_words0.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY"},
        Var(0, 2, "down", 3): {"ODE"},
        Var(2, 1, "across", 5): {"TODAY", "READY"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY"},
        Var(0, 2, "down", 3): {"ODE"},
        Var(2, 1, "across", 5): {"READY"}
    }
    creator.ac3()
    for var in expected:
        assert expected[var] == creator.domains[var], f"ac3 updates domains when only one possible solution"

def test_ac3_1(setup_crossword):
    """ac3 updates domains when multiple possible domain values exist"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"READY", "HELLO", "AMAZE"}
    }
    creator.ac3()
    for var in expected:
        assert expected[var] == creator.domains[var], f"ac3 updates domains when multiple possible domain values exist"

def test_ac3_2(setup_crossword):
    """ac3 does nothing when given an empty starting list of arcs"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    creator.ac3(arcs=[])
    for var in expected:
        assert expected[var] == creator.domains[var], f"ac3 does nothing when given an empty starting list of arcs"

def test_ac3_3(setup_crossword):
    """ac3 handles processing arcs when an initial list of arcs is provided"""
    crossword = setup_crossword("test_structure0.txt", "test_words1.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    expected = {
        Var(0, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"},
        Var(0, 2, "down", 3): {"ODE", "ELM"},
        Var(2, 1, "across", 5): {"TODAY", "READY", "HELLO", "AMAZE", "FORGE"}
    }
    creator.ac3(arcs=[(Var(0, 2, "down", 3), Var(2, 1, "across", 5))])
    for var in expected:
        assert expected[var] == creator.domains[var], f"ac3 handles processing arcs when an initial list of arcs is provided"

def test_ac3_4(setup_crossword):
    """ac3 handles multiple rounds of updates"""
    crossword = setup_crossword("test_structure1.txt", "test_words2.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(4, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"}
    }
    expected = {
        Var(0, 1, "across", 5): {"DAISY"},
        Var(0, 2, "down", 3): {"AIL"},
        Var(2, 1, "across", 5): {"SLOPE"},
        Var(2, 4, "down", 3): {"PAN"},
        Var(4, 1, "across", 5): {"GRANT", "FRONT"}
    }
    creator.ac3()
    for var in expected:
        assert expected[var] == creator.domains[var], f"ac3 handles multiple rounds of updates"

def test_ac3_5(setup_crossword):
    """ac3 returns False if no solution possible"""
    crossword = setup_crossword("test_structure1.txt", "test_words3.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(4, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"}
    }
    result = creator.ac3()
    assert result == False, "ac3 should return False when no solution is possible"

def test_assignment_complete(setup_crossword):
    """assignment_complete identifies complete assignment"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "WHERE",
        Var(0, 2, "down", 3): "RAM",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "PAINT"
    }

    assert creator.assignment_complete(assignment) == True, "assignment_complete failed to identify complete assignment"

def test_assignment_complete1(setup_crossword):
    """assignment_complete identifies incomplete assignment"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "WHERE",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "PAINT"
    }

    assert creator.assignment_complete(assignment) == False, "assignment_complete identifies incomplete assignment"

def test_consistent(setup_crossword):
    """consistent identifies consistent assignment"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "DAISY",
        Var(0, 2, "down", 3): "AIL",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "GRANT"
    }

    assert creator.consistent(assignment) == True, "consistent failed to identify consistent assignment"

def test_consistent1(setup_crossword):
    """consistent identifies when assignment doesn't meet unary constraints"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "RAT",
        Var(0, 2, "down", 3): "AIL",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "GRANT"
    }

    assert creator.consistent(assignment) == False, "consistent failed to identify assignment not meeting unary constraints"

def test_consistent2(setup_crossword):
    """consistent identifies when assignment doesn't meet binary constraints"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "DAISY",
        Var(0, 2, "down", 3): "AIL",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "CLOTH"
    }

    assert creator.consistent(assignment) == False, "consistent failed to identify assignment not meeting binary constraints"

def test_consistent3(setup_crossword):
    """consistent identifies when assignment doesn't meet uniqueness constraints"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "PAINT",
        Var(0, 2, "down", 3): "AIL",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "PAINT"
    }

    assert creator.consistent(assignment) == False, "consistent failed to identify assignment not meeting uniqueness constraints"

def test_consistent3_1(setup_crossword):
    """consistent identifies when assignment doesn't meet uniqueness constraints"""
    crossword = setup_crossword("test_structure1.txt", "test_words4.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    assignment = {
        Var(0, 1, "across", 5): "DAISY",
        Var(2, 1, "across", 5): "SLOPE",
        Var(4, 1, "across", 5): "GRANT"
    }

    assert creator.consistent(assignment) == True, "consistent failed to identify consistent incomplete assignments"

def test_order_domain_values(setup_crossword):
    """order_domain_values returns all available domain values"""
    crossword = setup_crossword("test_structure2.txt", "test_words5.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"HELLO", "COINS"},
        Var(0, 2, "down", 3): {"ELM", "ELK", "OAK"},
    }
    assignment = dict()
    result = set(creator.order_domain_values(Var(0, 1, "across", 5), assignment))
    expected = {"HELLO", "COINS"}
    assert result == expected, "order_domain_values failed to return all available domain values"

def test_order_domain_values1(setup_crossword):
    """order_domain_values returns all available domain values in correct order"""
    crossword = setup_crossword("test_structure2.txt", "test_words5.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"HELLO", "COINS"},
        Var(0, 2, "down", 3): {"ELM", "ELK", "OAK"},
    }
    assignment = dict()
    result = creator.order_domain_values(Var(0, 1, "across", 5), assignment)
    expected = ["HELLO", "COINS"]
    assert result == expected, "order_domain_values failed to return correct order"

def test_select_unassigned_variable(setup_crossword):
    """select_unassigned_variable returns variable with minimum remaining values"""
    crossword = setup_crossword("test_structure1.txt", "test_words3.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN"},
        Var(4, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"}
    }
    assignment = dict()
    result = creator.select_unassigned_variable(assignment)
    expected = Var(2, 4, "down", 3)
    assert result == expected, "select_unassigned_variable failed to return variable with minimum remaining values"

def test_select_unassigned_variable1(setup_crossword):
    """select_unassigned_variable returns variable with highest degree with remaining values tied"""
    crossword = setup_crossword("test_structure1.txt", "test_words2.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"SLOPE", "FRONT"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"SLOPE", "FRONT"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(4, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "GRANT", "WHERE", "CLOTH"}
    }
    assignment = dict()
    result = creator.select_unassigned_variable(assignment)
    expected = Var(2, 1, "across", 5)
    assert result == expected, "select_unassigned_variable failed to return variable with highest degree when remaining values are tied"

def test_select_unassigned_variable1_1(setup_crossword):
    """select_unassigned_variable doesn't choose a variable if already assigned"""
    crossword = setup_crossword("test_structure1.txt", "test_words2.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    creator.domains = {
        Var(0, 1, "across", 5): {"SLOPE", "FRONT", "DAISY"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"SLOPE", "FRONT"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(4, 1, "across", 5): {"GRANT"}
    }
    assignment = {
        Var(4, 1, "across", 5): {"GRANT"}
    }
    result = creator.select_unassigned_variable(assignment)
    expected = Var(2, 1, "across", 5)
    assert result == expected, "select_unassigned_variable shouldn't choose a variable if already assigned"

def test_backtrack(setup_crossword):
    """backtrack returns assignment if possible to calculate"""
    crossword = setup_crossword("test_structure1.txt", "test_words6.txt")
    creator = generate.CrosswordCreator(crossword)

    Var = generate.Variable
    result = creator.solve()
    expected = {
        Var(0, 1, "across", 5): "DAISY",
        Var(0, 2, "down", 3): "AIL",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "FRONT"
    }
    assert result == expected, "backtrack failed to return correct assignment"

def test_backtrack1(setup_crossword):
    """backtrack returns no assignment if not possible to calculate"""
    crossword = setup_crossword("test_structure1.txt", "test_words3.txt")
    creator = generate.CrosswordCreator(crossword)

    result = creator.solve()
    assert result is None, "backtrack should return None when no solution is possible"