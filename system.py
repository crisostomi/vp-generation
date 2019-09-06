import os

from pyfmi.fmi import load_fmu
from pymodelica import compile_fmu
import re
import numpy as np

UNDEFINED_PARAMETER = np.zeros(1)
MONITOR_PREFIX = "monitor."
PARAMETER_PREFIX = "parameters."
SIMULATION_SUFFIX = "simulation_time"
STOP_TIME = 20.0

class System:
    max = 0

    def __init__(self, path):
        modelica_files = []
        for file in os.listdir(path):
            if file.endswith(".mo"):
                modelica_files.append(path + "/" + file)

        fmu = compile_fmu("System", modelica_files)
        self.model = load_fmu(fmu)
        self.res = None
        self.abundances = None

    def is_admissible(self, tolerance=0.2):
        # per ogni average di cui esiste l'abundance, devo controllare che sia nel range di tolleranza
        assert self.res is not None
        assert self.abundances is not None

        admissible = True
        totProteins = len(self.abundances.items())
        admProteinsCount = 0
        admProteins = []
        for protein_name, abundance in self.abundances.items():
            for monitor_name in self.get_monitors_name():
                if protein_name in monitor_name:
                    monitor_value = self.res[monitor_name][-1]
                    min_range_value = abundance - tolerance * abundance
                    max_range_value = abundance + tolerance * abundance
                    # print(protein_name + " monitor :" + str(monitor_value) + " min: " + str(
                    #     min_range_value) + " max: " + str(max_range_value))
                    if monitor_value < min_range_value or monitor_value > max_range_value:
                        admissible = False
                    else:
                        admProteinsCount += 1
                        admProteins.append(protein_name)
                        
        if admProteinsCount > self.max:
            self.max = admProteinsCount
            print(str(self.max)+"/"+str(totProteins))
            print(admProteins)
        return admissible

    def simulate(self, options, final_time):
        self.res = self.model.simulate(final_time=final_time, options=options)

    def set_abundances(self, abundances):
        self.abundances = abundances

    def get_variables_name(self):
        return [str(var) for var in self.model.get_model_variables()]

    def get_monitors_name(self):
        return [var for var in self.get_variables_name() if var.startswith(MONITOR_PREFIX)]

    def get_parameters_name(self):
        return [var for var in self.get_variables_name() if var.startswith(PARAMETER_PREFIX) and not var.endswith(SIMULATION_SUFFIX)]

    def get_undefined_parameters_name(self):
        return [var for var in self.get_parameters_name() if self.parameter_is_undefined(var)]

    def parameter_is_undefined(self, parameter_name):
        parameter_value = self.model.get(parameter_name)
        return np.array_equal(parameter_value, UNDEFINED_PARAMETER)

    def set_parameter(self, parameter_name, value):
        self.model.set(parameter_name, value)

    def set_parameters(self, parameters):
        for param, value in parameters.items():
            self.set_parameter(param, value)

    def get_model_species(self):
        variables = self.get_variables_name()
        result = []
        for var in variables:
            regex = '(?<!=(der\())(compartment\w+\.species_[a-zA-Z0-9]+)(?!=(_init))'
            m = re.search(regex, var)
            if m is not None:
                result.append(m.group(0))

        return result

    # def simulate(self, parameters_values_map):
    #     for parameter, value in parameters_values_map.items():
    #         self.set_parameter(parameter, value)
    #
    #     self.simulate()
    #     return self.res

