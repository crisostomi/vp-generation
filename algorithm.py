import math
import random
import time

import numpy as np
import traceback

# S' = current_admissible_params
# S = admissibleParams
# cal(S) = system
# Lambda cappuccio = parameter_space

STOP_TIME_PARAMETER = "parameters.simulation_time"
STOP_TIME = 20


def getVirtualPatients(model, parameter_space, adm_parameter, epsilon, delta, verbose=True):
    N = int((math.log(delta)) / (math.log(1 - epsilon)))
    if verbose:
        print "N = " + str(N)

    if type(adm_parameter) == dict:
        adm_parameter = parameter_space.get_array_from_map(adm_parameter)

    if verbose:
        print "Admissible parameter vector: " + str(adm_parameter)

    current_admissible_params = {adm_parameter}
    admissible_params = set()
    start_time = time.time()
    while True:
        admissible_params.update(current_admissible_params)
        for i in range(1, N):
            model.model.reset()
            next_param = choose_next_parameter(parameter_space, admissible_params, verbose=verbose)
            if verbose:
                print "New parameter: " + str(next_param)
            if next_param not in admissible_params:
                param_map = parameter_space.get_map_from_array(next_param)
                model.set_parameters(param_map)
                model.simulate(final_time=STOP_TIME, verbose=False)
                if model.is_admissible():
                    if verbose:
                        print "Parameter is admissible, number of current admissible params: " \
                              + str(len(current_admissible_params))

                    if len(current_admissible_params) % 100 == 0:
                        elapsed_time = time.time() - start_time
                        print "[%.3f s]" % elapsed_time + \
                              " Number of current admissible params: " + str(len(current_admissible_params))

                    current_admissible_params.add(next_param)
                    break

        if current_admissible_params == admissible_params:
            break

    return admissible_params


def choose_next_parameter(parameter_space, admissible_params, b=2, verbose=True):

    param_vector = random.choice(list(admissible_params))
    if verbose:
        print "Random admissible parameter: " + str(param_vector)

    n = len(param_vector)
    numbers = np.arange(1, n+1)
    probabilities = {h: float(h)**(-b) for h in numbers}

    number_of_components_to_be_changed = 0
    while number_of_components_to_be_changed == 0:
        np.random.shuffle(numbers)
        for i in range(0, n):
            h = numbers[i]
            prob_h = probabilities[h]
            if np.random.random() <= prob_h:
                number_of_components_to_be_changed = h

    components_to_be_changed = np.random.choice(np.arange(0, n), number_of_components_to_be_changed)
    if verbose:
        print "Components changed: " + str(components_to_be_changed)

    new_vector = list()
    for i in range(n):
        if i in components_to_be_changed:
            value = parameter_space.get_random_parameter_scalar(i)
        else:
            value = param_vector[i]

        new_vector.append(value)

    return tuple(new_vector)


def bootstrap(model, parameter_space):
    while True:
        parameters = parameter_space.get_random_parameter_as_map()
        model.set_parameters(parameters)
        try:
            model.simulate(final_time=STOP_TIME, verbose=False)
        except:
            print("bad setup parameters")
            traceback.print_exc()
            exit(0)

        if model.is_admissible():
            return parameters
        model.model.reset()
