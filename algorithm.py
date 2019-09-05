import math
import numpy as np
from copy import deepcopy


# S' = current_admissible_params
# S = admissibleParams
# cal(S) = system
# Lambda cappuccio = parameter_space


def getVirtualPatients(model, parameter_space, adm_parameter, epsilon, delta):
    N = (math.log(delta)) / (math.log(1 - epsilon))
    current_admissible_params = {adm_parameter}

    while True:
        admissibile_params = deepcopy(current_admissible_params)
        for i in range(1, N):
            next_param = choose_next_parameter(parameter_space, admissibile_params)
            if next_param not in admissibile_params:
                model.simulate(next_param, final_time=2000)
                if model.is_admissible():
                    current_admissible_params.add(next_param)
                    break

        if current_admissible_params == admissibile_params:
            break

    return admissibile_params

def choose_next_parameter(parameter_space, admissibile_params, b=2):
    param_vector = np.random.choice(admissibile_params, 1)[0]

    n = len(param_vector)
    numbers = np.arange(1, n+1)
    parameters_names = sorted(list(parameter_space.map.keys()))
    probabilities = {h: h**(-b) for h in numbers}

    np.random.shuffle(numbers)

    number_of_components_to_be_changed = 0
    while number_of_components_to_be_changed == 0:
        for i in range(0, n):
            h = numbers[i]
            prob_h = probabilities[h]
            if np.random.random() <= prob_h:
                number_of_components_to_be_changed = h

        np.random.shuffle(numbers)

    compontents_to_be_changed = np.random.choice(np.arange(0, n), number_of_components_to_be_changed)
    new_vector = dict()
    for i in range(n):
        param = parameters_names[i]
        if i in compontents_to_be_changed:
            value = parameter_space.get_random_parameter_scalar(param)
        else:
            value = param_vector[param]

        new_vector[param] = value

    return new_vector

def bootstrap(model, parameter_space):
    opts = model.model.simulate_options()
    opts["CVode_options"]["verbosity"] = 50
    while True:
        parameters = parameter_space.get_random_parameters()
        model.set_parameters(parameters)
        try:
            model.simulate(options=opts, final_time=2000)
        except:
            print("bad setup parameters")
            continue
        if (model.is_admissible()):
            return parameters
        model.model.reset()
        model.set_parameter("parameters.simulation_time",2000)