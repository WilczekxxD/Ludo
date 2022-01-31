import pygame.display

from plansza import Final
import dice
from pawn import Pawn


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

    def move(self, strikes):
        # moves = dice.throw()
        moves = int(input("how far do you wanna move: "))
        print(f"dice: {moves}")
        if moves == 6:
            strikes += 1
        again = False
        candidates = []
        chosen = False

        if strikes != 3:
            for pawn in self.pawns:
                pawn.movable(moves)
                if pawn.possible or (pawn.position == -1 and moves == 6):
                    candidates.append(pawn)

            if len(candidates) == 1:
                chosen = candidates[0]
                chosen.move(moves)

            elif len(candidates) != 0:
                print([candidate.index for candidate in candidates], self.color)
                chosen = candidates[int(input("give the index of your choice: "))]

                chosen.move(moves)

            if chosen and (moves == 6 or chosen.finished):
                again = True

            if chosen and chosen.finished:
                strikes = 0

        return strikes, again, chosen

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
