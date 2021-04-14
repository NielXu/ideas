"""
A very simple implementation of Neural Network (NN) with no optimization at all.

For learning purpose only.
"""
import random
import math
from keras.datasets import mnist


class Neuron():
    """
    A neuron is a basic unit in the Neural Network, each neuron contains:
    1. input, the input to the neuron
    2. output, the output of the neuron, AFTER running the activation function
    3. activation, a activation function
    4. (extra) the derivative of the activation function
    """
    def __init__(self, input_, output, activation=None, deriv=None, activation_bounds=None):
        self.input_ = input_
        self.output = output
        self.activation = activation
        self.deriv = deriv
        if activation_bounds:
            self.activation_lower, self.activation_upper = activation_bounds
        else:
            self.activation_upper = None
            self.activation_lower = None
    
    def activate(self):
        self.output = self.activation(self.input_)
        return self.output

    def __str__(self):
        return f"Neuron(input={self.input_}, output={self.output})"

    def __repr__(self):
        return self.__str__()


class Input():
    """
    Input of the Neural Network, it should usually be preprocessed.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Input(value={self.value})"
    
    def __repr__(self):
        return self.__str__()


class NeuralNet():
    """
    A neural network contains:
    1. Inputs
    2. One or multiple layers
    3. A loss function to evaluate the network score
    """
    def __init__(self, inputs, layers, loss):
        self.inputs = inputs
        self.layers = layers
        self.weights = []
        self.weight_size = 0
        self.loss = loss
        self.errors = [0 for _ in layers[-1]]
        self.outputs = [0 for _ in layers[-1]]
    
    def train(self, X_train, y_train, epoch, alpha):
        for i in range(epoch):
            score = 0
            for index in range(len(X_train)):
                x = X_train[index]
                y = y_train[index]
                self.feed_forward(x)
                score = score + self.evaluate(y)
                self.back_propagation(y, alpha)
            print("After", i+1, "epoch, average loss:", score / len(X_train))

    def link(self, init_weight=0, rand_weight_range=None):
        # Link inputs with the first layer
        first_weights = [[self._initialize_weight(init_weight, rand_weight_range) for _ in self.layers[0]] for _ in self.inputs]
        self.weights.append(first_weights)
        self.weight_size = len(self.layers[0]) * len(self.inputs)

        # Do the same thing for the rest of the layers
        for i in range(len(self.layers)):
            if i + 1 < len(self.layers):
                layer_weights = [[self._initialize_weight(init_weight, rand_weight_range) for _ in self.layers[i+1]] for _ in self.layers[i]]
                self.weights.append(layer_weights)
                self.weight_size = self.weight_size + len(self.layers[i]) * len(self.layers[i+1])
        return self.weights

    def feed_forward(self, input_values):
        # Setup inputs values
        for index in range(len(input_values)):
            self.inputs[index].value = input_values[index]

        # Feed inputs into the first layer, loop in layer -> input order
        # to help activate a neuron after feeding all the values
        for index in range(len(self.layers[0])):
            neuron = self.layers[0][index]
            neuron_input_value = 0
            for jindex in range(len(self.inputs)):
                weight = self.weights[0][jindex][index]
                neuron_input_value = neuron_input_value + weight * self.inputs[jindex].value
            neuron.input_ = neuron_input_value
            neuron.activate()

        # Feed the rest of the layers
        layer_index = 0
        while layer_index + 1 < len(self.layers):
            layer = self.layers[layer_index]
            next_layer = self.layers[layer_index + 1]
            for index in range(len(next_layer)):
                neuron = next_layer[index]
                neuron_input_value = 0
                for jindex in range(len(layer)):
                    weight = self.weights[layer_index + 1][jindex][index]
                    neuron_input_value = neuron_input_value + weight * layer[jindex].output
                neuron.input_ = neuron_input_value
                neuron.activate()
            layer_index = layer_index + 1

        # Update outputs
        for i in range(len(self.layers[-1])):
            self.outputs[i] = self.layers[-1][i]
        return self.outputs
    
    def predict(self, input_values):
        self.feed_forward(input_values)
        return self.classify()

    def classify(self):
        max_val = 0
        max_index = 0
        for i in range(len(self.outputs)):
            output = self.outputs[i]
            if output.output > max_val:
                max_val = output.output
                max_index = i
        return max_index, max_val

    def evaluate(self, expected_values):
        total = 0
        for i in range(len(self.outputs)):
            total = total + self.loss(expected_values[i], self.outputs[i].output)
        return total

    def back_propagation(self, expected_values, alpha):
        # At least one hidden layer in the network
        if len(self.layers) > 1:
            # ==========================================================
            # I wrote them once and suprisingly there were no errors! :O
            # I cannot guarantee if the following codes are correct :D
            # ==========================================================
            prev_layer = self.layers[-2]
            # Hidden layer to outputs error
            track_err = [0 for _ in range(len(self.outputs))]
            track_weight = [[0 for _ in range(len(self.outputs))] for _ in range(len(prev_layer))]
            # For each neuron in the output layer
            for index in range(len(self.outputs)):
                output_neuron = self.outputs[index]
                # error_obj: The objective error, (T_j - O_j)
                error_obj = expected_values[index] - output_neuron.output
                # the total error, (T_j) * (O_j) * df(x)/dA_j(I)
                error = output_neuron.deriv(output_neuron.output) * error_obj
                # Save data for later used
                track_err[index] = error
                # For each neuron in the hidden layer
                for jindex in range(len(prev_layer)):
                    track_weight[jindex][index] = self.weights[-1][jindex][index]
                    prev_neuron = prev_layer[jindex]
                    # w_ab = w_ab + a * dA(I)/dw_ab * dO_b/dA(I) * dErr_b/dO_b
                    self.weights[-1][jindex][index] = self.weights[-1][jindex][index] + alpha * error * prev_neuron.output
            # Continue for the rest of the hidden layers
            # MAGIC...
            rest_index = len(self.layers) - 2
            while rest_index > 0:
                this_layer = self.layers[rest_index]
                prev_layer = self.layers[rest_index - 1]
                next_layer = self.layers[rest_index + 1]
                new_track_err = [0 for _ in range(len(this_layer))]
                new_track_weight = [[0 for _ in range(len(this_layer))] for _ in range(len(prev_layer))]
                for index in range(len(this_layer)):
                    this_neuron = this_layer[index]
                    for jindex in range(len(prev_layer)):
                        error = 0
                        for kindex in range(len(next_layer)):
                            error = error + track_err[kindex] * track_weight[index][kindex]
                        new_track_err[index] = error
                        prev_neuron = prev_layer[jindex]
                        new_track_weight[jindex][index] = self.weights[rest_index][jindex][index]
                        self.weights[rest_index][jindex][index] = self.weights[rest_index][jindex][index] + alpha * error * this_neuron.deriv(this_neuron.output) * this_neuron.output
                track_err = new_track_err
                track_weight = new_track_weight
                rest_index = rest_index - 1
            # Last step input->first layer
            for index in range(len(self.inputs)):
                for jindex in range(len(self.layers[0])):
                    neuron = self.layers[0][jindex]
                    error = 0
                    for kindex in range(len(self.layers[1])):
                        error = error + track_err[kindex] * track_weight[jindex][kindex]
                    self.weights[0][index][jindex] = self.weights[0][index][jindex] + alpha * error * neuron.deriv(neuron.output) * self.inputs[index].value
        # Inputs directly connected to the outputs
        else:
            self._back_propagation_no_hidden(alpha, expected_values)

    @classmethod
    def get_loss(cls, method="se"):
        if method == "se":
            return lambda actual, expected: (actual - expected) ** 2

    @classmethod
    def get_activation(cls, name):
        if name == "relu":
            return lambda x: x if x > 0 else 0
        elif name == "log":
            return lambda x: 1/(1 + math.e ** (-x))
        elif name == "hyper":
            return lambda x: math.tanh(x)

    @classmethod
    def get_deriv(cls, name):
        if name == "relu":
            return lambda x: 1 if x > 0 else 0
        elif name == "log":
            return lambda x: x * (1 - x)
        elif name == "hyper":
            return lambda x: 1 - x **2
    
    @classmethod
    def get_activation_bounds(cls, name):
        if name == "relu":
            return (0, 0)
        elif name == "log":
            return (0, 1)
        elif name == "hyper":
            return (-1, 1)

    @classmethod
    def create_layer(cls, n, activation):
        result = []
        for _ in range(n):
            result.append(
                Neuron(
                    0,
                    0,
                    cls.get_activation(activation),
                    cls.get_deriv(activation),
                    cls.get_activation_bounds(activation),
                )
            )
        return result

    @classmethod
    def create_input(cls, n):
        result = []
        for _ in range(n):
            result.append(Input(0))
        return result

    def _back_propagation_no_hidden(self, alpha, expected_values):
        for index in range(len(self.outputs)):
            output_neuron = self.outputs[index]
            for jindex in range(len(self.inputs)):
                error_obj = expected_values[index] - output_neuron.output
                deriv = output_neuron.deriv(output_neuron.output)
                self.weights[0][jindex][index] = self.weights[0][jindex][index] + alpha * self.inputs[jindex].value * deriv * error_obj

    def _initialize_weight(self, init_weight, rand_weight_range):
        if rand_weight_range is not None:
            return random.uniform(rand_weight_range[0], rand_weight_range[1])
        else:
            return init_weight

    def __str__(self):
        return f"NeuralNet(layers={len(self.layers)}, size={self.weight_size}, inputs={len(self.inputs)}, outputs={len(self.layers[-1])})"

    def __repr__(self):
        return self.__str__()


(X_train, y_train), (X_test, y_test) = mnist.load_data()
nn = NeuralNet(
    NeuralNet.create_input(28*28),
    [
        NeuralNet.create_layer(10, "hyper")
    ],
    NeuralNet.get_loss()
)
nn.link()
# Some updates required because of the implementation of the network
modified_y_train = []
for y in y_train:
    modified_y_train.append(
        [1 if a == y else 0 for a in range(10)]
    )
modified_y_test = []
for y in y_test:
    modified_y_test.append(
        [1 if a == y else 0 for a in range(10)]
    )
modified_X_train = []
for x in X_train:
    modified_X_train.append(x.flatten() / 255)
modified_X_test = []
for x in X_test:
    modified_X_test.append(x.flatten() / 255)

# Unfortunately the network training is very slow without any optimization,
# therefore, we can only train a very small portion of them. The original
# train size is 60000 and each image has size 28*28=784, it will take forever
# to train. Please modify the train_size accorindingly
train_size = 100
epochs = 20
learning_rate = 0.01
print("\nStart training with train_size=" + str(train_size))
nn.train(modified_X_train[:train_size], modified_y_train[:train_size], epochs, learning_rate)

test_size = 100
correct = 0
for i in range(test_size):
    expected = y_test[i]
    index, value = nn.predict(modified_X_test[i])
    if index == expected:
        correct = correct + 1
print("\nWith test_size=" + str(test_size), ", the correct rate is:", correct / test_size)
