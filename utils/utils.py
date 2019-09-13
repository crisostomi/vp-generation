def get_parameters_from_file(file):
    tuples = []
    with open(file, "r") as f:
        for line in f.readlines():
            tuples.append(eval(line))
    tuples.pop(0)
    return tuples


def save_parameters_to_file(file, parameter_space, parameters):
    with open(file, "w+") as f:
        f.write(str(parameter_space.params))
        f.write("\n")
        for parameter in parameters:
            if type(parameter) == dict:
                parameter = parameter_space.get_array_from_map(parameter)
            f.write(str(parameter))
            f.write("\n")