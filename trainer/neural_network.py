from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfd
from IPython.display import display
import keras
from keras.models import Sequential
from keras.layers import Dense

dataset = pd.read_json("dataset/labels.json")
x = dataset.iloc[:, :6].values
y = dataset.iloc[:, 1:2].values
print(dataset.info())
display(dataset)
# display(pd.DataFrame(x))
# display(pd.DataFrame(y))
#sc = StandardScaler()

# Neural network
""" model = Sequential()
model.add(Dense(16, input_dim=20, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(4, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
 """
