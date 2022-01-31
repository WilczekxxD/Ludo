import pygame
pygame.font.init()


class Field:

    # not sure if lists instead of dictionaries wouldn't be better

    def __init__(self, win, color, x, y, side):
        self.star = False
        self.color = color
        self.side = side
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.x = x
        self.y = y
        self.win = win
        self.pawns = {(255, 0, 0): [],
                      (0, 255, 0): [],
                      (0, 0, 255): [],
                      (255, 255, 0): [], }

    def reset_pawns(self):
        self.pawns = {(255, 0, 0): [],
                      (0, 255, 0): [],
                      (0, 0, 255): [],
                      (255, 255, 0): [], }

    def draw(self):

        # grey border
        pygame.draw.rect(self.win, (100, 100, 100), [self.x, self.y, self.side, self.side], 1)
        # field
        pygame.draw.rect(self.win, self.color, [self.x + 1, self.y + 1, self.side - 1, self.side - 1])
        # marking protected fields, making a polygon between middles of sides
        # self.color//2 to make it darker, just visuals
        if self.star:
            pygame.draw.polygon(self.win, (self.color[0]//2, self.color[1]//2, self.color[2]//2),
                                [(self.x + self.side/2, self.y),
                                 (self.x + self.side/2, self.y + self.side),
                                 (self.x, self.y + self.side/2),
                                 (self.x + self.side, self.y + self.side/2)])

        # drawing pawns as circles, with numbers

        for key in self.pawns:
            for i in range(len(self.pawns[key])):
                x = self.x + (i % 2) * self.side//2 + self.side//4
                y = self.y + + (i // 2) * self.side//2 + self.side//4
                pygame.draw.circle(self.win, (100, 100, 100), (int(x), int(y)), int((self.side//4) - 1), 6)
                pygame.draw.circle(self.win, key, (int(x), int(y)), int((self.side // 4) - 5))


if __name__ == "__main__":
    WIN_SIDE = 610
    MARGIN = 5
    win = pygame.display.set_mode((WIN_SIDE, WIN_SIDE))
    GRID_SIDE = (WIN_SIDE-MARGIN*2)/15

    color_numbers = {
        "r": 0,
        "g": 1,
        "b": 2,
        "y": 3
    }
