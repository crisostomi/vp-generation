from system import System
from parameter_space import ParameterSpace
from utils.handle_xml import *
import algorithm
import getpass
import utils.utils
from logger import Logger
from utils.plot import plot

epsilon = 10**(-3)
delta = 10**(-3)

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "dna-sumoylation"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
MODEL_FOLDER = TEST_FOLDER + "/out"
SEARCH_FOLDER = TEST_FOLDER+"/search"
XML_PATH = MODEL_FOLDER + "/parameters.xml"
CONSTRAINTS_PATH = MODEL_FOLDER + "/constraints.xml"

STOP_TIME = 1e5
PROT_DISCR_STEP = 10
NON_PROT_DISCR_STEP = 3
SMALLEST_VALUE = 1e-15
POWER_LAW_EXP = 1.5

SIMULATION_TIME = "parameters.simulation_time"
ADM_PARAM_FILE = SEARCH_FOLDER+"/admissible_param.txt"
PARAM_FILE = SEARCH_FOLDER + "/virtual_patients.txt"
LOG_FILE = SEARCH_FOLDER + "/log.txt"
TIME_SERIES_FILE = SEARCH_FOLDER + "/time_series.txt"

def main(bootstrap=False):
    logger = Logger(LOG_FILE, TIME_SERIES_FILE)
    logger.log_config(TEST, STOP_TIME, PROT_DISCR_STEP, NON_PROT_DISCR_STEP, SMALLEST_VALUE, epsilon, delta)
    system = System(MODEL_FOLDER)
    param_bounds = parse_parameters_bounds_xml(XML_PATH)
    constraints = parse_constraints(CONSTRAINTS_PATH)
    system.set_constraints(constraints)
    parameter_space = ParameterSpace(param_bounds, system, PROT_DISCR_STEP, NON_PROT_DISCR_STEP, SMALLEST_VALUE)
    logger.log_parameter_space(parameter_space)
    if bootstrap:
        admissible_param = algorithm.bootstrap(system, parameter_space, STOP_TIME)
        utils.utils.save_parameters_to_file(ADM_PARAM_FILE, parameter_space, [admissible_param])
    adm_parameter_array = utils.utils.get_parameters_from_file(ADM_PARAM_FILE)[0]
    # adm_parameter_map = parameter_space.get_map_from_array(adm_parameter_array)
    # system.set_parameters(adm_parameter_map)
    # system.simulate(STOP_TIME, True)
    vps = algorithm.get_virtual_patients(system, parameter_space, adm_parameter_array, epsilon, delta, STOP_TIME, POWER_LAW_EXP, logger)
    utils.utils.save_parameters_to_file(PARAM_FILE, parameter_space, vps)


if __name__ == '__main__':
    main(bootstrap=False)