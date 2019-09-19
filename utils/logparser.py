import matplotlib.pyplot as plt
import getpass
import matplotlib
import matplotlib.ticker as plticker
import numpy as np
import re

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "dna-sumoylation"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
SEARCH_FOLDER = TEST_FOLDER + "/search"
OUT_FOLDER = TEST_FOLDER + "/out"
TIME_SERIES_FILE = SEARCH_FOLDER + "/" + "time_series_5.txt"
VP_COLOR = '#1f77b4'
ABUNDANCE_COLOR = "black"


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
                map[(species_name, i)] = species_timeSeries_list
    return map


def get_protein_map(protein_name, map):
    map_prot = dict()
    for prot, t in map.keys():
        if prot == protein_name:
            map_prot[t] = map[(prot, t)]
    return map_prot


def plot_vps(map_prot, time, ymin, ymax, abundance, prot_name):
    map_prot = get_protein_map(prot_name, map_prot)
    abundance = abundance[prot_name]
    V = range(len(map_prot.keys())) # num of VPS
    fig, ax = plt.subplots()
    for vp in sorted(map_prot.keys()):                  # for list of vp_list_of_concs in y
        vp_time_series = map_prot[vp]
        t = [ tup[0] for tup in vp_time_series ]
        conc = [ tup[1] for tup in vp_time_series ]
        ax.plot(t, conc, color=VP_COLOR, alpha=0.5)

    ax.grid(alpha=0.5)
    # plt.ylim(ymin=ymin, ymax=ymax)

    plt.xlabel("hours")
    plt.ylabel("mol/L")
    ax.set_title("concentration of "+get_species_name(prot_name))

    formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: int(ms/3600))
    ax.xaxis.set_major_formatter(formatter)

    T = range(int(time))
    abundance_points = [abundance for _ in T]
    ax.plot(abundance_points, linestyle='dashed', color=ABUNDANCE_COLOR, alpha=1, label="abundance")
    # upper_bound = abundance + (abundance * 0.2)

    # upper_line = [upper_bound for i in T]
    # ax.plot(upper_line, linestyle='dashed', color="red", alpha=0.5, label="error tolerance")
    # lower_bound = abundance - (abundance * 0.2)
    # lower_line = [lower_bound for i in T]
    # ax.plot(lower_line, linestyle='dashed', color="red", alpha=0.5)
    # plt.legend(loc='best')
    plt.show()


def get_abundances(map_prot):
    abundances = dict()
    with open(OUT_FOLDER + "/Monitor.mo", "r") as f:
        abundances_file_content = f.read()

    proteins = {prot for prot, vp in map_prot.keys()}
    for prot in proteins:
        for line in abundances_file_content.splitlines():
            prot_name = prot.split(".")[1] + "_abundance"
            if prot_name in line:
                abundance = float(line.split("=")[1].strip(" ;"))
                abundances[prot] = abundance
                break

    return abundances


def get_species_name(species_name):
    regex = "\w+\.(species\_[0-9]+)\_\w+"
    m = re.match(regex, species_name)
    return m.group(1)


if __name__ == '__main__':
    # map = get_timeseries_from_log(LOG_FILE)
    map = get_timeseries_to_plot(TIME_SERIES_FILE)
    # prot = dict()
    # prot['A'] = [PROT_A, MIN_A, MAX_A, ABUND_A, PROT_A_NAME]
    # prot['B'] = [PROT_B, MIN_B, MAX_B, ABUND_B, PROT_B_NAME]
    # prot['C'] = [PROT_C, MIN_C , MAX_C, ABUND_C, PROT_C_NAME]
    # prot['D'] = [PROT_D, MIN_D , MAX_D, ABUND_D, PROT_D_NAME]
    # for letter in ['A','B','C','D']:
    #     prot_attrs = prot[letter]
    #     prot_name = prot_attrs[0]
    #     prot_min = prot_attrs[1]
    #     prot_max = prot_attrs[2]
    #     prot_abund = prot_attrs[3]
    #     prot_bio_name = prot_attrs[4]
    #     prot_map = get_protein_map(prot_name, map)
    #     plot_vps(prot_map, 1e5, prot_min, prot_max, prot_abund, prot_bio_name)
    abundances = get_abundances(map)

    for protein in abundances.keys():
        print "Plotting %s..." % protein
        plot_vps(map, 1e5, None, None, abundances, protein)



