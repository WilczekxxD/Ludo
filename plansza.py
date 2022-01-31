from colorama import Fore, init
init(autoreset=True)

color_numbers = {
    "r": 0,
    "g": 1,
    "b": 2,
    "y": 3
}


class Field:

    # not sure if lists instead of dictionaries wouldn't be better

    def __init__(self):
        self.star = False
        self.pawns = {"r": [],
                      "g": [],
                      "y": [],
                      "b": [], }

    def reset_pawns(self):
        self.pawns = {"r": [],
                      "g": [],
                      "y": [],
                      "b": [], }


class Board:

    def __init__(self):
        self.fields = list([Field() for _ in range(52)])

        # marking stars
        index = 1
        for i in range(8):
            if i != 0:
                if i % 2 == 1:
                    index += 8
                else:
                    index += 5
            self.fields[index].star = True

    def update(self, pawns):
        for field in self.fields:
            field.reset_pawns()

        for pawn in pawns:
            if pawn.position != -1:
                self.fields[pawn.position].pawns[pawn.color].append(pawn)

    def find_conflicts(self, chosen):
        # chosen is the moved pawn, consistent with chinczyk and agent
        potential_casualties = []
        conflict = False
        field = self.fields[chosen.position]
        defence = 0
        attack = 1
        if not field.star:
            for pawns in field.pawns:
                for pawn in field.pawns[pawns]:
                    if pawn.team == chosen.team:
                        attack += 1
                    else:
                        defence += 1
                        potential_casualties.append(pawn)

        if defence <= attack and defence != 0:
            conflict = True
            for pawn in potential_casualties:
                pawn.reset()

        return conflict

    def show(self):
        for x, field in enumerate(self.fields):
            start = -1
            finish = -1
            if x % 13 == 1:
                start = x//13
            elif (x+1) % 13 == 0:
                finish = (x+1)//13-1

            print("[", end='')

            if start >= 0:
                if start == 0:
                    print(f"{Fore.RED}S", end='')
                elif start == 1:
                    print(f"{Fore.GREEN}S", end='')
                elif start == 2:
                    print(f"{Fore.YELLOW}S", end='')
                elif start == 3:
                    print(f"{Fore.BLUE}S", end='')

            elif finish >= 0:
                if finish == 0:
                    print(f"{Fore.GREEN}F", end='')
                if finish == 1:
                    print(f"{Fore.YELLOW}F", end='')
                if finish == 2:
                    print(f"{Fore.BLUE}F", end='')
                if finish == 3:
                    print(f"{Fore.RED}F", end='')

            if field.star:
                print("*", end='')

            for key in field.pawns:
                for _ in field.pawns[key]:
                    if key == "r":
                        print(f"{Fore.RED}P", end='')
                    elif key == "g":
                        print(f"{Fore.GREEN}P", end='')
                    elif key == "y":
                        print(f"{Fore.YELLOW}P", end='')
                    elif key == "b":
                        print(f"{Fore.BLUE}P", end='')
            print("]", end='')
        print()


class Final:

    def __init__(self, color):
        self.fields = list([0 for _ in range(6)])
        self.color = color

    def update(self, pawns):
        self.fields = list([0 for _ in range(6)])
        for pawn in pawns:
            self.fields[pawn.position] += 1

    def show(self):

        for number in self.fields:
            print("[", end='')
            for _ in range(number):
                if self.color == "r":
                    print(f"{Fore.RED}P", end='')
                elif self.color == "g":
                    print(f"{Fore.GREEN}P", end='')
                elif self.color == "y":
                    print(f"{Fore.YELLOW}P", end='')
                elif self.color == "b":
                    print(f"{Fore.BLUE}P", end='')
            print("] ", end='')
        print()


if __name__ == "__main__":
    Final("r").show()