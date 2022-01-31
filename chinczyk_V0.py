from plansza import Board, Final
from agent import Agent
import os
import neat

color_numbers = {
    "r": 0,
    "g": 1,
    "b": 2,
    "y": 3
}


def main(genomes, config):
    playing_bu = []
    data = [["r", 0], ["g", 1], ["y", 0], ["b", 1]]

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        playing_bu.append(Agent(data[0], data[1], g, net))
    print(len(playing_bu))

    for _ in range(10):
        playing = playing_bu
        board = Board()

        finished = []

        end = False
        i = -1
        while not end:
            i = (i+1) % len(playing)
            print(f"move of {playing[i].color}")
            strikes = 0
            again = True
            while again:
                strikes, again, chosen = playing[i].move(strikes, pawns=[player.pawns for player in playing])

                # conflicts
                if chosen and (chosen.finished or board.find_conflicts(chosen)):
                    again = True
                    strikes = 0
                    for player in playing:
                        player.update()

                # after moving and conflicts updating pawns and board and final ways
                on_board = []
                finishing = []
                waiting = []
                for player in playing:
                    for pawn in player.pawns:
                        if pawn.finishing or pawn.finished:
                            finishing.append(pawn)
                        elif pawn.position == -1:
                            waiting.append(1)
                        elif pawn.position != -1:
                            on_board.append(pawn)
                    player.final.update(finishing)
                    player.waiting = waiting
                    waiting = []
                    finishing = []
                board.update(on_board)

                # checking if someone won
                for x, player in enumerate(playing):
                    status = [pawn.finished for pawn in player.pawns]
                    if all(status):
                        finished.append(player)
                        playing = playing[:x] + playing[x+1:]

                # ending the game
                if len(finished) >= 2:
                    team_list = [player.team for player in playing]
                    if finished[0].team != any(team_list) or finished[1].team != any(team_list):
                        end = True

                # printing the board
                board.show()
                for player in playing:
                    player.final.show()

        for x, player in enumerate(finished):
            player.g.fitness += 100 - (x*20)


def run(config_path):
    # those match the topic in configuration file, those names down there,
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # showing stats instead of black running screan

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter
    p.add_reporter(stats)

    winner = p.run(main, 200)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT_config.txt")
    run(config_path)