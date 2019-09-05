import numpy as np


class ParameterSpace:
    def __init__(self, parameters, discretization_step=3):
        self.map = dict()

        for param, bounds_tuple in parameters.items():
            self.map[param] = np.linspace(bounds_tuple[0], bounds_tuple[1], num=discretization_step)

    def get_parameter_values(self, parameter_name):
        return self.map[parameter_name]

    def get_parameters_number(self):
        return len(self.map.keys())

    def get_random_parameter_scalar(self, parameter_name):
        return np.random.choice(self.map[parameter_name])



