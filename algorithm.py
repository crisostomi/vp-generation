import math
import time
import numpy as np


STOP_TIME_PARAMETER = "parameters.simulation_time"
STOP_TIME = 1e5


def get_virtual_patients(model, parameter_space, adm_parameter, epsilon, delta, b=1.5, limit=0, verbose=0):
    N = int((math.log(delta)) / (math.log(1 - epsilon)))
    if verbose > 0:
        print "N = " + str(N)

    if type(adm_parameter) == dict:
        adm_parameter = parameter_space.get_array_from_map(adm_parameter)

    if verbose > 1:
        print "Admissible parameter vector: " + str(adm_parameter)

    admissible_params = {adm_parameter}
    admissible_params_array = list(admissible_params)
    start_time = time.time()

    max_N = 0
    n = len(adm_parameter)
    numbers = np.arange(1, n+1)
    a = 1./sum([float(h)**(-b) for h in numbers])
    probabilities = {h: a*float(h)**(-b) for h in numbers}

    while True:
        new_parameter_found = False
        for i in range(1, N):
            if i > max_N:
                max_N = i
                if verbose > 0:
                    print "Maximum number of failures: " + str(max_N)
            model.model.reset()
            timer_1 = time.time()
            new_param = choose_next_parameter(parameter_space, admissible_params_array, numbers, probabilities, verbose=verbose)
            elapsed_time_1 = (time.time() - timer_1)
            if verbose > 1:
                print "New parameter: " + str(new_param)
            timer_2 = time.time()
            if new_param not in admissible_params:
                elapsed_time_2 = time.time() - timer_2
                param_map = parameter_space.get_map_from_array(new_param)
                model.set_parameters(param_map)
                try:
                    timer_3 = time.time()
                    model.simulate(final_time=STOP_TIME, verbose=False)
                    elapsed_time_3 = time.time() - timer_3
                except:
                    continue
                if model.is_admissible():
                    if verbose > 1:
                        print "Parameter is admissible, number of current admissible params: " \
                              + str(len(admissible_params))

                    if verbose > 0 and len(admissible_params) % 100 == 0:
                        elapsed_time = time.time() - start_time
                        print "\n[%.3f s]" % elapsed_time + \
                              " Number of current admissible params: " + str(len(admissible_params))
                        print "Random sampling time: %f" % elapsed_time_1
                        print "Containment check time: %f" % elapsed_time_2
                        print "Simulation time: %f" % elapsed_time_3

                    admissible_params.add(new_param)
                    admissible_params_array.append(new_param)
                    new_parameter_found = True
                    if limit != 0 and len(admissible_params) >= limit:
                        return admissible_params

                    break

        if not new_parameter_found:
            break

    return admissible_params


def choose_next_parameter(parameter_space, admissible_params_array, numbers, probabilities, verbose=2):

    L = len(admissible_params_array)
    i = np.random.randint(0, L)
    param_vector = admissible_params_array[i]

    if verbose > 1:
        print "Random admissible parameter: " + str(param_vector)

    n = len(param_vector)

    number_of_components_to_be_changed = 0
    while number_of_components_to_be_changed == 0:
        np.random.shuffle(numbers)
        for i in range(0, n):
            h = numbers[i]
            prob_h = probabilities[h]
            if np.random.random() <= prob_h:
                number_of_components_to_be_changed = h

    components_to_be_changed = np.random.choice(np.arange(0, n), number_of_components_to_be_changed)
    if verbose > 1:
        print "Components changed: " + str(components_to_be_changed)

    new_vector = list()
    for i in range(n):
        if i in components_to_be_changed:
            value = parameter_space.get_random_parameter_scalar(i)
        else:
            value = param_vector[i]

        new_vector.append(value)

    return tuple(new_vector)


def bootstrap(model, parameter_space, stop_time):
    while True:
        parameters = parameter_space.get_random_parameter_as_map()
        model.set_parameters(parameters)
        try:
            model.simulate(final_time=stop_time, verbose=False)
        except:
            print("bad setup parameters")

        if model.is_admissible():
            return parameters
        model.model.reset()
