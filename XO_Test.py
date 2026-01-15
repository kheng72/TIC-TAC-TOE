import numpy as np
import math

O = []      # ผู้เล่น (Min)
X = []      # AI (Max)

win = [[1,2,3],
       [4,5,6],
       [7,8,9],
       [1,4,7],
       [2,5,8],
       [3,6,9],
       [1,5,9],
       [3,5,7]]

def checkWin(P):
    for w in win:
        if all(i-1 in P for i in w):
            return True
    return False

def displayOX():
    board = np.array([' ']*9)
    for o in O:
        board[o] = 'O'
    for x in X:
        board[x] = 'X'
    print(board.reshape(3,3))

def evalState(O, X):
    if checkWin(X):
        return 1
    if checkWin(O):
        return -1
    return 0

def minimax(O, X, depth, alpha, beta, isMax):
    score = evalState(O, X)
    if score != 0 or depth == 0 or len(O)+len(X) == 9:
        return score

    if isMax:  # AI (X)
        maxEval = -math.inf
        for m in range(9):
            if m not in O+X:
                X.append(m)
                eval = minimax(O, X, depth-1, alpha, beta, False)
                X.pop()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break   # Alpha-Beta Pruning
        return maxEval
    else:      # Player (O)
        minEval = math.inf
        for m in range(9):
            if m not in O+X:
                O.append(m)
                eval = minimax(O, X, depth-1, alpha, beta, True)
                O.pop()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break   # Alpha-Beta Pruning
        return minEval

def AI():
    bestScore = -math.inf
    bestMove = None
    for m in range(9):
        if m not in O+X:
            X.append(m)
            score = minimax(O, X, 9, -math.inf, math.inf, False)
            X.pop()
            if score > bestScore:
                bestScore = score
                bestMove = m
    return bestMove

while True:
    move = int(input('Choose position [1-9]')) - 1
    while move in O+X or move > 8 or move < 0:
        move = int(input('Bad move: Choose position [1-9]')) -1
    O.append(move)
    displayOX()
    if checkWin(O):
        print('O win')
        break
    if len(O) + len(X) == 9:
        print('Draw')
        break
    X.append(AI())
    displayOX()
    if checkWin(X):
        print('X win')
        break 
    if len(O) + len(X) == 9:
        print('Draw')
        break 