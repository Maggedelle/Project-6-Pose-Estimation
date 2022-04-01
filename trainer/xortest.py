import numpy as np

from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer 
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime

x_train = np.array([[[0,0]], [[0,1]], [[1,0]], [[1,1]]])
y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

net = Network()
net.add(FCLayer(2, 3))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(3, 1))
net.add(Activation_Layer(tanh, tanh_prime))

net.use(mse, mse_prime)
net.fit(x_train, y_train, epochs = 1000, learning_rate = 0.1)

out = net.predict(x_train)
print(out)