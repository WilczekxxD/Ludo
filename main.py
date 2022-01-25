import pygame
from board import Board
from player import Player
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def main():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    teams = [0, 1, 2, 3]
    win_side = 610
    win = pygame.display.set_mode((win_side, win_side))
    margin = 5

    players = [Player(colors[i], teams[i], )]


