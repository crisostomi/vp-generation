import os
from pyfmi.fmi import load_fmu
from pymodelica import compile_fmu
import re
import numpy as np

UNDEFINED_PARAMETER = np.zeros(1)
MONITOR_PREFIX = "monitor."
PARAMETER_PREFIX = "parameters."
SIMULATION_SUFFIX = "simulation_time"


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
        self.constraints = None

    def is_admissible(self):
        # per ogni monitor di errore, devo controllare se sta nei bounds specificati nei constraints
        assert self.res is not None
        assert self.constraints is not None

        adm_proteins_count = 0
        adm_proteins = []
        tot_proteins = len(self.constraints.items())

        admissible = True
        for monitor, bounds in self.constraints.items():
            lb, ub = bounds
            monitor_name = MONITOR_PREFIX + monitor
            monitor_value = self.res[monitor_name][-1]
            if monitor_value < lb or monitor_value > ub:
                admissible = False
            else:
                adm_proteins_count += 1
                adm_proteins.append(monitor_name)

        if adm_proteins_count > self.max:
            self.max = adm_proteins_count
            print(str(self.max)+"/"+str(tot_proteins))
            print(adm_proteins)

        return admissible

    def simulate(self, final_time, verbose=True):
        opts = self.model.simulate_options()  # Retrieve the default options
        self.set_parameter(PARAMETER_PREFIX + SIMULATION_SUFFIX, final_time)
        if not verbose:
            opts["CVode_options"]["verbosity"] = 50
            self.res = self.model.simulate(final_time=final_time, options=opts)
        else:
            self.res = self.model.simulate(final_time=final_time, options=opts)

    def set_constraints(self, constraints):
        self.constraints = constraints

    def get_proteins(self):
        proteins = []
        for constraint in self.constraints.keys():
            initialParameter = "parameters." + constraint.replace("error", "init")
            proteins.append(initialParameter)
        return proteins

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
            regex = '(?<!=(der\())(compartment\w+\.species_[a-zA-Z0-9]+_conc)(?!=(_init))'
            m = re.search(regex, var)
            if m is not None:
                result.append(m.group(0))

        return result

    def set_parameters_from_file(self, file):
        f = open(file)
        content = f.readline()
        dict = eval(content)
        self.set_parameters(dict)
        f.close()