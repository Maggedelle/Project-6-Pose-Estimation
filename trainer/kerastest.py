from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

training_set = pd.read_json("preprocess/labels.json")
x = training_set.iloc[:, 3:].values
y = training_set.iloc[:, 2:3].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
x_train = x_train.reshape(x_train.shape[0], 1, 1*8)
x_train = x_train.astype('float32')

x_test = x_test.reshape(x_test.shape[0], 1, 1*8)
x_test = x_test.astype('float32')

# Neural network
model = Sequential()
model.add(Dense(16, input_dim=8, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(1, activation='softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=10000, batch_size=64)

y_pred = model.predict(x_test)
# Converting predictions to label
pred = list()
for i in range(len(y_pred)):
    pred.append(np.argmax(y_pred[i]))
# Converting one hot encoded test label to label
test = list()
for i in range(len(y_test)):
    test.append(np.argmax(y_test[i]))

a = accuracy_score(pred, test)
print('Accuracy is:', a*100)
