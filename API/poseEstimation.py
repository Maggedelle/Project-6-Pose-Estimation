import sys
import const
import calculator as calc
import mediapipe as mp
import base64
import cv2 as cv
import numpy as np
from collections import defaultdict
sys.path.insert(0, './trainer')
from neural_network_class import Network_class

network = Network_class()


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist


fps = 21  # amount of miliseconds to wait, before showing next image
b = 0
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose


def receivedFrameData(connection):
    if(connection.currFrame != None):
        img = decodeBase64(connection.currFrame)
        poseResults = findPose(img, connection.pose)
        features = calculateAngles(poseResults, connection.currExercise, img)
        updateFeatureDict(connection, features)
        if(checkForIteration(features, connection) == True):
            setPrediction(connection)
            connection.features = defaultdict(int)


def showFrame(frame: np.mat, fps: int, connectionId: str, poseResults=None):
    if poseResults and poseResults.pose_landmarks:
        mpDraw.draw_landmarks(
            frame, poseResults.pose_landmarks, mpPose.POSE_CONNECTIONS)
    cv.imshow(connectionId, frame)
    cv.waitKey(fps)


def findPose(frame: np.mat, pose):
    results = pose.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    return results


def updateFeatureDict(connection, features):
    if(features != None):
        connection.features["feature_armcurl"] = 0
        connection.features["feature_armraise"] = 0
        connection.features["feature_pushup"] = 0
        connection.features["f1"] += features["f1"]
        connection.features["f2"] += features["f2"]
        connection.features["f3"] += features["f3"]
        connection.features["f4"] += features["f4"]
        connection.features["f5"] += features["f5"]


def checkForIteration(features, connection):
    if(features != None):
        if(connection.hasBeenUp and connection.currExercise == "armcurl" and features["f1"] > 160):
            print("iteraion")
            connection.hasBeenUp = False
            return True

        elif(connection.hasBeenUp and connection.currExercise == "armraise" and features["f3"] < 10):
            print("iteration")
            connection.hasBeenUp = False
            return True
        elif(connection.hasBeenUp and connection.currExercise == "pushup" and features["f1"] > 145):
            print("iteration")
            connection.hasBeenUp = False
            return True

        if(connection.currExercise == "armcurl" and features["f1"] < 60):
            connection.hasBeenUp = True
        elif(connection.currExercise == "armraise" and features["f3"] > 80 and features["f3"] < 100):
            connection.hasBeenUp = True
        elif(connection.currExercise == "pushup" and features["f1"] < 80):
            connection.hasBeenUp = True

        return False


def calculateAngles(poseResults, exercise, frame):
    features = dict()
    if(poseResults.pose_landmarks != None):
        coordinates = list_coordinates(
            frame, poseResults.pose_landmarks.landmark)
        if(exercise == "armcurl"):
            if(coordinates[const.WRIST_LEFT] != None and coordinates[const.ELBOW_LEFT] != None and coordinates[const.SHOULDER_LEFT] != None):
                arm_angle = calc.angle(
                    coordinates[const.WRIST_LEFT], coordinates[const.ELBOW_LEFT], coordinates[const.SHOULDER_LEFT])
                shoulder_angle = calc.angle(
                    coordinates[const.ELBOW_LEFT], coordinates[const.SHOULDER_LEFT], coordinates[const.HIP_LEFT])
                back_deviation = calc.devation(
                    coordinates[const.SHOULDER_LEFT], coordinates[const.HIP_LEFT])
                features["f1"] = arm_angle
                features["f2"] = back_deviation
                features["f3"] = shoulder_angle
                features["f4"] = 0
                features["f5"] = 0

        elif(exercise == "armraise"):
            if(coordinates[const.WRIST_LEFT] != None and coordinates[const.ELBOW_LEFT] != None and coordinates[const.SHOULDER_LEFT] != None
               and coordinates[const.HIP_LEFT] != None):
                arm_angle = calc.angle(
                    coordinates[const.WRIST_LEFT], coordinates[const.ELBOW_LEFT], coordinates[const.SHOULDER_LEFT])
                shoulder_angle = calc.angle(
                    coordinates[const.HIP_LEFT], coordinates[const.SHOULDER_LEFT], coordinates[const.WRIST_LEFT])
                back_deviation_angle = calc.devation(
                    coordinates[const.SHOULDER_LEFT], coordinates[const.HIP_LEFT])
                features["f1"] = arm_angle
                features["f2"] = back_deviation_angle
                features["f3"] = shoulder_angle
                features["f4"] = 0
                features["f5"] = 0

        elif(exercise == "pushup"):
            if(coordinates[const.WRIST_LEFT] != None and coordinates[const.SHOULDER_LEFT] != None and coordinates[const.ELBOW_LEFT] != None
               and coordinates[const.KNEE_LEFT] != None and coordinates[const.HIP_LEFT] != None and coordinates[const.ANKLE_LEFT] != None):
                arm_angle = calc.angle(
                    coordinates[const.SHOULDER_LEFT], coordinates[const.ELBOW_LEFT], coordinates[const.WRIST_LEFT])
                leg_angle = calc.angle(
                    coordinates[const.ANKLE_LEFT], coordinates[const.KNEE_LEFT], coordinates[const.HIP_LEFT])
                hip_angle = calc.angle(
                    coordinates[const.KNEE_LEFT], coordinates[const.HIP_LEFT], coordinates[const.SHOULDER_LEFT])
                features["f1"] = arm_angle
                features["f2"] = 0
                features["f3"] = 0
                features["f4"] = leg_angle
                features["f5"] = hip_angle

        return features


