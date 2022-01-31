
color_numbers = {
    (255, 0, 0): 0,
    (0, 255, 0): 1,
    (0, 0, 255): 2,
    (255, 255, 0): 3,
}


class Pawn:

    def __init__(self, color, team, index):
        self.position = -1
        self.color = color
        self.team = team
        self.possible = False
        self.finishing = 0
        self.finished = False
        self.index = index

    def movable(self, moves):
        self.possible = False
        if self.position != -1 and not self.finished:
            if not self.finishing or (self.finishing and (self.position+moves) <= 5):
                self.possible = True

    def move(self, moves):
        if self.possible:
            for _ in range(moves):
                if self.position == (13 * ((color_numbers[self.color]+3) % 4 + 1))-1 and not self.finishing:
                    self.finishing = 1
                    self.position = 0
                else:
                    self.position = (self.position + 1) % 52

        elif self.position == -1:
            self.position = 1 + color_numbers[self.color] * 13

        if self.finishing and self.position == 5:
            self.finished = True

    def reset(self):
        self.position = -1
        self.possible = False


if __name__ == "__main__":
    pass
