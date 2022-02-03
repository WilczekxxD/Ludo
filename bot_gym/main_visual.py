import time
from ludo.indicator import Indicator
import pygame
from ludo.board import Board
from botV0.agentV0 import Player
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
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

    board = Board(win, win_side, margin)

    players = [Player(colors[i], teams[i], board.starts[i], board.finish_lines[i]) for i in range(4)]

    # it loooks dumb and is but i wanted to make it in one for, for the sake of it
    # ended up changing colors so as they mach
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
            # playing player moving
            strikes, again, chosen = playing.move(strikes, players)

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


if __name__ == "__main__":
    main()