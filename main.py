import math.log as log

print("Hello world!")


def bioAdmPars(S, space, admParameter, epsilon, delta, bounds):
    N = ( log(delta) ) / ( log(1-epsilon) )
    admissibleParams = { admParameter }
    simulationResult = simulate(S, admParameter)
    while True:
        S = admissibleParams
        for i in range(1,N):
            nextParam = chooseNextParameter(space, S)
            if nextParam not in S:
                newSimulationResult = simulate(S, nextParam)
                if adm(simulationResult, newSimulationResult, bounds):
                    admissibleParams += nextParam
                    break
        if admissibleParams == S:
            break
    return S


def simulate():
    pass

def adm():
    pass

def chooseNextParameter():
    pass
