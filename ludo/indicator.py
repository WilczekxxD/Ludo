import time
from ludo.field import Field
from ludo.path import Path
from ludo.final import Final
from ludo.starting import Starting
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


class Indicator:

    def __init__(self, win, color, x, y, r):
        self.win = win
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.r = int(r)

    def on(self):
        pygame.draw.circle(self.win, self.color, (self.x, self.y), self.r)

    def off(self):
        pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), self.r)