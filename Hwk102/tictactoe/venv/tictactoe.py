# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *

# declaring the global variables

# for storing the 'x' or 'o'
# value as character
XO = 'x'

# storing the WINNER's value at
# any instant of code
WINNER = None

# to check if the game is a DRAW
DRAW = None

# to set WIDTH of the game window
WIDTH = 400

# to set height of the game window
HEIGHT = 400

# to set background color of the
# game window
WHITE = (255, 255, 255)

# color of the straightlines on that
# WHITE game board, dividing board
# into 9 parts
LINE_COLOR = (0, 0, 0)

# setting up a 3 * 3 board in canvas
BOARD = [[None] * 3, [None] * 3, [None] * 3]

# setting fps manually
FPS = 30

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
SCREEN = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)

# loading the images as python object
INITIATING_WINDOW = pg.image.load("modified_cover.png")
X_IMG = pg.image.load("x_modified.png")
Y_IMG = pg.image.load("o_modified.png")

# resizing images
INITIATING_WINDOW = pg.transform.scale(INITIATING_WINDOW, (WIDTH, HEIGHT + 100))
X_IMG = pg.transform.scale(X_IMG, (80, 80))
O_IMG = pg.transform.scale(Y_IMG, (80, 80))

def game_INITIATING_WINDOW():
    # displaying over the screen
    SCREEN.blit(INITIATING_WINDOW, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(3)
    SCREEN.fill(WHITE)

    # flush old events from menu
    pg.event.clear()

    # DRAWing vertical lines
    pg.draw.line(SCREEN, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(SCREEN, LINE_COLOR, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)

    # DRAWing horizontal lines
    pg.draw.line(SCREEN, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(SCREEN, LINE_COLOR, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)
    draw_status()
#end def game_INITIATING_WINDOW():


def draw_status():
    # getting the global variable DRAW
    # into action
    global DRAW

    if WINNER is None:
        message = XO.upper() + "'s Turn"
    else:
        message = WINNER.upper() + " won !"
    if DRAW:
        message = "Game Draw !"

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties like
    # color and WIDTH of the text
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    SCREEN.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, 500 - 50))
    SCREEN.blit(text, text_rect)
    pg.display.update()
#end def draw_status():


def check_win(ret_val=False):
    global BOARD, WINNER, DRAW

    # DRAW is what hte ret_val cares about
    # moved these lines up from the bottom
    if (all([all(row) for row in BOARD]) and WINNER is None):
        DRAW = True

    if ret_val:
        if DRAW:
            DRAW = None
            return True
        else:
            return False

            # checking for winning rows
    for row in range(0, 3):
        if ((BOARD[row][0] == BOARD[row][1] == BOARD[row][2]) and (BOARD[row][0] is not None)):
            WINNER = BOARD[row][0]
            pg.draw.line(SCREEN, (250, 0, 0),
                         (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         4)
            break

    # checking for winning columns
    for col in range(0, 3):
        if ((BOARD[0][col] == BOARD[1][col] == BOARD[2][col]) and (BOARD[0][col] is not None)):
            WINNER = BOARD[0][col]
            pg.draw.line(SCREEN, (250, 0, 0), ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            break

    # check for diagonal WINNERs
    if (BOARD[0][0] == BOARD[1][1] == BOARD[2][2]) and (BOARD[0][0] is not None):
        # game won diagonally left to right
        WINNER = BOARD[0][0]
        pg.draw.line(SCREEN, (250, 70, 70), (50, 50), (350, 350), 4)

    if (BOARD[0][2] == BOARD[1][1] == BOARD[2][0]) and (BOARD[0][2] is not None):
        # game won diagonally right to left
        WINNER = BOARD[0][2]
        pg.draw.line(SCREEN, (250, 70, 70), (350, 50), (50, 350), 4)

    # if (all([all(row) for row in BOARD]) and WINNER is None):
    #     DRAW = True
    draw_status()
# def check_win(ret_val=False):


def DRAWXO(row, col):
    global BOARD, XO

    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    if row == 1:
        posx = 30

    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
        # margin or WIDTH / 3 + 30 from
        # the left margin of the window
        posx = WIDTH / 3 + 30

    if row == 3:
        posx = WIDTH / 3 * 2 + 30

    if col == 1:
        posy = 30

    if col == 2:
        posy = HEIGHT / 3 + 30

    if col == 3:
        posy = HEIGHT / 3 * 2 + 30

    # setting up the required board
    # value to display
    BOARD[row - 1][col - 1] = XO

    if (XO == 'x'):

        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_y, posx) defined in the
        # above code
        SCREEN.blit(X_IMG, (posy, posx))
        XO = 'o'

    else:
        SCREEN.blit(O_IMG, (posy, posx))
        XO = 'x'
    pg.display.update()
#end def DRAWXO(row, col):


def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if (x < WIDTH / 3):
        col = 1

    elif (x < WIDTH / 3 * 2):
        col = 2

    elif (x < WIDTH):
        col = 3

    else:
        col = None

    # get row of mouse click (1-3)
    if (y < HEIGHT / 3):
        row = 1

    elif (y < HEIGHT / 3 * 2):
        row = 2

    elif (y < HEIGHT):
        row = 3

    else:
        row = None

    # after getting the row and col,
    # we need to DRAW the images at
    # the desired positions
    if (row and col and BOARD[row - 1][col - 1] is None):
        global X0, WINNER, DRAW
        DRAWXO(row, col)
        check_win()
        if not DRAW and not WINNER:
            # computer only moves if click was valid and game not over
            computer_move()
# end def user_click():


def evaluate(b):
    player = 'o'
    opponent = 'x'
    for row in range(0, 3):
        if b[row][0] == b[row][1] and \
                b[row][1] == b[row][2]:
            if b[row][0] == player:
                return +10
            elif b[row][0] == opponent:
                return -10
    for col in range(0, 3):
        if b[0][col] == b[1][col] and \
                b[1][col] == b[2][col]:
            if b[0][col] == player:
                return +10
            elif b[0][col] == opponent:
                return -10
    # Checking for Diagonals for X or 0 victory.
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == player:
            return +10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == player:
            return +10
        elif b[0][2] == opponent:
            return -10

    # Else if none of them have won then return 0
    return 0
# end def evaluate_BOARD(BOARD):

def minimax(BOARD, depth, is_max):
    score = evaluate(BOARD)

    # either max won with 10 or min with —10
    if abs(score) == 10:
        return score
    # if this BOARD would be a DRAW
    if check_win(True) == True:
        return 0
    # if it is maximizers turn
    if is_max:
        # repeat code from computer_move. You can clean this later
        best = -1000

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for row in range(1, 4):
            for col in range(1, 4):
                # check if cell is empty and valid
                if (BOARD[row - 1][col - 1] is None):
                    # make the move
                    BOARD[row - 1][col - 1] = 'o'
                    # compute evaluation function for this move

                    best = max(best, minimax(BOARD, depth + 1, not is_max))
                    # undo the move
                    BOARD[row - 1][col - 1] = None
        return best
    # else it is minimizer's turn
    else:
        # repeat code from computer_move, except posistive score.
        best = 1000

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for row in range(1, 4):
            for col in range(1, 4):
                # check if cell is empty and valid
                if (BOARD[row - 1][col - 1] is None):
                    # make the move
                    BOARD[row - 1][col - 1] = 'x'
                    # compute evaluation function for this move

                    best = min(best, minimax(BOARD, depth + 1, not is_max))  # min not max
                    # undo the move
                    BOARD[row - 1][col - 1] = None

        return best
    # end def minimax(BOARD, depth, is_max):


# This will return the best possible move for the player
def computer_move():
    global XO
    best_val = -1000
    best_move = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if (BOARD[row - 1][col - 1] is None):
                # make the move
                BOARD[row - 1][col - 1] = XO
                # compute evaluation function for this move

                # TODO: Imlpement minimax
                move_val = minimax(BOARD, 0, False)
                # undo the move
                BOARD[row - 1][col - 1] = None

                # If the value of the current move is
                # more than the best value, then update
                # best
                if move_val > best_val:
                    best_move = (row, col)
                    best_val = move_val

    # perform move with the largest value
    DRAWXO(best_move[0], best_move[1])  # broken right now
    check_win()
# end def computer_move():


def reset_game():
    global BOARD, WINNER, XO, DRAW
    time.sleep(3)
    XO = 'x'
    DRAW = False
    game_INITIATING_WINDOW()
    WINNER = None
    BOARD = [[None] * 3, [None] * 3, [None] * 3]
#end reset_game():


# driver Code
def main():
    # initializing the pygame window
    pg.init()

    # setting up a nametag for the
    # game window
    pg.display.set_caption("My Tic Tac Toe")

    game_INITIATING_WINDOW()

    while (True):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif pg.mouse.get_pressed()[0]:
                user_click()
                if (WINNER or DRAW):
                    reset_game()
        pg.display.update()
        CLOCK.tick(FPS)
#end def main():


if __name__ == '__main__':
    main()