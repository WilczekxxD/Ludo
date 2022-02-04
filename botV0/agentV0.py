import pygame.display

import ludo.dice as dice
from ludo.pawn import Pawn


class Player:

    def __init__(self, color, team, starting, final):
        self.starting = starting
        self.pawns = [Pawn(color, team, i) for i in range(4)]
        self.color = color
        self.finished = False
        self.final = final
        self.team = team
        self.place_pawns()

    def place_pawns(self):
        for x, pawn in enumerate(self.pawns):
            self.starting.fields[x].pawns[self.color].append(pawn)

    def move(self, strikes, moves, chosen, candidates):
        chosen = chosen
        reward = 0
        if moves == 6:
            strikes += 1
        again = False

        if strikes != 3:
            if len(candidates) != 0:
                if chosen in candidates:
                    reward += 2
                else:
                    reward -= 2
                    chosen = candidates[0]
                chosen.move(moves)

            if chosen and (moves == 6 or chosen.finished):
                again = True

            if chosen and chosen.finished:
                strikes = 0

        return strikes, again, chosen, reward

    def update(self):
        self.starting.reset()
        self.final.reset()
        for pawn in self.pawns:
            if pawn.position == -1:
                self.starting.fields[pawn.index].pawns[pawn.color].append(pawn)
            if pawn.finishing:
                self.final.fields[pawn.position].pawns[pawn.color].append(pawn)


if __name__ == "__main__":
    pass
