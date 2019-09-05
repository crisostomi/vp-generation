import math
import simulator
# S' = currentAdmissibleParams
# S = admissibleParams
# cal(S) = system
# Lambda cappuccio = parameterSpace


def getVirtualPatients(model, parameterSpace, admParameter, epsilon, delta):
    N = ( math.log(delta) ) / ( math.log(1-epsilon) )
    currentAdmissibleParams = { admParameter }

    while True:
        admissibileParams = currentAdmissibleParams
        for i in range(1,N):
            nextParam = chooseNextParameter(parameterSpace, admissibileParams)
            if nextParam not in admissibileParams:
                simulationResult = simulator.simulate(model, nextParam)
                if adm(simulationResult):
                    currentAdmissibleParams += nextParam
                    break

        if currentAdmissibleParams == admissibileParams:
            break

    return admissibileParams

def chooseNextParameter():
    pass

def adm():
    pass

def bootstrap():
    pass