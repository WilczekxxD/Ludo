import time
from ludo.field import Field
from ludo.path import Path
from ludo.final import Final
from ludo.starting import Starting
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


# combining starting, final fields and path into one board
class Board:

    def __init__(self, win, side, margin,):
        # for drawing
        self.side = side
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.margin = margin
        self.grid_side = (self.side - self.margin * 2) / 15
        self.win = win
        
        # logic
        self.path = Path(self.win, self.side, self.margin)
        self.finish_lines = []
        self.create_final()
        self.starts = []
        self.create_starting()

    def create_starting(self):
        # only 4
        self.starts.append(Starting(self.win, self.colors[0], self.margin + self.grid_side * 2,
                                    self.margin + self.grid_side * 11, self.grid_side))

        self.starts.append(Starting(self.win, self.colors[1], self.margin + self.grid_side * 2,
                                    self.margin + self.grid_side * 2, self.grid_side))

        self.starts.append(Starting(self.win, self.colors[2], self.margin + self.grid_side * 11,
                                    self.margin + self.grid_side * 2, self.grid_side))

        self.starts.append(Starting(self.win, self.colors[3], self.margin + self.grid_side * 11,
                                    self.margin + self.grid_side * 11, self.grid_side))

    def create_final(self):
        # only 4 no need for any smart for
        # added in a r, g, b, y order if that will prove problematic could use dictionary
        self.finish_lines.append(Final(self.win, self.colors[0], self.margin + self.grid_side * 7,
                                       self.side - self.margin - self.grid_side * 2, [0, -self.grid_side], self.grid_side))

        self.finish_lines.append(Final(self.win, self.colors[1], self.margin + self.grid_side,
                                       self.margin + self.grid_side * 7, [self.grid_side, 0], self.grid_side))

        self.finish_lines.append(Final(self.win, self.colors[2], self.margin + self.grid_side * 7,
                                       self.margin + self.grid_side, [0, self.grid_side], self.grid_side))

        self.finish_lines.append(Final(self.win, self.colors[3], self.side - self.margin - self.grid_side * 2,
                                       self.margin + self.grid_side * 7, [-self.grid_side, 0], self.grid_side))

    def draw(self):
        self.path.draw()
        for final in self.finish_lines:
            final.draw()
        for start in self.starts:
            start.draw()


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