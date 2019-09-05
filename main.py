from model import Model
import getpass

from parameter_space import ParameterSpace
from utils.handle_xml import *
from utils.plot import plot
import algorithm

SIMULATION_TIME = "parameters.simulation_time"

epsilon = 10**3
delta = 0.05

user = getpass.getuser()
PROJECT_FOLDER = "/home/"+user+"/Dropbox/Tesisti/software/test-cases"
TEST = "urea"
TEST_FOLDER = PROJECT_FOLDER + "/" + TEST
MODEL_FOLDER = TEST_FOLDER + "/out"
XML_PATH = MODEL_FOLDER + "/parameters.xml"
ABUNDANCES_PATH = MODEL_FOLDER + "/constraints.xml"

def main():
    model = Model(MODEL_FOLDER)
    param_bounds = parse_parameters_bounds_xml(XML_PATH)
    parameter_space = ParameterSpace(param_bounds, discretization_step=5)
    abundances = parse_abundance_xml(ABUNDANCES_PATH)
    model.set_parameter(SIMULATION_TIME, 2000)
    model.set_abundances(abundances)
    algorithm.bootstrap(model, parameter_space)
    # res = model.simulate(20.0)
    # plot(model, res)

if __name__ == '__main__':
    main()