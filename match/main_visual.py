import neat.nn
from match.choosing_genomes import run
import time
from ludo.indicator import Indicator
import ludo.dice as dice
from botV1.boardV1 import Board
from botV1.agentV1 import Player
from ludo.pawn import Pawn
import numpy as np
import neat
import os
import pygame

clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
frame_rate = 30


def main(nets, matches):

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    teams = [0, 1, 2, 3]
    win_side = 610
    win = pygame.display.set_mode((win_side, win_side))
    margin = 5

    points = [0, 0, 0, 0]
    for m in range(matches):
        # one round of a tournament,
        # points for who wins
        # making one set of nets play eachother multiple times so as to decrease luck factor
        # creating board
        board = Board(win, win_side, margin)
        # creating players
        players = [Player(colors[i], teams[i], board.starts[i], board.finish_lines[i]) for i in range(4)]
        i = 0
        end = False
        while not end:

            playing = players[i]
            strikes = 0
            again = True
            # this is used to make multiple moves of one player possible
            while again:
                # pygame stuff
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                board.draw()
                pygame.display.update()
                clock.tick(frame_rate)

                # adding ability to pouse the game under p
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_p]:
                    time.sleep(30)

                again = False
                moves = dice.throw()
                print(i, strikes, moves)
                # playing player moving
                # activating net of x + indx of player from ge
                # activating by position of every pawn
                candidates = []
                chosen = False
                for pawn in playing.pawns:
                    pawn.movable(moves)
                    if pawn.possible or (pawn.position == -1 and moves == 6):
                        candidates.append(pawn)

                if len(candidates) > 0:
                    if len(candidates) == 1:
                        chosen = candidates[0]
                        chosen.move(moves)

                    elif len(candidates) > 1:
                        states = []
                        # this is a loop which creates a set of dummy states
                        for candidate in candidates:
                            # cooping strikes
                            c_strikes = strikes
                            # creating and moving a copy of a pawn not to disrupt the original game
                            chosen = Pawn(candidate.color, candidate.team, candidate.index)
                            chosen.position = int(candidate.position)
                            chosen.possible = True
                            chosen.move(moves)
                            # checking for conflicts
                            conflict, potential_casualties = board.path.find_conflictsV1(chosen)
                            # creating state
                            state = []
                            for k in range(16):
                                pawn = players[(i + k // 4) % 4].pawns[k % 4]
                                # if conflict and in potential casualties pawn should be teleported
                                # to the beggining
                                # but since we do not actually move pawns just inserting -1 into state
                                if conflict and pawn in potential_casualties:
                                    state.append(-1)
                                elif pawn.finishing == 1:
                                    state.append(pawn.position + 52)
                                # this pawn is the one moved in this scenario therefore value of the copy is
                                # different from this of the actual pawn
                                elif pawn in playing.pawns and pawn.index == chosen.index:
                                    state.append(chosen.position)
                                else:
                                    state.append(pawn.position)
                            print(f"state {state}")
                            # changing strikes if need be, but only a copy
                            if chosen and (chosen.finished or conflict):
                                c_strikes = 0

                            state = tuple(state + [c_strikes])
                            states.append(state)

                        # getting output from net for every state
                        outputs = [nets[i].activate(state) for state in states]
                        index = np.argmax(outputs)
                        print(f"outputs: {outputs}\nstates:{states}")

                        # choosing and moving the choice, this already has impact on the game
                        chosen = candidates[index]
                        chosen.move(moves)

                    # actual conflict resolution
                    if chosen.finished or board.path.find_conflicts(chosen):
                        again = True
                        strikes = 0

                    # moves pawns back into starting positions if they were taken out and updates finish lines
                    for player in players:
                        player.update()

                    # after moving and conflicts updating path since final and starting where updated before
                    on_board = []
                    for player in players:
                        for pawn in player.pawns:
                            if pawn.position != -1 and not pawn.finishing and not pawn.finished:
                                on_board.append(pawn)

                    board.path.update(on_board)

                    # checking if again previously handled but player.move but in this version
                    # it just does not make sense
                    if moves == 6:
                        strikes += 1
                        again = True

                status = [pawn.finished for pawn in playing.pawns]
                if all(status):
                    end = True
                    again = False
                    points[i] += 1

            # printing the board
            board.draw()
            pygame.display.update()
            i += 1
            i = i % 4

    winner_index = np.argmax(points)
    print(f"winner has index: {winner_index}\npoints are: {points}\n"
          f"winning percatage of the winner is: {((points[winner_index])/matches) * 100}\n"
          f"out of {matches}")


def match(g1, config1, g2, config2, matches):

    # creating players and their nets
    nets = []
    # creating net of the better player
    nets.append(neat.nn.FeedForwardNetwork.create(g1, config1))

    # creating the rest
    for _ in range(3):
        nets.append(neat.nn.FeedForwardNetwork.create(g2, config2))

    main(nets, matches)


if __name__ == "__main__":
    g1, config1, g2, config2 = run()
    match(g1, config1, g2, config2, 100)
