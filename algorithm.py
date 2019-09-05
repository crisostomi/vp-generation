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
                model.simulate(next_param, final_time=2000)
                if model.is_admissible():
                    current_admissible_params.add(next_param)
                    break

        if current_admissible_params == admissibile_params:
            break

    return admissibile_params


def choose_next_parameter(parameter_space, admissibile_params):
    return None



def bootstrap(model, parameter_space):
    opts = model.model.simulate_options()
    opts["CVode_options"]["verbosity"] = 50
    while True:
        parameters = parameter_space.get_random_parameters()
        model.set_parameters(parameters)
        print(model.model.get("parameters.species_70544_init"))
        try:
            model.simulate(options=opts, final_time=2000)
        except:
            print("bad setup parameters")
            continue
        if (model.is_admissible()):
            return parameters
        model.model.reset()
        model.set_parameter("parameters.simulation_time",2000)