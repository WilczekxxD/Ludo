import time
from ludo.indicator import Indicator
import ludo.dice as dice
from ludo.board import Board
from agentV0 import Player
import numpy as np
import neat
import os


def main(genomes, config):

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    teams = [0, 1, 2, 3]
    win_side = 610
    win = 0
    margin = 5

    nets = []
    ge = []
    for id, g in genomes:
        # setting up genomes, connecting them and appending to the genome list named ge

        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    while not len(ge) < 4:
        advancing_ge = []
        advancing_nets = []

        for j in range(int(len(ge)/4)):
            x = 0 + 4 * j
            # one round of a tournament,
            # not checking if ge devisible by 4 so population should be a power of 4
            # points for following who wins and goes on
            points = [0, 0, 0, 0]
            for game in range(4):
                # making one set of genomes play eachother multiple times so as to decrease luck factor
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
                        again = False
                        moves = dice.throw()
                        # playing player moving
                        # activating net of x + indx of player from ge
                        # activating by position of every pawn
                        candidates = []
                        chosen = False
                        for pawn in playing.pawns:
                            pawn.movable(moves)
                            if pawn.possible or (pawn.position == -1 and moves == 6):
                                candidates.append(pawn)
                        if len(candidates) > 1:
                            state = []
                            for k in range(16):
                                pawn = players[(i + k//4) % 4].pawns[k % 4]
                                if pawn.finishing != 0:
                                    state.append(pawn.position + 52)
                                else:
                                    state.append(pawn.position)
                            state = tuple([moves] + state)
                            output = nets[x + i].activate(state)
                            chosen = playing.pawns[np.argmax(output)]
                            strikes, again, chosen, reward = playing.move(strikes, moves, chosen, candidates)

                            # adding rewards for quality of moves, ex. where they legal
                            ge[x+i].fitness += reward
                        elif len(candidates) == 1:
                            chosen = candidates[0]
                            chosen.move(moves)

                        # conflicts
                        if chosen and (chosen.finished or board.path.find_conflicts(chosen)):
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
                        # checking if someone won and ending the game
                        status = [pawn.finished for pawn in playing.pawns]
                        if all(status):
                            end = True
                            again = False
                            points[i] += 1

                    i += 1
                    i = i % 4

            winner = np.argmax(points)
            advancing_ge.append(ge[winner])
            advancing_nets.append(nets[winner])

        for g in advancing_ge:
            g.fitness += 20
        ge = advancing_ge
        nets = advancing_nets


def run(config_path):
    # those match the topic in configuration file, those names down there,
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # showing stats instead of black running screan

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(500))

    winner = p.run(main)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'configV0.txt')
    run(config_path)
