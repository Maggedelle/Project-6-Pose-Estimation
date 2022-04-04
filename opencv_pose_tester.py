import cv2
import mediapipe as mp
import time
import math
import numpy as np
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

def calc_angle(p1, p2, p3):
    vector_ab = p1[1] - p2[1], p1[2] - p2[2]
    vector_bc = p3[1] - p2[1], p3[2] - p2[2]

    dot_product = (vector_ab[0] * vector_bc[1]) + (vector_ab[1] * vector_bc[0])

    lenght_ab = np.sqrt(vector_ab[0]**2 + vector_bc[1]**2)
    lenght_bc = np.sqrt(vector_bc[0]**2 + vector_bc[1]**2)

    angel = math.degrees(math.atan2(
        p3[2]-p2[2], p3[1] - p2[1])-math.atan2(p1[2]-p2[2], p1[1]-p2[1]))
    if angel < 0:
        angel += 360
        if angel >= 360:
            angel -= 360
    return angel
    # math.degrees(np.arccos(dot_product/(lenght_ab*lenght_bc)))


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist


mp_draw = mp.solutions.drawing_utils
mppose = mp.solutions.pose

pose = mppose.Pose()

cap = cv2.VideoCapture('dataset/14.wmv')
#cap = cv2.VideoCapture(0)
time_b = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    if result.pose_landmarks:
        mp_draw.draw_landmarks(img, result.pose_landmarks,
                               mppose.POSE_CONNECTIONS)
        plist = list_coordinates(img, result.pose_landmarks.landmark)

        cv2.putText(img, str(int(calc_angle(
                       plist[SHOULDER_LEFT],  plist[ELBOW_LEFT], plist[WRIST_LEFT]))), (plist[ELBOW_LEFT][1] - 50, plist[ELBOW_LEFT][2] + 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
      #  cv2.putText(img, str(int(calc_angle(plist[23], plist[25], plist[27]))), (plist[25][1] - 50, plist[25][2] + 30),
       #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
       # cv2.putText(img, str(int(calc_angle(plist[24], plist[12], plist[14]))), (plist[12][1] - 50, plist[12][2] + 30),
        #            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
        #cv2.putText(img, str(int(calc_angle(plist[13], plist[11], plist[23]))), (plist[11][1] - 50, plist[11][2] + 30),
         #           cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))

        print(calc_angle(plist[24], plist[26], plist[28]))
        print(plist)

    time_a = time.time()
    fps = 1/(time_a-time_b)
    time_b = time_a

    cv2.putText(img, "fps: " + str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(100)
