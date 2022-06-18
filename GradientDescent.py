from NeuralNetwork import NeuralNetwork
from random import uniform


class GradientNetwork(NeuralNetwork):

    def __init__(self, *, numInputs: int, nodesInLayer: int = 5, numLayers: int = 2, nodes=None,
                 maxIter: int = 10, learnRate: float = 0.1):
        super().__init__(numInputs, nodesInLayer, numLayers, nodes)

        self.maxIter = maxIter
        self.learnRate = learnRate

        self.size = nodesInLayer * numLayers

    def evolve(self, inputs, goal):

        for _ in range(self.maxIter):
            self(inputs)
            print("Current iteration value:", self.value)
            self.stepGeneration(inputs, goal)

    def evolveTillTolerance(self, inputs, goal, tolerance=0):
        MAXIMUM_ITERATION = 1000

        if tolerance <= 0:
            tolerance = 0.1

        iterationCounter = 0
        while iterationCounter < MAXIMUM_ITERATION:
            if abs(self.value - goal) < abs(tolerance * goal):
                print(f"Value at iteration {iterationCounter}:", self.value)
                break

            self(inputs)
            if iterationCounter % 5 == 0:
                print(f"Value at iteration {iterationCounter}:", self.value)

            self.stepGeneration(inputs, goal)
            iterationCounter += 1

        print(f"Reached {abs((self.value - goal) * 100 / goal)} percent of goal after {iterationCounter} iterations")

    def stepGeneration(self, inputs, goal):
        for index in range(self.nodesInLayer):
            node = self.nodes[0][index]
            node.gradient(inputs, goal / self.size, self.learnRate)