import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime
from sklearn.model_selection import KFold, train_test_split

train, test = list(), list()
dataset = pd.read_json("preprocess/labels.json")
result, fold_iteration = list(), 0

net = Network()
net.add(FCLayer(8, 5))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(5, 3))
net.add(Activation_Layer(tanh, tanh_prime))
net.add(FCLayer(3, 1))
net.add(Activation_Layer(tanh, tanh_prime))
net.use(mse, mse_prime)

kf5 = KFold(n_splits=4, shuffle=True)

for train_index, test_index in kf5.split(range(len(dataset))):
    x_train = dataset.iloc[train_index].iloc[:, 3:].values
    x_test = dataset.iloc[test_index].iloc[:, 3:].values
    y_train = dataset.iloc[train_index].iloc[:, 2:3].values
    y_test = dataset.iloc[test_index].iloc[:, 2:3].values

    """ print(x_test)
    print(x_train) """

    x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
    x_train = x_train.astype('float32')

    x_test = x_test.reshape(x_test.shape[0], 1, 1*8)
    x_test = x_test.astype('float32')

    net.fit(x_train, y_train, epochs=5000, learning_rate=0.025)
    out = net.predict(x_test)

    count = 0
    for i in range(len(out)):

        if(out[i] >= 0.9 and y_test[i] == 1):
            count += 1
        elif(out[i] < 0.1 and y_test[i] == 0):
            count += 1
        print("prediction: ", out[i], ", actual value: ", y_test[i])
    accuracy = (count * 100) / len(out)
    result.append(accuracy)
    fold_iteration += 1

for i, r in enumerate(result):
    print(f'Accuracy {round(r,2)}% on fold {i+1}')
