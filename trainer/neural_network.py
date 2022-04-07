import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime
from sklearn.model_selection import train_test_split


dataset = pd.read_json("preprocess/armcurl.json")
x = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 2:3].values

x_train_armcurl, x_test_armcurl, y_train_armcurl, y_test_armcurl = train_test_split(
    x, y, test_size=0.1)

dataset = pd.read_json("preprocess/armraise.json")
x = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 2:3].values

x_train_armraise, x_test_armraise, y_train_armraise, y_test_armraise = train_test_split(
    x, y, test_size=0.1)

dataset = pd.read_json("preprocess/pushup.json")
x = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 2:3].values

x_train_pushup, x_test_pushup, y_train_pushup, y_test_pushup = train_test_split(
    x, y, test_size=0.1)

x_train = np.concatenate(
    (x_train_armcurl, x_train_armraise, x_train_pushup))
x_test = np.concatenate(
    (x_test_armcurl, x_test_armraise, x_test_pushup))
y_train = np.concatenate(
    (y_train_armcurl, y_train_armraise, y_train_pushup))
y_test = np.concatenate(
    (y_test_armcurl, y_test_armraise, y_test_pushup))


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
net.fit(x_train, y_train, epochs=15000, learning_rate=0.025)

out = net.predict(x_test)

for i in range(len(out)):
    print("prediction: ", out[i], ", actual value: ", y_test[i])

count = 0
for i in range(len(out)):

    if(out[i] >= 0.9 and y_test[i] == 1):
        count += 1
    elif(out[i] < 0.1 and y_test[i] == 0):
        count += 1
    print("prediction: ", out[i], ", actual value: ", y_test[i])

print((count * 100) / len(out), "%")
