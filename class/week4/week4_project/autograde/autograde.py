import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connect_three import *
import copy

@pytest.fixture
def empty_board():
    return initial_state()

@pytest.fixture
def board1(empty_board):
    board = copy.deepcopy(empty_board)
    board[4][1] = X
    board[3][1] = O
    return board

@pytest.fixture
def board2(board1):
    board = copy.deepcopy(board1)
    board[2][1] = X
    return board

@pytest.fixture
def board3(empty_board):
    board = copy.deepcopy(empty_board)
    board[0] = [X, O, None]
    board[1] = [O, X, None]
    board[2] = [O, X, X]
    board[3] = [X, O, O]
    board[4] = [O, X, X]
    return board

@pytest.fixture
def board4():
    return [[X, O, X], [O, O, X], [X, X, O], [O, O, X], [X, X, O]]

def test_player(board1, board2):
    assert player(board1) == X
    assert player(board2) == O

def test_actions(board1, board2):
    assert actions(board1) == {(4, 0), (2, 1), (4, 2)}, 'actions function is wrong'
    assert actions(board2) == {(4, 0), (1, 1), (4, 2)}, 'actions function is wrong'

def test_result(board1):
    temp_board = copy.deepcopy(board1)
    temp_board[4][0] = X
    assert result(board1, (4, 0)) == temp_board, 'result function is wrong'

    temp_board = copy.deepcopy(board1)
    temp_board[2][1] = X
    assert result(board1, (2, 1)) == temp_board, 'result function is wrong'

def test_winner(board1, board2, board3, board4):
    assert winner(board1) is None, 'winner function is wrong'
    assert winner(board2) is None, 'winner function is wrong'
    assert winner(board3) == X, 'winner function is wrong'
    assert winner(board4) is None, 'winner function is wrong'

def test_terminal(board1, board2, board3, board4):
    assert terminal(board1) == False, 'terminal function is wrong'
    assert terminal(board2) == False,'terminal function is wrong'
    assert terminal(board4) == True, 'terminal function is wrong'

def test_utility(board1, board2, board3, board4):
    assert utility(board1) == 0, 'utility function is wrong'
    assert utility(board2) == 0, 'utility function is wrong'
    assert utility(board3) == 1, 'utility function is wrong'
    assert utility(board4) == 0, 'utility function is wrong'

def test_minimax(board1, board2):
    assert minimax(board1)[0] == (2, 1), 'minimax function does not return the correct action'
    assert minimax(board2)[0] == (1, 1), 'minimax function does not return the correct action'
