import math


# S' = current_admissible_params
# S = admissibleParams
# cal(S) = system
# Lambda cappuccio = parameter_space


def getVirtualPatients(model, parameter_space, adm_parameter, epsilon, delta):
    N = (math.log(delta)) / (math.log(1 - epsilon))
    current_admissible_params = {adm_parameter}

    while True:
        admissibileParams = current_admissible_params
        for i in range(1, N):
            next_param = choose_next_parameter(parameter_space, admissibileParams)
            if next_param not in admissibileParams:
                simulationResult = model.simulate(next_param)
                if adm(simulationResult):
                    current_admissible_params += next_param
                    break

        if current_admissible_params == admissibileParams:
            break

    return admissibileParams


def choose_next_parameter():
    pass


def adm(simulation_result):
    return True


def bootstrap():
    pass
