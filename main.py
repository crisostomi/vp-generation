from system import System
from parameter_space import ParameterSpace
from utils.handle_xml import *
import algorithm
import getpass

epsilon = 10**3
delta = 0.05

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "signal-regulatory"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
MODEL_FOLDER = TEST_FOLDER + "/out"
XML_PATH = MODEL_FOLDER + "/parameters.xml"
ABUNDANCES_PATH = MODEL_FOLDER + "/constraints.xml"

SIMULATION_TIME = "parameters.simulation_time"


def main():
    system = System(MODEL_FOLDER)
    param_bounds = parse_parameters_bounds_xml(XML_PATH)
    parameter_space = ParameterSpace(param_bounds, discretization_step=50)
    abundances = parse_abundance_xml(ABUNDANCES_PATH)
    system.set_parameter(SIMULATION_TIME, 200)
    system.set_abundances(abundances)
    print algorithm.bootstrap(system, parameter_space)


if __name__ == '__main__':
    main()