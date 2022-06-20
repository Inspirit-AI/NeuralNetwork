from math import e
from random import uniform


class Node:

    MIN_WEIGHT = -3
    MAX_WEIGHT = 3

    MIN_BIAS = -1
    MAX_BIAS = 1

    DEFAULT_SIGMOID_VALUE = 0.1

    MAX_MUTATION = 0.5

    def __init__(self, weights: list[float], biases: list[float], children: list, sigmoid_value: float):
        """
        :param weights: the weight attached to this node
        :param biases: the bias (constant)
        :param children: the list of all attached nodes
        :param sigmoid_value: a float that is used in the sigmoid activation function
        """

        # the length of weights and biases are the number of inputs
        self.numInputs = len(weights)

        # there must be an equal amount of weights and biases because they are applied together
        # allow difference number of weights/biases and children
        if len(weights) != len(biases):
            raise ValueError("Different amount of weights and biases.")

        # these are part of the function that is applied when this node is called
        self.weights = weights
        self.biases = biases

        # a list of all the attached nodes
        self.children = children

        # sigmoid_value is the coefficient used in sigmoid function
        # 1 / (1 + e^-cx) where c is sigmoid_value
        self.sigmoid_value = sigmoid_value

        # this is the last value associated with this node
        # this will be used to call the next in layer
        self.value = 0

    def mutate(self):
        """
        This function would change the weights by a random percent, up to MAX_MUTATION
        """

        # mutating the weights by a random amount within -max and max
        for index in range(len(self.weights)):
            change = uniform(-self.MAX_MUTATION, self.MAX_MUTATION)
            self.weights[index] *= (1 - change)

        # mutating the biases by a random amount within -max and max
        for index in range(len(self.biases)):
            change = uniform(-self.MAX_MUTATION, self.MAX_MUTATION)
            self.biases[index] *= (1 - change)

        # returning the mutated node
        return self

    def setChildren(self, newChildren: list):
        """
        :param newChildren: the new children list that this node will be
        :return: does not return anything
        """

        self.children = newChildren

    def isInChildren(self, other) -> bool:
        """
        :param other: Node
        :return: returns other in list of children
        """

        # does a check whether another node is in its list of children
        return other in self.children

    def isConnectedTo(self, other) -> bool:
        """
        :param other: Node
        :return: one of descendents, no matter how deep
        """

        # first checks whether this other is in the children list
        # if it is not in its children list, it checks whether it is connected to any of the children
        return self.isInChildren(other) or any(map(lambda child: child.isConnectedTo(other), self.children))

    def sigmoid(self, num):
        return 1 / (1 + e ** (-1 * num * self.sigmoid_value)) / self.numInputs

    def __call__(self, nums: list[float]) -> float:
        """
        :param nums: list of outputs from previous nodes
        :return the value of self
        """

        # call this node with a list of inputs (from previous layer)
        # applies a sigmoid function on the sum of weights * input

        self.value = sum(map(lambda weight, bias, num: self.sigmoid(weight * num + bias),
                             self.weights, self.biases, nums))

        return self.value

    def gradient(self, nums: list[float], goal: float, learnRate):
        length = len(nums)

        for index, (weight, bias, num) in enumerate(zip(self.weights, self.biases, nums)):
            weightChange, biasChange = self.gradientHelper(weight, bias, num, goal / length)
            weightChange *= learnRate
            biasChange *= learnRate

            self.weights[index] -= weightChange
            self.biases[index] -= biasChange

    def gradientHelper(self, weight: float, bias: float, num: float, goal: float, ) -> tuple[float, float]:
        # this is a precalculated gradient vector function
        # a gradient is just a vector of partial derivatives of the loss function
        # with respect to weight and bias
        # this gives you a vector tangent to the 3d loss function

        a = weight * num + bias
        b = e ** (-a * self.sigmoid_value) + 1
        c = 1 / (b * self.numInputs)
        d = (c - goal) ** 2

        partialDerivativeRespectBias = 2 * self.sigmoid_value * b * (c - goal) / (b ** 2 * self.numInputs)
        partialDerivativeRespectWeight = partialDerivativeRespectBias * num

        return partialDerivativeRespectWeight, partialDerivativeRespectBias

    @staticmethod
    def loss(weight: float, bias: float, num: float, goal: float) -> float:
        # this is the square of the error
        return (weight * num + bias - goal) ** 2

    def __deepcopy__(self, memo):
        """
        :param memo: not used. this is a parameter because __deepcopy__ overrides a default function
        :return: the copied node object
        """

        # creating copy of weight through list comprehension
        # because weights are floats, do not need to copy weights
        weightsCopy = [weight for weight in self.weights]

        # creating copy of biases through list comprehension
        # because biases are floats, do not need to copy biases
        biasesCopy = [bias for bias in self.biases]

        # returning the copied node
        # does not change the children list
        return Node(weightsCopy, biasesCopy, self.children, self.sigmoid_value)

    def asDict(self) -> dict:
        """
        :return: a dictionary representation of the node
        """

        # keys are weights and biases
        return {"Weights": self.weights, "Biases": self.biases}


def randomNode(numInputs: int) -> Node:
    """
    :param numInputs: number of inputs it will receive
    :return: a node generated with random weights/biases
    """

    # create a list with a random weight (in the range of Min/Max weights)
    # length of list is numInputs
    randomWeights = [uniform(Node.MIN_WEIGHT, Node.MAX_WEIGHT) for _ in range(numInputs)]

    # creates a list with random biases (in the range of Min/Max biases)
    # length of list is numInputs
    randomBiases = [uniform(Node.MIN_BIAS, Node.MAX_BIAS) for _ in range(numInputs)]

    # uses default sigmoid value
    defaultSigmoid = Node.DEFAULT_SIGMOID_VALUE

    # does not initialize children
    # must initialize later in the calling of random node
    emptyChildren = []

    # creates a new node with these variables
    return Node(weights=randomWeights, biases=randomBiases, children=emptyChildren, sigmoid_value=defaultSigmoid)
