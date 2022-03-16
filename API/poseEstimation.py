import numpy as np
import cv2 as cv
import base64
import mediapipe as mp

fps = 100 #amount of miliseconds to wait, before showing next image

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

async def receivedFrameData(bytes:str):
    img = await decodeBase64(bytes)
    poseResults = await findPose(img)
    await showFrame(img, fps, poseResults)

async def showFrame(frame:np.mat, fps:int, poseResults = None):
    if poseResults and poseResults.pose_landmarks:
        mpDraw.draw_landmarks(frame,poseResults.pose_landmarks,mpPose.POSE_CONNECTIONS)
    cv.imshow("img",frame)
    cv.waitKey(fps)

async def findPose(frame:np.mat):
    results = pose.process(frame)
    return results

async def decodeBase64(bytes:str):
    im_bytes = base64.b64decode(bytes)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)    
    return img