import json

PATH = "C:/P6/Project-6-Pose-Estimation/dataset/labels.json"

def labels_lenght():
    with open(PATH, "r+") as file:
        data = json.load(file)
    return len(data)


def add_data(json_list, index, angle_type):
    with open(PATH, "r+") as file:
        data = json.load(file)

    data[index][angle_type] = json_list

    with open(PATH, "w") as file:
        json.dump(data, file)


def find_exercise(index):
    with open(PATH, "r+") as file:
        data = json.load(file)
    return data[index]['exercise']


def read_json():
    with open(PATH, "r+") as file:
        data = json.load(file)
    return data
