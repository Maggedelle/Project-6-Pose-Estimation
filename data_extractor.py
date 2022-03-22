import cv2
import mediapipe as mp
import time
import calculator as calc
import toJSON

WRIST_LEFT = 15
WRIST_RIGHT = 16
ELBOW_LEFT = 13
ELBOW_RIGHT = 14
SHOULDER_LEFT = 11
SHOULDER_RIGHT = 12
HIP_LEFT = 23
HIP_RIGHT = 24


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist


list_data_type = ['arm_angle', 'upperback_angle']
mppose = mp.solutions.pose
pose = mppose.Pose()
angle_list = []
deviation_list = []

for i in range(6):
    cap = cv2.VideoCapture(f'dataset/{i}.wmv')
    while True:
        success, img = cap.read()
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = pose.process(imgRGB)

            if result.pose_landmarks:
                plist = list_coordinates(img, result.pose_landmarks.landmark)
                deviation_list.append(calc.devation(
                    plist[SHOULDER_LEFT], plist[HIP_LEFT]))
                angle_list.append(calc.angle(
                    plist[WRIST_LEFT], plist[ELBOW_LEFT], plist[SHOULDER_LEFT]))

        except Exception as e:
            print(e)
            toJSON.add_data(angle_list, i, list_data_type[0])
            toJSON.add_data(deviation_list, i, list_data_type[1])
            print(f"Done! {i}")
            break
