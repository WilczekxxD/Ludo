import time
from ludo.field import Field
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


# it is the final 6 fields for the pawn
class Final:

    def __init__(self, win, color, x, y, shift, side):
        self.fields = []
        # coordinates of first square
        self.win = win
        self.x = x
        self.y = y
        # side of squares:
        self.side = side
        # the shift after each square
        self.shift = shift
        self.color = color
        self.create_fields()

    def reset(self):
        for field in self.fields:
            field.reset_pawns()

    def create_fields(self):
        for i in range(6):
            self.fields.append(Field(self.win, self.color, self.x + self.shift[0] * i,
                                                           self.y + self.shift[1] * i, self.side))

    def draw(self):
        for field in self.fields:
            field.draw()


