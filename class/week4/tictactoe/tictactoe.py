"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# board=initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board=[item for sublist in board for item in sublist]
    if flat_board.count('X')==flat_board.count('O'):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action=set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is None:
                action.add((i,j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # raise error
    if action[0] not in range(0,len(board)) or action[1] not in range(0,len(board[0])) or action not in actions(board):
        sys.exit("Not valid action")

    # result board
    next_board=copy.deepcopy(board)
    next_board[action[0]][action[1]]=player(board)
    return next_board


# board=result(board,(,0))
# action=(1,1)

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ## Horizontally
    place=[i for i in board]

    ## Vertically
    for j in range(len(board[0])):
        place.append([i[j] for i in board])

    ## Diagonally
    place.append([board[0][0],board[1][1],board[2][2]])
    place.append([board[0][2],board[1][1],board[2][0]])

    ## Count number of X and O
    X_result=[i.count('X') for i in place]
    O_result = [i.count('O') for i in place]

    ## Check whether three in a row
    if X_result.count(3):
        return X
    if O_result.count(3):
        return O
    else:
        return None

# winner(board)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or len(actions(board))==0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board)==X:
        return 1
    if winner(board)==O:
        return -1
    else:
        return 0

def Max_Value(board):

    if terminal(board):
        return utility(board)

    v=-np.inf
    action=actions(board)
    for a in action:
        v = max(v,Min_Value(result(board, a)))

    return v

def Min_Value(board):
    if terminal(board):
        return utility(board)

    action=actions(board)
    v=np.inf

    for a in action:
        v = min(v, Max_Value(result(board, a)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    action=actions(board)

    if player(board)==X:
        v=-np.inf
        for a in action:
            temp=Min_Value(result(board, a))
            if temp>v:
                v=temp
                solution=a
        return solution

    if player(board)==O:
        v=np.inf
        for a in action:
            temp=Max_Value(result(board, a))
            if temp<v:
                v=temp
                solution=a
        return solution


