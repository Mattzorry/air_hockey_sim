import numpy as np

def sigmoid(x):
    """ Return the sigmoid function of x. """
    return 1 / (1 + np.exp(-x))

def square_sigmoid(x):
    return 1 / (1 + np.power(2,-x))

# def norm_sigmoid(x, flatten=1):
#     return sigmoid(flatten*(x-50)/100)

# def flatter_sigmoid_comp(x, y, flatten=0.5):
#     return sigmoid(flatten*(x - y) / 100)

def norm_sigmoid(x, flatten=1):
    return square_sigmoid(flatten*(x-50)/50)

def flatter_sigmoid_comp(x, y, flatten=0.5):
    return square_sigmoid(flatten*(x - y) / 50)

def general_sigmoid(base, exponent, center=0, spread=1):
    return 1 / (1 + np.power(base,-spread*(exponent-center)))