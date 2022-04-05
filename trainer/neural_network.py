import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime

dataset = pd.read_json("preprocess/labels.json")
x_train = dataset.iloc[:, 3:].values
y_train = dataset.iloc[:, 2:3].values

# x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
# x_train = x_train.astype('float32')

net = Network()
net.add(FCLayer(8, 5))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(5, 1))
net.add(Activation_Layer(tanh, tanh_prime))


net.use(mse, mse_prime)
net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

out = net.predict(x_train)
print(out)
