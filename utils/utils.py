def get_parameter_from_file(file):
    f = open(file)
    content = f.readline()
    dict = eval(content)
    return dict