import json


def add_data(json_list, index, angle_type):
    with open("dataset/labels.json", "r+") as file:
        data = json.load(file)

    # for i in range(len(data["labels"])):
    data["labels"][index][angle_type] = json_list

    with open("dataset/labels.json", "w") as file:
        json.dump(data, file)
