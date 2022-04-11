from collections import defaultdict
from pickle import FALSE
import string
from tokenize import String
from turtle import back
import numpy as np
import cv2 as cv
import base64
import mediapipe as mp
import calculator as calc

WRIST_LEFT = 15
WRIST_RIGHT = 16
ELBOW_LEFT = 13
ELBOW_RIGHT = 14
SHOULDER_LEFT = 11
SHOULDER_RIGHT = 12
HIP_LEFT = 23
HIP_RIGHT = 24
KNEE_LEFT = 25
KNEE_RIGHT = 26
ANKLE_LEFT = 27
ANKLE_RIGHT = 28


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist

fps = 42 #amount of miliseconds to wait, before showing next image

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
    
async def receivedFrameData(connections):
    for connection in connections:
        if(connection.currFrame != None):
            img = await decodeBase64(connection.currFrame)
            poseResults = await findPose(img, connection.pose)
            features = await calculateAngles(poseResults, connection.currExercise, img)
            await updateFeatureDict(connection,features)
            if(await checkForIteration(features, connection) == True):
                print(connection.prevAngles["f1"])
                connection.prevAngles = defaultdict(int)
            await showFrame(img, fps,connection.id,poseResults)

async def showFrame(frame:np.mat, fps:int, connectionId:str, poseResults = None):
    if poseResults and poseResults.pose_landmarks:
        mpDraw.draw_landmarks(frame,poseResults.pose_landmarks,mpPose.POSE_CONNECTIONS)
    cv.imshow(connectionId,frame)
    cv.waitKey(fps)

async def findPose(frame:np.mat, pose):
    results = pose.process(frame)
    return results

async def updateFeatureDict(connection, features):
    if(features != None):
        connection.prevAngles["f1"] += features["f1"]
        connection.prevAngles["f2"] += features["f2"]
        connection.prevAngles["f3"] += features["f3"]
        connection.prevAngles["f4"] += features["f4"]
        connection.prevAngles["f5"] += features["f5"]

async def checkForIteration(features, connection):
    if(features != None):
        if(connection.hasBeenUp and connection.currExercise == "armcurl" and features["f1"] > 160):
            print("iteraion")
            connection.hasBeenUp = False
            return True
        
        elif(connection.hasBeenUp and connection.currExercise == "armraise" and features["f1"] < 10):
            print("iteration")
            connection.hasBeenUp = False
            return True
        elif(connection.hasBeenUp and connection.currExercise == "pushup" and features["f1"] > 145):
            print("iteration")
            connection.hasBeenUp = False
            return True

        if(connection.currExercise == "armcurl"  and features["f1"] < 60):
            connection.hasBeenUp = True
        elif(connection.currExercise == "armraise" and features["f1"] > 80):
            connection.hasBeenUp = True
        elif(connection.currExercise == "pushup" and features["f1"] > 145):
            connection.hasBeenUp = True

        return False
        

async def calculateAngles(poseResults, exercise, frame):
    features = dict();
    if(poseResults.pose_landmarks != None):
        coordinates = list_coordinates(frame,poseResults.pose_landmarks.landmark)
        if(exercise == "armcurl"):
            if(coordinates[WRIST_LEFT] != None and coordinates[ELBOW_LEFT] != None and coordinates[SHOULDER_LEFT] != None):
                arm_angle = calc.angle(coordinates[WRIST_LEFT], coordinates[ELBOW_LEFT], coordinates[SHOULDER_LEFT])
                shoulder_angle = calc.angle(coordinates[ELBOW_LEFT], coordinates[SHOULDER_LEFT], coordinates[HIP_LEFT])
                back_deviation = calc.devation(coordinates[SHOULDER_LEFT], coordinates[HIP_LEFT])
                features["f1"] = arm_angle
                features["f2"] = back_deviation
                features["f3"] = shoulder_angle
                features["f4"] = 0
                features["f5"] = 0

        elif(exercise == "armraise"):
            if(coordinates[WRIST_LEFT] != None and coordinates[ELBOW_LEFT] != None and coordinates[SHOULDER_LEFT] != None
            and coordinates[HIP_LEFT] != None):
                arm_angle = calc.angle(coordinates[WRIST_LEFT], coordinates[ELBOW_LEFT], coordinates[SHOULDER_LEFT])
                shoulder_angle = calc.angle(coordinates[HIP_LEFT], coordinates[SHOULDER_LEFT], coordinates[WRIST_LEFT])
                back_deviation_angle = calc.devation(coordinates[SHOULDER_LEFT], coordinates[HIP_LEFT])
                features["f1"] = arm_angle
                features["f2"] = back_deviation_angle 
                features["f3"] = shoulder_angle
                features["f4"] = 0
                features["f5"] = 0

        elif(exercise == "pushup"):
            if(coordinates[WRIST_LEFT] != None and coordinates[SHOULDER_LEFT] != None and coordinates[ELBOW_LEFT] != None
            and coordinates[KNEE_LEFT] != None and coordinates[HIP_LEFT] != None and coordinates[ANKLE_LEFT] != None):
                arm_angle = calc.angle(coordinates[SHOULDER_LEFT], coordinates[ELBOW_LEFT], coordinates[WRIST_LEFT])
                leg_angle = calc.angle(coordinates[ANKLE_LEFT, coordinates[KNEE_LEFT], coordinates[HIP_LEFT]])
                hip_angle = calc.angle(coordinates[KNEE_LEFT], coordinates[HIP_LEFT], coordinates[SHOULDER_LEFT])
                features["f1"] = arm_angle
                features["f2"] = 0
                features["f3"] = 0
                features["f4"] = leg_angle
                features["f5"] = hip_angle
        
        return features

async def decodeBase64(bytes:str):
    im_bytes = base64.b64decode(bytes)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)    
    return img