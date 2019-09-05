import algorithm

epsilon = 10**3
delta = 0.05
from pyfmi.examples import fmi_bouncing_ball
def main():

    # admParameter = algorithm.bootstrap()
    # parameterSpace = "?"
    # algorithm.getVirtualPatients("model", parameterSpace, admParameter, epsilon, delta)
    fmi_bouncing_ball.run_demo()

