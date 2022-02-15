import os
import matplotlib.pyplot as plt
import neat

import main
import choosing_genomes
import botV1.main as v1


def compare_generations(directory):
    # getting files with checkpoints
    files = []
    for filename in os.scandir(directory):
        file = filename
        name = filename.path[9:]
        if name[:4] == "neat":
            generation = name[16:]
            files.append([filename, int(generation)])

    # sorting by generation
    files = sorted(files, key=lambda f: f[1])

    # getting win rates
    win_rates = []
    # creating constant random opponent
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    winner2, config2 = v1.run(config_path)
    for f in files:
        path = f[0]
        p = neat.Checkpointer.restore_checkpoint(path)
        config1 = p.config
        winner1 = p.run(choosing_genomes.main, 1)
        win_rate = main.match(winner1, config1, winner2, config2, 1000)
        win_rates.append(win_rate)
        print(f"win rate: {win_rate}, generation: {f[1]}")

    generations = [f[1] for f in files]
    sub_par = []
    for x, r in enumerate(win_rates):
        if r > 35:
            sub_par.append(generations[x])
    print(sub_par)
    plt.plot(generations, win_rates, 'ro')
    plt.axis([0, 500, 0, 100])
    plt.show()

if __name__ == "__main__":
    directory = os.path.join("..", "botv1")
    compare_generations(directory)
