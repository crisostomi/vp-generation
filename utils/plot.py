import matplotlib.pyplot as plt

def plot(system, species=[], limit=10):
    res = system.res
    t = res["time"]
    plt.figure(1)
    if len(species) == 0:
        species = system.get_model_species()

    for i, s in enumerate(species):
        plt.plot(t, res[s])
        if i == limit:
            break

    plt.grid(True)
    plt.legend(species)
    plt.grid(True)
    plt.show()