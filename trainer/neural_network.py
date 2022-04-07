import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime
from sklearn.model_selection import train_test_split

dataset = pd.read_json("preprocess/labels.json")
x = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 2:3].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
x_train = x_train.astype('float32')

x_test = x_test.reshape(x_test.shape[0], 1, 1*8)
x_test = x_test.astype('float32')


net = Network()
net.add(FCLayer(8, 5))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(5, 3))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(3, 1))
net.add(Activation_Layer(tanh, tanh_prime))


net.use(mse, mse_prime)
net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

out = net.predict(x_test)

for i in range(len(out)):
    print("prediction: ", out[i], ", actual value: ", y_test[i])
