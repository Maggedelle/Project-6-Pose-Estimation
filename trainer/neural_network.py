import numpy as np
import pandas as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime
from helper_functions.save_weight import save, load
from sklearn.model_selection import KFold

dataset = pd.read_json("preprocess/labels.json")
result, fold_iteration = list(), 0

input_layer = FCLayer(8, 5)
middel_layer = FCLayer(5, 3)
output_layer = FCLayer(3, 4)

input_layer.weights = load('weights', 0)
input_layer.bias = load('bias', 0)

middel_layer.weights = load('weights', 1)
middel_layer.bias = load('bias', 1)

output_layer.weights = load('weights', 2)
output_layer.bias = load('bias', 2)

net = Network()
net.add(input_layer)
net.add(Activation_Layer(tanh, tanh_prime))
net.add(middel_layer)
net.add(Activation_Layer(tanh, tanh_prime))
net.add(output_layer)
net.add(Activation_Layer(tanh, tanh_prime))
net.use(mse, mse_prime)

kf5 = KFold(n_splits=4, shuffle=True)
for train_index, test_index in kf5.split(range(len(dataset))):

    x_train = dataset.iloc[train_index].iloc[:, 6:].values
    x_test = dataset.iloc[test_index].iloc[:, 6:].values

    y_train = dataset.iloc[train_index].iloc[:, 2:6].values
    y_test = dataset.iloc[test_index].iloc[:, 2:6].values

    x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
    x_train = x_train.astype('float32')

    x_test = x_test.reshape(x_test.shape[0], 1, 1*8)
    x_test = x_test.astype('float32')

    net.fit(x_train, y_train, epochs=1000,
            learning_rate=0.025, save_weights=save)
    out = net.predict(x_test)

    count = 0
    for i in range(len(out)):
        for j in range(len(out[i])):
            for k in range(len(out[i][j])):
                if(out[i][j][k] >= 0.9 and y_test[i][j] == 1):
                    count += 1
                elif(out[i][j][k] < 0.1 and y_test[i][j] == 0):
                    count += 1
            print("prediction: ", out[i][j], ", actual value: ", y_test[i])
    accuracy = (count/4)*100 / len(out)
    result.append(accuracy)
    fold_iteration += 1

for i, r in enumerate(result):
    print(f'Accuracy {r:0.2f}% on fold {i+1}')
print(f'Accuracy average: {sum(result)/len(result):0.2f}%')
