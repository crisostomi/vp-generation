from model import Model
from random import *
import getpass

epsilon = 10**3
delta = 0.05

def main():
    user = getpass.getuser()
    model = Model("/home/"+user+"/Dropbox/Tesisti/software/test-cases/urea/out")
    for var in model.get_model_parameters_name():
        value = random()
        model.set_model_parameter(var, value)
        print var, value

    for species in model.get_model_species():
        print species

    model.simulate(20.0)
    model.plot()


if __name__ == '__main__':
    main()