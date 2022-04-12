import json
import numpy as np

PATH = "trainer/helper_functions/weights.json"


def save(weights, bias, index):
    with open(PATH, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data[index]['weights'] = weights.tolist()
        data[index]['bias'] = bias.tolist()
    with open(PATH, 'w') as f:
        json.dump(data, f)


def load(element, index):
    with open(PATH, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        return np.array(data[index][element])
