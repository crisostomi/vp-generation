import math
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
                model.simulate(next_param)
                if model.is_admissible():
                    current_admissible_params.add(next_param)
                    break

        if current_admissible_params == admissibile_params:
            break

    return admissibile_params


def choose_next_parameter(parameter_space, admissibile_params):
    return None



def bootstrap():
    # montecarlo per trovare admissibile
    pass
