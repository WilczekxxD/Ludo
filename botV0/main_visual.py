import time
from ludo.indicator import Indicator
import pygame
import ludo.dice as dice
from ludo.board import Board
from ludo.player import Player
import numpy as np
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

frame_rate = 30


def main():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    teams = [0, 1, 2, 3]
    win_side = 610
    win = pygame.display.set_mode((win_side, win_side))
    margin = 5

    nets = []
    ge = []

    for _, g in genomes:
        # setting up genomes, connecting them and appending to the genome list named ge

        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    for x in range(int(len(ge))/4):
        # one round of a tournament,
        # not checking if ge devidible by 4 so population should be a power of 4
        for game in range(4):
            # making one set of genomes play eachother multiple times so as to decrease luck factor
            # creating board
            board = Board(win, win_side, margin)
            # creating players
            players = [Player(colors[i], teams[i], board.starts[i], board.finish_lines[i]) for i in range(4)]

            # creating indicators
            r = (win_side-2*margin)/30
            indicators = []
            indicators.append(Indicator(win, colors[0], r, (win_side - 2 * margin - r), r))
            indicators.append(Indicator(win, colors[1], r, r, r))
            indicators.append(Indicator(win, colors[2], (win_side - 2 * margin - r), r, r))
            indicators.append(Indicator(win, colors[3], (win_side - 2 * margin - r), (win_side - 2 * margin - r), r))

            i = 0
            end = False
            while not end:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                playing = players[i]
                strikes = 0
                again = True
                # this is used to make multiple moves of one player possible
                while again:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    board.draw()
                    indicators[i].on()
                    pygame.display.update()

                    clock.tick(frame_rate)
                    print(f"move of player {playing.team} on strike {strikes}")
                    moves = dice.throw()
                    print(f"moves {moves}")
                    # playing player moving
                    # activating net of x + indx of player from ge
                    # activating by position of every pawn

                    output = nets[x + i].activate(moves, playing.pawns[0].position, playing.pawns[1].position,
                                                  playing.pawns[2].position, playing.pawns[3].position,

                                                  players[(i + 1) % 4].pawns[0].position,
                                                  players[(i + 1) % 4].pawns[1].position,
                                                  players[(i + 1) % 4].pawns[2].position,
                                                  players[(i + 1) % 4].pawns[3].position,

                                                  players[(i + 2) % 4].pawns[0].position,
                                                  players[(i + 2) % 4].pawns[1].position,
                                                  players[(i + 2) % 4].pawns[2].position,
                                                  players[(i + 2) % 4].pawns[3].position,

                                                  players[(i + 3) % 4].pawns[0].position,
                                                  players[(i + 3) % 4].pawns[1].position,
                                                  players[(i + 3) % 4].pawns[2].position,
                                                  players[(i + 3) % 4].pawns[3].position,
                                                  )
                    chosen = playing.pawns[np.argmax(output)]
                    strikes, again = playing.move(strikes)

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

                    # printing the board
                    board.draw()
                    indicators[i].off()
                    pygame.display.update()
                    time.sleep(1)
                i += 1
                i = i % 4


def run(config_path):
    # those match the topic in configuration file, those names down there,
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # showing stats instead of black running screan

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 200)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "ConfigV0.txt")
    run(config_path)
