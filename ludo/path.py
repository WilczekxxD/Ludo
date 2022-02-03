import time
from ludo.field import Field
import pygame
from colorama import Fore, init
init(autoreset=True)
pygame.init()


class Path:

    # the Path for the pawns

    def __init__(self, win, side, margin):
        self.win = win
        self.side = side
        self.margin = margin
        self.grid_side = (self.side - self.margin*2) / 15
        self.fields = []
        self.create_fields()

        # marking stars
        index = 1
        for i in range(8):
            if i != 0:
                if i % 2 == 1:
                    index += 8
                else:
                    index += 5
            self.fields[index].star = True

    def create_fields(self):
        # creating the list of fields, no care for stars aka. special spots
        # they are added later as an operation on a list
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        yellow = (255, 255, 0)
        white = (255, 255, 255)
        # column
        x = 6 * self.grid_side + self.margin
        y = self.side - self.margin - self.grid_side
        for i in range(6):
            if i == 1:
                self.fields.append(Field(self.win, red, x, y, self.grid_side))
            else:
                self.fields.append(Field(self.win, white, x, y, self.grid_side))
            y -= self.grid_side

        # row
        for i in range(6):
            x -= self.grid_side
            self.fields.append(Field(self.win, white, x, y, self.grid_side))

        # only one no to overlap, it would couse more fields than there rely are
        for i in range(1):
            y -= self.grid_side
            self.fields.append(Field(self.win, white, x, y, self.grid_side))
        y -= self.grid_side

        # row
        for i in range(6):
            if i == 1:
                self.fields.append(Field(self.win, green, x, y, self.grid_side))
            else:
                self.fields.append(Field(self.win, white, x, y, self.grid_side))
            x += self.grid_side

        # column
        for i in range(6):
            y -= self.grid_side
            self.fields.append(Field(self.win, white, x, y, self.grid_side))

        x += self.grid_side
        self.fields.append(Field(self.win, white, x, y, self.grid_side))
        x += self.grid_side

        # column
        for i in range(6):
            if i == 1:
                self.fields.append(Field(self.win, blue, x, y, self.grid_side))
            else:
                self.fields.append(Field(self.win, white, x, y, self.grid_side))
            y += self.grid_side

        # row
        for i in range(6):
            x += self.grid_side
            self.fields.append(Field(self.win, white, x, y, self.grid_side))

        y += self.grid_side
        self.fields.append(Field(self.win, white, x, y, self.grid_side))
        y += self.grid_side

        # row
        for i in range(6):
            if i == 1:
                self.fields.append(Field(self.win, yellow, x, y, self.grid_side))
            else:
                self.fields.append(Field(self.win, white, x, y, self.grid_side))
            x -= self.grid_side

        # column
        for i in range(6):
            y += self.grid_side
            self.fields.append(Field(self.win, white, x, y, self.grid_side))

        x -= self.grid_side
        self.fields.append(Field(self.win, white, x, y, self.grid_side))
        x -= self.grid_side

    def update(self, pawns):
        for field in self.fields:
            field.reset_pawns()

        for pawn in pawns:
            if pawn.position != -1:
                self.fields[pawn.position].pawns[pawn.color].append(pawn)

    def find_conflicts(self, chosen):
        # chosen is the moved pawn, consistent with chinczyk and agent
        potential_casualties = []
        conflict = False
        field = self.fields[chosen.position]
        defence = 0
        attack = 1
        if not field.star or chosen.finishing == 0:
            for pawns in field.pawns:
                for pawn in field.pawns[pawns]:
                    if pawn.team == chosen.team:
                        attack += 1
                    else:
                        defence += 1
                        potential_casualties.append(pawn)

        if defence <= attack and defence != 0:
            conflict = True
            for pawn in potential_casualties:
                pawn.reset()

        return conflict

    def draw(self):
        for field in self.fields:
            field.draw()


if __name__ == "__main__":
    WIN_SIDE = 610
    win = pygame.display.set_mode((WIN_SIDE, WIN_SIDE))
    MARGIN = 10
    color_numbers = {
        "r": 0,
        "g": 1,
        "b": 2,
        "y": 3
    }

    board = Path(win, WIN_SIDE, MARGIN)
    board.draw()
    time.sleep(10)