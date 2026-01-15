import pygame
import sys
import math
import numpy as np

# =====================
# GAME LOGIC (เดิมของคุณ)
# =====================

O = []  # Player
X = []  # AI

win = [
    [1,2,3],[4,5,6],[7,8,9],
    [1,4,7],[2,5,8],[3,6,9],
    [1,5,9],[3,5,7]
]

def checkWin(P):
    for w in win:
        if all(i-1 in P for i in w):
            return True
    return False

def evalState(O, X):
    if checkWin(X):
        return 1
    if checkWin(O):
        return -1
    return 0

def minimax(O, X, depth, alpha, beta, isMax):
    score = evalState(O, X)
    if score != 0 or depth == 0 or len(O) + len(X) == 9:
        return score

    if isMax:
        maxEval = -math.inf
        for m in range(9):
            if m not in O + X:
                X.append(m)
                eval = minimax(O, X, depth-1, alpha, beta, False)
                X.pop()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = math.inf
        for m in range(9):
            if m not in O + X:
                O.append(m)
                eval = minimax(O, X, depth-1, alpha, beta, True)
                O.pop()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval

def AI():
    bestScore = -math.inf
    bestMove = None
    for m in range(9):
        if m not in O + X:
            X.append(m)
            score = minimax(O, X, 9, -math.inf, math.inf, False)
            X.pop()
            if score > bestScore:
                bestScore = score
                bestMove = m
    return bestMove

# =====================
# PYGAME SETUP
# =====================

pygame.init()
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
BLUE  = (0,0,255)

LINE_WIDTH = 5
CELL_SIZE = 200
FONT = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
game_over = False
message = ""

# =====================
# DRAW FUNCTIONS
# =====================

def draw_board():
    for i in range(1,3):
        pygame.draw.line(
            screen, BLACK,
            (0, i*CELL_SIZE),
            (600, i*CELL_SIZE),
            LINE_WIDTH
        )
        pygame.draw.line(
            screen, BLACK,
            (i*CELL_SIZE, 0),
            (i*CELL_SIZE, 600),
            LINE_WIDTH
        )

def draw_marks():
    for o in O:
        r, c = divmod(o, 3)
        pygame.draw.circle(
            screen, BLUE,
            (c*CELL_SIZE+100, r*CELL_SIZE+100),
            60, 5
        )

    for x in X:
        r, c = divmod(x, 3)
        pygame.draw.line(
            screen, RED,
            (c*CELL_SIZE+40, r*CELL_SIZE+40),
            (c*CELL_SIZE+160, r*CELL_SIZE+160),
            5
        )
        pygame.draw.line(
            screen, RED,
            (c*CELL_SIZE+160, r*CELL_SIZE+40),
            (c*CELL_SIZE+40, r*CELL_SIZE+160),
            5
        )

def draw_text(text):
    surf = FONT.render(text, True, BLACK)
    rect = surf.get_rect(center=(300, 625))
    screen.blit(surf, rect)

# =====================
# UTILS
# =====================

def mouse_to_index(pos):
    x, y = pos
    if y >= 600:
        return None
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row * 3 + col

def reset_game():
    global O, X, game_over, message
    O = []
    X = []
    game_over = False
    message = ""

# =====================
# MAIN LOOP
# =====================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            idx = mouse_to_index(pygame.mouse.get_pos())
            if idx is not None and idx not in O + X:
                O.append(idx)

                if checkWin(O):
                    game_over = True
                    message = "O WIN!"
                elif len(O) + len(X) == 9:
                    game_over = True
                    message = "DRAW"
                else:
                    ai_move = AI()
                    if ai_move is not None:
                        X.append(ai_move)
                        if checkWin(X):
                            game_over = True
                            message = "X WIN!"
                        elif len(O) + len(X) == 9:
                            game_over = True
                            message = "DRAW"

    screen.fill(WHITE)
    draw_board()
    draw_marks()
    draw_text(message + "   (Press R to Restart)")
    pygame.display.update()
    clock.tick(60)
