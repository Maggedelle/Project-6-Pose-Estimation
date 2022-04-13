
import json


def normalizer():
    armcurls_f1 = []
    armcurls_f2 = []
    armcurls_f3 = []
    armcurls_f4 = []
    armcurls_f5 = []
    armraises_f1 = []
    armraises_f2 = []
    armraises_f3 = []
    armraises_f4 = []
    armraises_f5 = []
    pushups_f1 = []
    pushups_f2 = []
    pushups_f3 = []
    pushups_f4 = []
    pushups_f5 = []

    with open('preprocess/labels.json', 'r+') as f:
        data = json.load(f)
        for exercise in data:
            if(exercise["exercise"] == "armcurl"):
                armcurls_f1.append(exercise["feature_1"])
                armcurls_f2.append(exercise["feature_2"])
                armcurls_f3.append(exercise["feature_3"])
                armcurls_f4.append(exercise["feature_4"])
                armcurls_f5.append(exercise["feature_5"])

            elif(exercise["exercise"] == "armraise"):
                armraises_f1.append(exercise["feature_1"])
                armraises_f2.append(exercise["feature_2"])
                armraises_f3.append(exercise["feature_3"])
                armraises_f4.append(exercise["feature_4"])
                armraises_f5.append(exercise["feature_5"])

            elif(exercise["exercise"] == "pushup"):
                pushups_f1.append(exercise["feature_1"])
                pushups_f2.append(exercise["feature_2"])
                pushups_f3.append(exercise["feature_3"])
                pushups_f4.append(exercise["feature_4"])
                pushups_f5.append(exercise["feature_5"])

            print("arm curl feature_1 average",
                  sum(armcurls_f1)/len(armcurls_f1))
            """ print("arm curl feature 2 max: ", max(
                armcurls_f2), ", min: ", min(armcurls_f2))
            print("arm curl feature 3 max: ", max(
                armcurls_f3), ", min: ", min(armcurls_f3))

            print("armraise feature 1 max: ", max(
                armraises_f1), ", min: ", min(armraises_f1))
            print("armraise feature 2 max: ", max(
                armraises_f2), ", min: ", min(armraises_f2))
            print("armraise feature 3 max: ", max(
                armraises_f3), ", min: ", min(armraises_f3)) """

            print("push up feature  1 max: ", max(
                pushups_f1), ", min: ", min(pushups_f1))
            print("push up feature  4 max: ", max(
                pushups_f4), ", min: ", min(pushups_f4))
            print("push up feature  5 max: ", max(
                pushups_f5), ", min: ", min(pushups_f5))

        for exercise in data:
            if(exercise["exercise"] == "armcurl"):
                if(exercise["feature_1"] != 0):
                    exercise["feature_1"] = (
                        exercise["feature_1"] - min(armcurls_f1)) / (max(armcurls_f1) - min(armcurls_f1))
                if(exercise["feature_2"] != 0):
                    exercise["feature_2"] = (
                        exercise["feature_2"] - min(armcurls_f2)) / (max(armcurls_f2) - min(armcurls_f2))
                if(exercise["feature_3"] != 0):
                    exercise["feature_3"] = (
                        exercise["feature_3"] - min(armcurls_f3)) / (max(armcurls_f3) - min(armcurls_f3))
                if(exercise["feature_4"] != 0):
                    exercise["feature_4"] = (
                        exercise["feature_4"] - min(armcurls_f4)) / (max(armcurls_f4) - min(armcurls_f4))
                if(exercise["feature_5"] != 0):
                    exercise["feature_5"] = (
                        exercise["feature_5"] - min(armcurls_f5)) / (max(armcurls_f5) - min(armcurls_f5))
            if(exercise["exercise"] == "armraise"):
                if(exercise["feature_1"] != 0):
                    exercise["feature_1"] = (
                        exercise["feature_1"] - min(armraises_f1)) / (max(armraises_f1) - min(armraises_f1))
                if(exercise["feature_2"] != 0):
                    exercise["feature_2"] = (
                        exercise["feature_2"] - min(armraises_f2)) / (max(armraises_f2) - min(armraises_f2))
                if(exercise["feature_3"] != 0):
                    exercise["feature_3"] = (
                        exercise["feature_3"] - min(armraises_f3)) / (max(armraises_f3) - min(armraises_f3))
                if(exercise["feature_4"] != 0):
                    exercise["feature_4"] = (
                        exercise["feature_4"] - min(armraises_f4)) / (max(armraises_f4) - min(armraises_f4))
                if(exercise["feature_5"] != 0):
                    exercise["feature_5"] = (
                        exercise["feature_5"] - min(armraises_f5)) / (max(armraises_f5) - min(armraises_f5))
            if(exercise["exercise"] == "pushup"):
                if(exercise["feature_1"] != 0):
                    exercise["feature_1"] = (
                        exercise["feature_1"] - min(pushups_f1)) / (max(pushups_f1) - min(pushups_f1))
                if(exercise["feature_2"] != 0):
                    exercise["feature_2"] = (
                        exercise["feature_2"] - min(pushups_f2)) / (max(pushups_f2) - min(pushups_f2))
                if(exercise["feature_3"] != 0):
                    exercise["feature_3"] = (
                        exercise["feature_3"] - min(pushups_f3)) / (max(pushups_f3) - min(pushups_f3))
                if(exercise["feature_4"] != 0):
                    exercise["feature_4"] = (
                        exercise["feature_4"] - min(pushups_f4)) / (max(pushups_f4) - min(pushups_f4))
                if(exercise["feature_5"] != 0):
                    exercise["feature_5"] = (
                        exercise["feature_5"] - min(pushups_f5)) / (max(pushups_f5) - min(pushups_f5))

    with open('preprocess/labels.json', 'w') as f:
        json.dump(data, f)

    armcurls_f1.clear()
    armcurls_f2.clear()
    armcurls_f3.clear()
    armcurls_f4.clear()
    armcurls_f5.clear()
    armraises_f1.clear()
    armraises_f2.clear()
    armraises_f3.clear()
    armraises_f4.clear()
    armraises_f5.clear()
    pushups_f1.clear()
    pushups_f2.clear()
    pushups_f3.clear()
    pushups_f4.clear()
    pushups_f5.clear()
    print("Data normalized ✔️")