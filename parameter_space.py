from enum import Enum

import numpy as np
import random

EPSILON_ABOVE_ZERO = 10**(-25)

class DiscretizationMethod(Enum):
    linear=0
    geometric=1

class ParameterSpace:
    def __init__(self, parameters, discretization_method=DiscretizationMethod.geometric, discretization_step=3, epsilon_above_zero=EPSILON_ABOVE_ZERO):
        self.map = dict()

        for param, bounds_tuple in parameters.items():
            param_name = "parameters."+param
            if discretization_method == DiscretizationMethod.geometric:
                self.map[param_name] = np.geomspace(
                    max(bounds_tuple[0], epsilon_above_zero),
                    bounds_tuple[1],
                    num=discretization_step
                )
            else:
                self.map[param_name] = np.linspace(
                    max(bounds_tuple[0], epsilon_above_zero),
                    bounds_tuple[1],
                    num=discretization_step
                )

    def get_parameter_values(self, parameter_name):
        return self.map[parameter_name]

    def get_random_parameters(self):
        random_parameters = dict()
        for param, linspace in self.map.items():
            random_index = random.randrange(len(linspace))
            random_parameters[param] = linspace[random_index]
        return random_parameters

    def get_parameters_number(self):
        return len(self.map.keys())

    def get_random_parameter_scalar(self, parameter_name):
        return np.random.choice(self.map[parameter_name])



