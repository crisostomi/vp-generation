import math
import time
import numpy as np
import traceback

def get_virtual_patients(system, parameter_space, adm_parameter, epsilon, delta, stop_time, b, logger, method="CVode", steps="1e3"):
    N = int(math.ceil((math.log(delta)) / (math.log(1 - epsilon))))

    admissible_params = {adm_parameter}
    admissible_params_array = list(admissible_params)
    start_time = time.time()

    max_N = 0
    iterations = 0
    n = len(adm_parameter)
    numbers = np.arange(1, n+1)
    a = 1./sum([float(h)**(-b) for h in numbers])
    probabilities = {h: a*float(h)**(-b) for h in numbers}

    while True:
        new_parameter_found = False
        for i in range(1, N):
            iterations += 1
            if iterations % 1e4 == 0:
                logger.log_summary(iterations, time.time() - start_time, len(admissible_params))

            if i > max_N:
                max_N = i
            system.model.reset()
            new_param = choose_next_parameter(parameter_space, admissible_params_array, numbers, probabilities)
            if new_param not in admissible_params:
                param_map = parameter_space.get_map_from_array(new_param)
                system.set_parameters(param_map)
                try:
                    system.simulate(final_time=stop_time, verbose=False, method=method, steps=steps)
                except KeyboardInterrupt:
                    print "Algorithm interrupted"
                    logger.log_summary(iterations, time.time() - start_time, len(admissible_params))
                    return admissible_params
                except Exception:
                    traceback.print_exc()
                    continue
                if system.is_admissible():
                    logger.log_virtual_patient(param_map, i)
                    logger.log_time_course(system)
                    admissible_params.add(new_param)
                    admissible_params_array.append(new_param)
                    new_parameter_found = True
                    break

        if not new_parameter_found:
            break

    logger.log_summary(iterations, time.time()-start_time, len(admissible_params))
    return admissible_params


def choose_next_parameter(parameter_space, admissible_params_array, numbers, probabilities):

    L = len(admissible_params_array)
    i = np.random.randint(0, L)
    param_vector = admissible_params_array[i]

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
