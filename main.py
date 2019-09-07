from system import System
from parameter_space import ParameterSpace
from utils.handle_xml import *
import algorithm
import getpass
import utils.utils

epsilon = 10**(-3)
delta = 0.05

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "lgi-adam"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
MODEL_FOLDER = TEST_FOLDER + "/out"
XML_PATH = MODEL_FOLDER + "/parameters.xml"
ABUNDANCES_PATH = MODEL_FOLDER + "/constraints.xml"

STOP_TIME_PARAMETER = "parameters.simulation_time"
STOP_TIME = 20

SIMULATION_TIME = "parameters.simulation_time"
ADM_PARAM_FILE = MODEL_FOLDER+"/adm_param.txt"


def main():
    system = System(MODEL_FOLDER)
    param_bounds = parse_parameters_bounds_xml(XML_PATH)
    parameter_space = ParameterSpace(param_bounds, discretization_step=5)
    abundances = parse_abundance_xml(ABUNDANCES_PATH)
    system.set_parameter(STOP_TIME_PARAMETER, STOP_TIME)
    system.set_abundances(abundances)
    # print algorithm.bootstrap(system, parameter_space)
    adm_parameters = utils.utils.get_parameter_from_file(ADM_PARAM_FILE)
    print algorithm.getVirtualPatients(system, parameter_space, adm_parameters, epsilon, delta, verbose=False)


if __name__ == '__main__':
    main()