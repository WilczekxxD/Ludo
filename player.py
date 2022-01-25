from plansza import Final
import dice
import pawn


class Player:

    def __init__(self, color, team):
        self.waiting = [1, 1, 1, 1]
        self.pawns = [pawn.Pawn(color, team, i) for i in range(4)]
        self.color = color
        self.finished = False
        self.final = Final(color)
        self.team = team

    def move(self, strikes, pawns):
        moves = dice.throw()
        # moves = int(input("how far do you wanna move: "))
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
                print(candidates.index)
                chosen = candidates[int(input("give the index of your choice: "))]
                # shortening pawns:
                short_pawns = []
                for pawn in pawns:
                    if pawn.color != self.color:
                        short_pawns.append(pawn)
                pawns = short_pawns

                chosen.move(moves)

            if chosen and (moves == 6 or chosen.finished):
                again = True

            if chosen and chosen.finished:
                strikes = 0

        return strikes, again, chosen

    def update(self):
        self.waiting = []
        for i in range(4):
            try:
                if self.pawns[i].position == -1:
                    self.waiting.append(1)
            except IndexError:
                self.waiting.append(0)


if __name__ == "__main__":
    pass
