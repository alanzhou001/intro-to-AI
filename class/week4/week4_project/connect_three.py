"""
Connect 3 Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None

ROW_COUNT = 5
COLUMN_COUNT = 3

NUM_TO_WIN = 3

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]


# board=initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    ##To do
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
     ##To do
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    ##To do
    raise NotImplementedError




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ##To do
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    ##To do
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ##To do
    raise NotImplementedError


def minimax(board, alpha=-math.inf, beta=math.inf):
    """
    Returns best action and utility for the current player on the board.
    """
    ##To do
    raise NotImplementedError
