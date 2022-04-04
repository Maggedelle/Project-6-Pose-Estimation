import numpy as np

def mse(y_true, y_predict):
    return np.mean(np.power(y_true - y_predict, 2))

def mse_prime(y_true, y_predict):
    return 2 * (y_predict - y_true) / y_true.size