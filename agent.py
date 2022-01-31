from plansza import Final
import kostka
import pawn
import neat

color_numbers = {
    "r": 0,
    "g": 1,
    "b": 2,
    "y": 3
}


class Agent:

    def __init__(self, color, team, g, net):
        self.waiting = [1, 1, 1, 1]
        self.pawns = [pawn.Pawn(color, team, i) for i in range(4)]
        self.color = color
        self.finished = False
        self.final = Final(color)
        self.g = g
        self.net = net
        self.team = team

    def move(self, strikes, pawns):
        moves = kostka.throw()
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
                # print(candidates.index)
                # chosen = candidates[int(input("give the index of your choice: "))]
                # shortening pawns:
                short_pawns = []
                for pawn in pawns:
                    if pawn.color != self.color:
                        short_pawns.append(pawn)
                pawns = short_pawns
                # i do not know if giving the team once for every set of pawns instead of before every pawn
                # wouldn't be better

                output = self.net.activate((moves, self.team,
                                           self.pawns[0].team, self.pawns[0].position, self.pawns[0].finishing,
                                           self.pawns[1].team, self.pawns[1].position, self.pawns[1].finishing,
                                           self.pawns[2].team, self.pawns[2].position, self.pawns[2].finishing,
                                           self.pawns[3].team, self.pawns[3].position, self.pawns[3].finishing,
                                           pawns[0].team, pawns[0].position, pawns[0].finishing,
                                           pawns[1].team, pawns[1].position, pawns[1].finishing,
                                           pawns[2].team, pawns[2].position, pawns[2].finishing,
                                           pawns[3].team, pawns[3].position, pawns[3].finishing,
                                           pawns[4].team, pawns[4].position, pawns[4].finishing,
                                           pawns[5].team, pawns[5].position, pawns[5].finishing,
                                           pawns[6].team, pawns[6].position, pawns[6].finishing,
                                           pawns[7].team, pawns[7].position, pawns[7].finishing,
                                           pawns[8].team, pawns[8].position, pawns[8].finishing,
                                           pawns[9].team, pawns[9].position, pawns[9].finishing,
                                           pawns[10].team, pawns[10].position, pawns[10].finishing,
                                           pawns[11].team, pawns[11].position, pawns[11].finishing,
                                            ))
                biggest_value = 0
                chosen = 0
                for x, value in enumerate(output):
                    if x == 0:
                        biggest_value = value
                    elif value > biggest_value:
                        biggest_value = value
                        chosen = x

                chosen = self.pawns[chosen]

                if chosen in candidates:
                    self.g.fitness += 1
                else:
                    self.g.fitness -= 1
                    chosen = candidates[0]

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
