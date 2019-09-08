def get_parameter_from_file(file):
    with open(file, "r") as f:
        content = f.readline()
        dict = eval(content)

    return dict


def save_parameters_to_file(file, parameter_space, parameter_arrays):
    with open(file, "w+") as f:
        f.write(str(parameter_space.params))
        f.write("\n")
        for parameter_array in parameter_arrays:
            f.write(str(parameter_array))
            f.write("\n")