import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime

training_set = pd.read_json("preprocess/labels.json")
x_train = training_set.iloc[:, 3:].values
y_train = training_set.iloc[:, 2:3].values

x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
x_train = x_train.astype('float32')

test_set = pd.read_json("preprocess/testset.json")
x_test = test_set.iloc[:, 3:].values
x_test_actual = test_set.iloc[:, 2:3].values

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
net.fit(x_train, y_train, epochs=5000, learning_rate=0.1)

out = net.predict(x_test)
count = 0;
for i in range(len(out)):
   
    if(out[i] >= 0.8 and x_test_actual[i] == 1):
        count+=1
    elif(out[i] < 0.2 and x_test_actual[i] == 0):
        count+=1
    print("prediction: ", out[i], ", actual value: ", x_test_actual[i])

print((count * 100) / len(out), "%")