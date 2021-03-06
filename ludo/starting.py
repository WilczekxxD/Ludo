import time
from ludo.field import Field
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


# it is the 4 starting places
class Starting:

    def __init__(self, win, color, x, y, side):
        self.fields = []
        # coordinates of upper left square
        self.win = win
        self.x = x
        self.y = y
        # side of squares:
        self.side = side
        self.color = color
        self.create_fields()

    def reset(self):
        for field in self.fields:
            field.reset_pawns()

    def create_fields(self):
        # here probably could be a smart for but 4 squares is not that much work
        self.fields.append(Field(self.win, self.color, self.x, self.y, self.side))
        self.fields.append(Field(self.win, self.color, self.x + self.side, self.y, self.side))
        self.fields.append(Field(self.win, self.color, self.x, self.y + self.side, self.side))
        self.fields.append(Field(self.win, self.color, self.x + self.side, self.y + self.side, self.side))

    def draw(self):
        for field in self.fields:
            field.draw()
