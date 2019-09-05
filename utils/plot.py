import matplotlib.pyplot as plt

def plot(model, simulation_result, species=[], limit=10):
    res = simulation_result
    t = res["time"]
    plt.figure(1)
    if len(species) == 0:
        species = model.get_model_species()

    for i, s in enumerate(species):
        plt.plot(t, res[s])
        if i == limit:
            break

    plt.grid(True)
    plt.legend(species)
    plt.grid(True)
    plt.show()