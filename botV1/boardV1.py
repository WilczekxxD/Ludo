import time
from ludo.board import board
from ludo.field import Field
from ludo.path import Path
from ludo.final import Final
from ludo.starting import Starting
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


# combining starting, final fields and path into one board

# TODO zobacz czy to kopiuje czy wysyła pointery
class BoardV1(board):

    def __init__(self, board):
        self.board = board
        self.path = board.path
        self.finish_lines = []
        self.finish_lines = board.finish_lines
        self.starts = board.starts


if __name__ == "__main__":
    WIN_SIDE = 610
    win = pygame.display.set_mode((WIN_SIDE, WIN_SIDE))
    MARGIN = 5
    color_numbers = {
        "r": 0,
        "g": 1,
        "b": 2,
        "y": 3
    }

    board = Board(win, WIN_SIDE, MARGIN)
    board.draw()
    time.sleep(10)