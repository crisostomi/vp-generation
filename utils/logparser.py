import matplotlib.pyplot as plt
import getpass
import matplotlib
import matplotlib.ticker as plticker
import numpy as np

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "dna-sumoylation"
OUT_FOLDER = PROJECT_FOLDER+"/"+TEST+"/search/"
LOG_FILE = OUT_FOLDER+"time_series_5.txt"
PROT_A,PROT_A_NAME = "compartment_7660.species_212181_conc", "DNMT3A"
PROT_B,PROT_B_NAME = "compartment_7660.species_212316_conc", "DNMT3B"
PROT_C,PROT_C_NAME = "compartment_7660.species_912481_conc", "UBE2I"
PROT_D,PROT_D_NAME = "compartment_7660.species_212287_conc", "DNMT1"
ABUND_A = 1.1139709952396766E-8
ABUND_B = 6.531052806376618E-10
ABUND_C = 1.425882873906786E-7
ABUND_D = 1.0566810583416363E-8
MIN_A, MAX_A, MIN_ZOOM_A, MAX_ZOOM_A = 0.85e-8, 1.35e-8, 1.2e-8, 1.32e-8
MIN_B, MAX_B = 5e-10, 8e-10
MIN_C, MAX_C = 0, 2e-7
MIN_D, MAX_D = 0, 2e-7


def get_epsilon(N, delta):
    return 1 - np.power(delta, 1./N)


# returns map['proteina']['t'] = [conc_vp_0, ... , conc_vp_n]

def get_timeseries_from_log(file):
    map = dict()
    with open(file, "r") as f:
        content = f.read()
        VPs = str(content).split("VP")
        VPs.pop(0)
        for vp in VPs:
            vp_stripped = vp.replace('\n', '')
            species_list = vp_stripped.split('#')
            species_list.pop(0)
            for species in species_list:
                species_name = species.split(':')[0]
                species_timeSeries = species.split(':')[1]
                species_timeSeries_list = eval(species_timeSeries.replace(' ', ','))
                for t in range(len(species_timeSeries_list)):
                    map.setdefault((species_name, t), []).append(species_timeSeries_list[t])
    return map


# returns map['proteina']['VP'] = [conc_t_0, ... , conc_t_n]
def get_timeseries_to_plot(file):
    map = dict()
    with open(file, "r") as f:
        content = f.read()
        VPs = str(content).split("VP")
        VPs.pop(0)
        for i,vp in enumerate(VPs):
            vp_stripped = vp.replace('\n', '')
            species_list = vp_stripped.split('#')
            species_list.pop(0)
            for species in species_list:
                species_name = species.split(':')[0]
                species_timeSeries_list = eval(species.split(':')[1])
                # map.setdefault((species_name, i), []).append(species_timeSeries_list)
                map[(species_name, i)] = species_timeSeries_list
    return map


def get_protein_map(protein_name, map):
    map_prot = dict()
    for prot, t in map.keys():
        if prot == protein_name:
            map_prot[t] = map[(prot, t)]
    return map_prot

def plot_vps(map_prot, time, ymin, ymax, abundance, prot_name):
    V = range(len(map_prot.keys())) # num of VPS
    fig, ax = plt.subplots()
    for vp in sorted(map_prot.keys()):                  # for list of vp_list_of_concs in y
        vp_time_series = map_prot[vp]
        t = [ tup[0] for tup in vp_time_series ]
        conc = [ tup[1] for tup in vp_time_series ]
        # distr = np.linspace(0, time, num=T)
        ax.plot(t, conc, color='#1f77b4', alpha=0.5)# marker='o',edgecolors='b', s=10
    ax.grid(alpha=0.5)
    # plt.ylim(ymin=ymin, ymax=ymax)

    plt.xlabel("hours")
    plt.ylabel("mol/L")
    ax.set_title("concentration of species "+prot_name)

    formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: int(ms/3600))
    ax.xaxis.set_major_formatter(formatter)

    T = range(int(time))
    abundance_points = [abundance for i in T]
    ax.plot(abundance_points, linestyle='dashed', color="black", alpha=0.5, label="abundance")
    # upper_bound = abundance + (abundance * 0.2)

    # upper_line = [upper_bound for i in T]
    # ax.plot(upper_line, linestyle='dashed', color="red", alpha=0.5, label="error tolerance")
    # lower_bound = abundance - (abundance * 0.2)
    # lower_line = [lower_bound for i in T]
    # ax.plot(lower_line, linestyle='dashed', color="red", alpha=0.5)
    # plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    # map = get_timeseries_from_log(LOG_FILE)
    map = get_timeseries_to_plot(LOG_FILE)
    prot = dict()
    prot['A'] = [PROT_A, MIN_A, MAX_A, ABUND_A, PROT_A_NAME]
    prot['B'] = [PROT_B, MIN_B, MAX_B, ABUND_B, PROT_B_NAME]
    prot['C'] = [PROT_C, MIN_C , MAX_C, ABUND_C, PROT_C_NAME]
    prot['D'] = [PROT_D, MIN_D , MAX_D, ABUND_D, PROT_D_NAME]
    for letter in ['A','B','C','D']:
        prot_attrs = prot[letter]
        prot_name = prot_attrs[0]
        prot_min = prot_attrs[1]
        prot_max = prot_attrs[2]
        prot_abund = prot_attrs[3]
        prot_bio_name = prot_attrs[4]
        prot_map = get_protein_map(prot_name, map)
        plot_vps(prot_map, 1e5, prot_min, prot_max, prot_abund, prot_bio_name)


