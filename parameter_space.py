from enum import Enum
import numpy as np
import random

class ParameterSpace:
    def __init__(self, parameters, system, prot_discretization_step, non_prot_discretization_step, smallest_value):
        self.space = dict()
        self.params = list()

        for param, bounds_tuple in parameters.items():
            param_name = "parameters."+param
            discretization_step = prot_discretization_step if self.is_protein(param_name, system) else non_prot_discretization_step
            self.params.append(param_name)
            self.space[param_name] = np.geomspace(
                max(bounds_tuple[0], smallest_value),
                bounds_tuple[1],
                num=discretization_step
            )
        self.params = tuple(self.params)

    def is_protein(self, param, system ):
        return param in system.get_proteins()

    def get_space(self, parameter_name):
        return self.space[parameter_name]

    def get_random_parameter_as_map(self):
        random_parameters = dict()
        for param, linspace in self.space.items():
            random_index = random.randrange(len(linspace))
            random_parameters[param] = linspace[random_index]
        return random_parameters

    def get_random_parameter_as_array(self):
        random_parameters = list()
        for i in range(len(self.params)):
            param = self.params[i]
            param_space = self.space[param]
            random_index = random.randrange(len(param_space))
            random_parameters[param] = param_space[random_index]

        return tuple(random_parameters)

    def get_parameters_number(self):
        return len(self.space.keys())

    def get_random_parameter_scalar(self, param):
        if type(param) == str:
            return np.random.choice(self.space[param])
        elif type(param) == int:
            return np.random.choice(self.space[self.params[param]])
        else:
            raise Exception

    def get_array_from_map(self, map):
        # assert set(self.map.keys()) == set(map.keys())
        return tuple([map[self.params[i]] for i in range(len(self.params))])

    def get_map_from_array(self, array):
        # assert len(array) == len(self.map.keys())
        return {self.params[i]: array[i] for i in range(len(self.params))}


