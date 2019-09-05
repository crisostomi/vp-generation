import os

from pyfmi.fmi import load_fmu
from pymodelica import compile_fmu
import re
import matplotlib.pyplot as plt



class Model:
    def __init__(self, path):
        modelicaFiles = []
        for file in os.listdir(path):
            if file.endswith(".mo"):
                modelicaFiles.append(path + "/" + file)

        fmu = compile_fmu("System", modelicaFiles)
        self.model = load_fmu(fmu)
        self.res = None

    def get_model_variables_name(self):
        return [str(var) for var in self.model.get_model_variables()]

    def get_model_parameters_name(self):
        return [var for var in self.get_model_variables_name() if var.startswith("parameters.")]

    def set_model_parameter(self, parameter_name, value):
        self.model.set(parameter_name, value)

    def simulate(self, stop_time):
        self.res = self.model.simulate(final_time=stop_time)

    def get_model_species(self):
        variables = self.get_model_variables_name()
        result = []
        for var in variables:
            regex = '(?<!der\()(compartment\w+\.species_[a-zA-Z0-9]+)(?!_init)'
            m = re.search(regex, var)
            if m is not None:
                result.append(m.group(0))

        return result

    def plot(self, species=[]):
        t = self.res["time"]
        plt.figure(1)
        if len(species) == 0:
            species = self.get_model_species()

        for s in species:
            plt.plot(t, self.res[s])

        plt.grid(True)
        plt.legend(species)
        plt.grid(True)
        plt.show()
