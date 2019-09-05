import numpy as np
import random

class ParameterSpace:
    def __init__(self, parameters, discretization_step=3):
        self.map = dict()

        for param, bounds_tuple in parameters.items():
            param_name = "parameters."+param
            self.map[param_name] = np.geomspace(bounds_tuple[0]+10**(-20), bounds_tuple[1], num=discretization_step)

    def get_parameter_values(self, parameter_name):
        return self.map[parameter_name]

    def get_random_parameters(self):
        random_parameters = dict()
        for param, linspace in self.map.items():
            random_index = random.randrange(len(linspace))
            random_parameters[param] = linspace[random_index]
        return random_parameters




