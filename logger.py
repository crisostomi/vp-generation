import math
import os

INDENT = "\t"


class Logger:
    def __init__(self, file_name):
        self.file_name = self.find_file_name(file_name)
        self.buffer = ""

    def write_to_file(self, content, append):
        mod = "a" if append else "w+"
        with open(self.file_name, mod) as f:
            f.write(content+"\n")

    def log_config(self, test, stop_time, prot_discr_step, non_prot_discr_step, smallest_value, epsilon, delta):
        N = int(math.ceil((math.log(delta)) / (math.log(1 - epsilon))))
        content = "TEST: {}\n".format(test)
        content += INDENT+"stop time: {}\n".format(stop_time)
        content += INDENT+"protein discretization step: {}\n".format(prot_discr_step)
        content += INDENT+"non protein discretization step: {}\n".format(non_prot_discr_step)
        content += INDENT+"smallest value: {}\n".format(smallest_value)
        content += INDENT+"epsilon: {}\n".format(epsilon)
        content += INDENT + "delta: {}\n".format(delta)
        content += INDENT + "N: {}\n".format(N)
        self.write_to_file(content, False)

    def log_parameter_space(self, parameter_space):
        content = "Parameter space: \n"
        for param in parameter_space.params:
            space = parameter_space.space[param]
            content += INDENT+"{}: {}\n".format(param, space)
        self.write_to_file(content, True)

    def log_virtual_patient(self, virtual_patient, failures):
        content = "VP: \n"
        content += INDENT+"failures: {}\n".format(failures)
        content += INDENT+str(virtual_patient)+"\n"
        self.buffer += content

    def flush(self):
        self.write_to_file(self.buffer, True)
        self.buffer = ""

    def log_summary(self, iterations, elapsed_time, vp_count):
        content = "\niterations: {}\n".format(iterations)
        content += "elapsed time: %.3f \n"%elapsed_time
        content += "virtual patients found: {}\n".format(vp_count)
        self.buffer += content
        self.flush()

    def find_file_name(self, file_name):
        if os.path.exists(file_name):
            i = 0
            name, ext = os.path.splitext(file_name)
            while True:
                new_name = name + "_%d" % i
                new_file_name = new_name + ext
                if os.path.exists(new_file_name):
                    i += 1
                else:
                    return new_file_name
        else:
            return file_name

