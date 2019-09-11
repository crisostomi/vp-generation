from system import System
from parameter_space import ParameterSpace
from utils.handle_xml import *
import algorithm
import getpass
import utils.utils

epsilon = 10**(-3)
delta = 0.1

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "small-sumoylation"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
MODEL_FOLDER = TEST_FOLDER + "/out"
XML_PATH = MODEL_FOLDER + "/parameters.xml"
ABUNDANCES_PATH = MODEL_FOLDER + "/constraints.xml"

STOP_TIME_PARAMETER = "parameters.simulation_time"
STOP_TIME = 200

SIMULATION_TIME = "parameters.simulation_time"
ADM_PARAM_FILE = MODEL_FOLDER+"/admissible_param.txt"
PARAM_FILE = MODEL_FOLDER + "/virtual_patients.txt"

def main():
    system = System(MODEL_FOLDER)
    param_bounds = parse_parameters_bounds_xml(XML_PATH)
    parameter_space = ParameterSpace(param_bounds, discretization_step=3, epsilon_above_zero=10**(-10))
    abundances = parse_abundance_xml(ABUNDANCES_PATH)
    system.set_parameter(STOP_TIME_PARAMETER, STOP_TIME)
    system.set_abundances(abundances)
    # print algorithm.bootstrap(system, parameter_space, STOP_TIME)
    adm_parameters = utils.utils.get_parameter_from_file(ADM_PARAM_FILE)
    vps = algorithm.get_virtual_patients(system, parameter_space, adm_parameters, epsilon, delta, verbose=1)
    utils.utils.save_parameters_to_file(PARAM_FILE, parameter_space, vps)


if __name__ == '__main__':
    main()