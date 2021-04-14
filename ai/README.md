# AI
Some algorithms related to artificial intelligence. Most of them are from [CSCD84](https://utsc.calendar.utoronto.ca/course/cscd84h3), which is very interesting to study if you are interested in AI.


## bayes_net.py
__From Wikipedia:__
A Bayesian network (also known as a Bayes network, belief network, or decision network) is a probabilistic graphical model that represents a set of variables and their conditional dependencies via a directed acyclic graph (DAG).

This script is a very basic example of Bayesian Network including four variables: Cloudy(C), Sprinkler(S), Rain(R) and Wet grass(W).
- Sprinkler depends on cloudy (C -> S)
- Rain depends on cloudy (C -> R)
- Wet grass depends on sprinkler and rain (S, R -> W)

It contains two parts: random sampling to all variables and random sampling with observed variables.


## neural_net.py
My own implementation of the Neural Network without any optimization. It contains some pre-defined functions that are ready to use and supports the following features:
1. Create a neural network with simple calls:

```python
nn = NeuralNet(
    NeuralNet.create_input(28*28),          # Create inputs
    [
        NeuralNet.create_layer(10, "hyper") # One layer (No hidden layers) with 10 neurons using hyperbolic tangent as the activation function
    ],
    NeuralNet.get_loss()                    # A loss function to evaluate the network
)
```

2. Train the given data:

```python
nn.train(X_train, y_train, 20, 0.01)        # Train the network for 20 epochs, 0.01 learning rate
```

3. Predict the test data using the trained network

```python
nn.predict(X_test)
```

#### Setup

Install the required packages, keras and tensorflow to gather the MNIST dataset only (Because I am too lazy to write my own script to gather it):

```
$ pip install -r requirements.txt
```

#### MNIST

It also demostrates the training and testing process of the very famous dataset MNIST. However, the network will train very slowly with a large dataset without any optimization, therefore, I only recommend you to test a portion of it. By modifying: 

```python
train_size = 100  # The original size is 60000
test_size = 100   # The original size is 60000
```

Example output:
```
Start training with train_size=100
After 1 epoch, average loss: 0.7488040729854367
After 2 epoch, average loss: 0.40561451535691
After 3 epoch, average loss: 0.31401908778790627
After 4 epoch, average loss: 0.2606107411021518
After 5 epoch, average loss: 0.22456867296787017
After 6 epoch, average loss: 0.19831484803341268
After 7 epoch, average loss: 0.17805740822737703
After 8 epoch, average loss: 0.16175216374819068
After 9 epoch, average loss: 0.14823737234320922
After 10 epoch, average loss: 0.13680358281031635
After 11 epoch, average loss: 0.12698303843256448
After 12 epoch, average loss: 0.11844669351681103
After 13 epoch, average loss: 0.11095181431124607
After 14 epoch, average loss: 0.10431337067575151
After 15 epoch, average loss: 0.09838710212156436
After 16 epoch, average loss: 0.09305872252611647
After 17 epoch, average loss: 0.08823661122471085
After 18 epoch, average loss: 0.08384663185521889
After 19 epoch, average loss: 0.0798283323847187
After 20 epoch, average loss: 0.07613208801989829

With test_size=100 , the correct rate is: 0.7
```
