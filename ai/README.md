# AI
Some algorithms related to artificial intelligence. Most of them are from [CSCD84](https://utsc.calendar.utoronto.ca/course/cscd84h3), which is very interesting to study if you are interested in AI.

Don't forget to install the required packages if you want to run the scripts in this folder.

```
$ pip install -r requirements.txt
```


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


## cnn_keras.py
This is an example from the [keras website](https://keras.io/examples/vision/mnist_convnet/). It uses the convolutional neural network (CNN) to train a model for recognzing the hand-written digits (MNIST dataset) with accuracy ~99%. The model definition is the following:
```python
model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
```
The idea of CNN is to group a few pixels as a box (`kernel_size`) and train their weights accordingly. We can do it because we usually only need to observe a small area of the graph to extract the features, instead of looking it pixels by pixels. It also uses a concept call pooling, which will reduce the number of calculations we need by selecting the maximum value (`MaxPooling`) in a small area (`pool_size`). Check out [this acticle](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53) for more information.

#### Train result
```
Epoch 1/15
422/422 [==============================] - 15s 34ms/step - loss: 0.7476 - accuracy: 0.7718 - val_loss: 0.0803 - val_accuracy: 0.9762
Epoch 2/15
422/422 [==============================] - 14s 32ms/step - loss: 0.1208 - accuracy: 0.9627 - val_loss: 0.0596 - val_accuracy: 0.9837
Epoch 3/15
422/422 [==============================] - 15s 36ms/step - loss: 0.0864 - accuracy: 0.9743 - val_loss: 0.0449 - val_accuracy: 0.9872
Epoch 4/15
422/422 [==============================] - 15s 35ms/step - loss: 0.0680 - accuracy: 0.9787 - val_loss: 0.0414 - val_accuracy: 0.9882
Epoch 5/15
422/422 [==============================] - 13s 32ms/step - loss: 0.0624 - accuracy: 0.9808 - val_loss: 0.0385 - val_accuracy: 0.9878
Epoch 6/15
422/422 [==============================] - 13s 31ms/step - loss: 0.0554 - accuracy: 0.9838 - val_loss: 0.0352 - val_accuracy: 0.9910
Epoch 7/15
422/422 [==============================] - 14s 32ms/step - loss: 0.0513 - accuracy: 0.9833 - val_loss: 0.0309 - val_accuracy: 0.9923
Epoch 8/15
422/422 [==============================] - 14s 33ms/step - loss: 0.0473 - accuracy: 0.9858 - val_loss: 0.0319 - val_accuracy: 0.9907
Epoch 9/15
422/422 [==============================] - 14s 34ms/step - loss: 0.0461 - accuracy: 0.9864 - val_loss: 0.0323 - val_accuracy: 0.9913
Epoch 10/15
422/422 [==============================] - 14s 33ms/step - loss: 0.0403 - accuracy: 0.9859 - val_loss: 0.0289 - val_accuracy: 0.9913
Epoch 11/15
422/422 [==============================] - 14s 34ms/step - loss: 0.0375 - accuracy: 0.9882 - val_loss: 0.0289 - val_accuracy: 0.9908
Epoch 12/15
422/422 [==============================] - 14s 33ms/step - loss: 0.0329 - accuracy: 0.9892 - val_loss: 0.0276 - val_accuracy: 0.9917
Epoch 13/15
422/422 [==============================] - 14s 32ms/step - loss: 0.0324 - accuracy: 0.9888 - val_loss: 0.0285 - val_accuracy: 0.9920
Epoch 14/15
422/422 [==============================] - 13s 32ms/step - loss: 0.0363 - accuracy: 0.9879 - val_loss: 0.0279 - val_accuracy: 0.9915
Epoch 15/15
422/422 [==============================] - 13s 31ms/step - loss: 0.0290 - accuracy: 0.9904 - val_loss: 0.0279 - val_accuracy: 0.9915
```

#### Test result
```
Test loss: 0.024496978148818016
Test accuracy: 0.9921000003814697
```