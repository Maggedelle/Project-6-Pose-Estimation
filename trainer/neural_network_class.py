import numpy as pd
from network_model.network import Network
from layers.fc_layer import FCLayer
from layers.activation_layer import Activation_Layer
from helper_functions.activation_functions import tanh, tanh_prime
from helper_functions.loss_function import mse, mse_prime
from helper_functions.save_weight import load

class Network_class():
    def __init__(self):

        input_layer = FCLayer(8, 16)
        middel_layer = FCLayer(16, 12)
        output_layer = FCLayer(12, 9)

        input_layer.weights = load('weights', 0)
        input_layer.bias = load('bias', 0)

        middel_layer.weights = load('weights', 1)
        middel_layer.bias = load('bias', 1)

        output_layer.weights = load('weights', 2)
        output_layer.bias = load('bias', 2)
        self.network  = Network()
        self.network.add(input_layer)
        self.network.add(Activation_Layer(tanh, tanh_prime))
        self.network.add(middel_layer)
        self.network.add(Activation_Layer(tanh, tanh_prime))
        self.network.add(output_layer)
        self.network.add(Activation_Layer(tanh, tanh_prime))
        self.network.use(mse, mse_prime)

    def predict(self, input_data):
        input_data = input_data.astype('float32')

        result = self.network.predict(input_data)
        #print(input_data)
        #(correct, arm_angle_correct, arm_angle_wide, arm_angle_narrow, back_correct, back_bend, 
        # shoulder_angle_correct, shoulder_angle_wide, shoulder_angle_narrow)
        #print(list(result[0][0]))
        return list(result[0][0])