def normalizeFeatures(connection):
    if(connection.currExercise == "armcurl"):
        connection.features["feature_armcurl"] = 1
        connection.features["f1"] = (connection.features["f1"] - const.ARM_CURL_FEATURE1_MIN) / (
            const.ARM_CURL_FEATURE1_MAX - const.ARM_CURL_FEATURE1_MIN)
        connection.features["f2"] = (connection.features["f2"] - const.ARM_CURL_FEATURE2_MIN) / \
            (const.ARM_CURL_FEATURE2_MAX - const.ARM_CURL_FEATURE2_MIN)
        connection.features["f3"] = (connection.features["f3"] - const.ARM_CURL_FEATURE3_MIN) / \
            (const.ARM_CURL_FEATURE3_MAX - const.ARM_CURL_FEATURE3_MIN)
    elif(connection.currExercise == "armraise"):
        connection.features["feature_armraise"] = 1
        connection.features["f1"] = connection.features["f1"] - const.ARM_RAISE_FEATURE1_MIN / \
            const.ARM_RAISE_FEATURE1_MAX - const.ARM_CURL_FEATURE1_MIN
        connection.features["f2"] = (connection.features["f2"] - const.ARM_RAISE_FEATURE2_MIN) / \
            const.ARM_RAISE_FEATURE2_MAX - const.ARM_RAISE_FEATURE2_MIN
        connection.features["f3"] = (connection.features["f3"] - const.ARM_RAISE_FEATURE3_MIN) / \
            const.ARM_RAISE_FEATURE3_MAX - const.ARM_RAISE_FEATURE3_MIN
    elif(connection.currExercise == "pushup"):
        connection.features["feature_pushup"] = 1
        connection.features["f1"] = connection.features["f1"] - \
            const.PUSH_UP_FEATURE1_MIN / const.PUSH_UP_FEATURE1_MAX - const.PUSH_UP_FEATURE1_MIN
        connection.features["f4"] = (connection.features["f4"] - const.PUSH_UP_FEATURE4_MIN) / \
            const.PUSH_UP_FEATURE4_MAX - const.PUSH_UP_FEATURE4_MIN
        connection.features["f5"] = (connection.features["f5"] - const.PUSH_UP_FEATURE5_MIN) / \
            const.PUSH_UP_FEATURE5_MAX - const.PUSH_UP_FEATURE5_MIN


def setPrediction(connection):
    normalizeFeatures(connection)
    print(connection.features)
    data = np.array([list(connection.features.values())])
    connection.prediction = network.predict(data)


def decodeBase64(bytes: str):
    im_bytes = base64.b64decode(bytes)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
    return img
