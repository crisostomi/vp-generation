def get_parameters_from_file(file, parameter_space):
    tuples = []
    with open(file, "r") as f:
        for line in f.readlines():
            tuples.append(eval(line))
    parameters = tuples.pop(0)
    values = tuples.pop(0)
    map = dict()
    for i in range(len(parameters)):
        p = parameters[i]
        v = values[i]
        map[p] = v

    return parameter_space.get_array_from_map(map)


def save_parameters_to_file(file, parameter_space, parameters):
    with open(file, "w+") as f:
        f.write(str(parameter_space.params))
        f.write("\n")
        for parameter in parameters:
            if type(parameter) == dict:
                parameter = parameter_space.get_array_from_map(parameter)
            f.write(str(parameter))
            f.write("\n")