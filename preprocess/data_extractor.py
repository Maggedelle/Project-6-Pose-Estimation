import cv2
import mediapipe as mp
import calculator as calc
import json
import os

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


def find_correctness(correctness):
    if correctness == 'correct':
        return 1
    else:
        return 0


mppose = mp.solutions.pose
pose = mppose.Pose()
correct_counter = 0
arm_angle_list, back_deviation_list, shoulder_angle_list, hip_angle_list, leg_angle_list = [], [], [], [], []
master_list = [arm_angle_list, back_deviation_list,
               shoulder_angle_list, hip_angle_list, leg_angle_list]
data = []
id_ = 0
folder = os.listdir('dataset')

with open('preprocess/labels.json', 'w', encoding='utf-8') as f:

    for exercise_folder in folder:
        correct_folder = os.listdir(f'dataset/{exercise_folder}')

        for correctness in correct_folder:
            clips = os.listdir(f'dataset/{exercise_folder}/{correctness}')

            for i in range(len(clips)):
                cap = cv2.VideoCapture(
                    f'dataset/{exercise_folder}/{correctness}/{i}.mp4')

                while True:
                    success, img = cap.read()

                    try:
                        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        result = pose.process(imgRGB)

                        if result.pose_landmarks:
                            p = list_coordinates(
                                img, result.pose_landmarks.landmark)

                            if exercise_folder == 'armcurl':
                                arm_angle_list.append(calc.angle(
                                    p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT]))
                                back_deviation_list.append(calc.devation(
                                    p[SHOULDER_LEFT], p[HIP_LEFT]))

                            elif exercise_folder == 'armraise':
                                arm_angle_list.append(calc.angle(
                                    p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT]))
                                shoulder_angle_list.append(calc.angle(
                                    p[HIP_LEFT], p[SHOULDER_LEFT], p[WRIST_LEFT]))
                                back_deviation_list.append(calc.devation(
                                    p[SHOULDER_LEFT], p[HIP_LEFT]))

                            elif exercise_folder == 'pushup':
                                arm_angle_list.append(calc.angle(
                                    p[SHOULDER_LEFT], p[ELBOW_LEFT], p[WRIST_LEFT]))
                                leg_angle_list.append(calc.angle(
                                    p[ANKLE_LEFT], p[KNEE_LEFT], p[HIP_LEFT]))
                                hip_angle_list.append(calc.angle(
                                    p[KNEE_LEFT], p[HIP_LEFT], p[SHOULDER_LEFT]))

                    except Exception as e:
                        # print(e)
                        if exercise_folder == 'armcurl':
                            data.append(
                                {'id': id_, 'exercise': exercise_folder, 'correct': find_correctness(correctness), 'feature_armcurl': 1, 'feature_armraise': 0, 'feature_pushup': 0, 'feature_1': sum(arm_angle_list.copy()), 'feature_2': sum(back_deviation_list.copy()), 'feature_3': 0, "feature_4": 0, "feature_5": 0})

                        elif exercise_folder == 'armraise':
                            data.append(
                                {'id': id_, 'exercise': exercise_folder, 'correct': find_correctness(correctness), 'feature_armcurl': 0, 'feature_armraise': 1, 'feature_pushup': 0, 'feature_1': sum(arm_angle_list.copy()), 'feature_2': sum(back_deviation_list.copy()), 'feature_3': sum(shoulder_angle_list.copy()), "feature_4": 0, "feature_5": 0})

                        elif exercise_folder == 'pushup':
                            data.append(
                                {'id': id_, 'exercise': exercise_folder, 'correct': find_correctness(correctness), 'feature_armcurl': 0, 'feature_armraise': 0, 'feature_pushup': 1, 'feature_1': sum(arm_angle_list.copy()), 'feature_2': 0, 'feature_3': 0, 'feature_4': sum(leg_angle_list.copy()), 'feature_5': sum(hip_angle_list.copy())})

                        for lists in master_list:
                            lists.clear()

                        print(f'Processing [{x}]')
                        break
                id_ += 1
    json.dump(data, f)
