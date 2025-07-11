"""
Tic Tac Toe Player
"""

import math
import copy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for line in board:
        for block in line:
            match block:
                case "X":
                    x_count += 1
                case "O": 
                    o_count += 1
                case None:
                    pass
                    
    if x_count == o_count:
        return X
    elif o_count < x_count:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
                
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] <= 2 and 0 <= action[1] <= 2):
        raise Exception("Action is out of bounds")
    
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Action not possible")
    
    curr_player = player(board)
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = curr_player
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verify lines
    for line in board:
        if line[0] == line[1] == line[2] != EMPTY:
            return line[0]
        
    # Verify columns
    for j in range(3):
        column_values = [board[0][j], board[1][j], board[2][j]]
        unique_values_in_column = set(column_values)
        
        if len(unique_values_in_column) == 1 and next(iter(unique_values_in_column)) != EMPTY:
            return next(iter(unique_values_in_column))

    # Verify diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is no more possible actions or there is already a winner
    if len(actions(board)) == 0 or winner(board) != None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
   
    curr_player = player(board)
    
    if curr_player == X:
        best_value = -math.inf
        best_action = None
        
        for action in actions(board):
            new_board = result(board, action)
            value = min_value(new_board)
            
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
            
    if curr_player == O:
        best_value = math.inf
        best_action = None
        
        for action in actions(board):
            new_board = result(board, action)
            value = max_value(new_board)
            
            if value < best_value:
                best_value = value
                best_action = action
        return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
    
    
def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v