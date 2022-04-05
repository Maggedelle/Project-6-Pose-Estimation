import numpy as np
import pandas as pd

dataset = pd.read_json("preprocess/labels.json")
x = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 2:3].values
print(x)
print(y)
